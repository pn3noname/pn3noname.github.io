#!/usr/bin/env python3
"""
build_notes.py
--------------
notes/ 폴더를 재귀 탐색하여 모든 .md 파일의 frontmatter + content를
읽고 notes-data.js 를 자동 생성합니다.

보안 고려사항:
- Path traversal 방지: notes/ 폴더 외부 경로 차단
- 입력값 sanitize: HTML 특수문자 이스케이프
- 파일 크기 제한: 단일 파일 1MB 초과 시 스킵
- .gitkeep, 숨김 파일 스킵
- slug 형식 검증: 영문자/숫자/하이픈만 허용
"""

import json
import os
import re
import sys
from pathlib import Path

import frontmatter  # python-frontmatter

# ── 설정 ──────────────────────────────────────────────────────────────────────
REPO_ROOT   = Path(__file__).resolve().parent.parent
NOTES_DIR   = REPO_ROOT / "notes"
OUTPUT_FILE = REPO_ROOT / "notes-data.js"
MAX_FILE_BYTES = 1 * 1024 * 1024   # 1MB

# slug에 허용되는 문자: 소문자, 숫자, 하이픈
SLUG_PATTERN = re.compile(r'^[a-z0-9][a-z0-9\-]{0,99}$')

# HTML 특수문자 이스케이프 맵
HTML_ESCAPE = str.maketrans({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
})


def sanitize_text(value: str) -> str:
    """문자열에서 HTML 특수문자를 이스케이프하고 제어문자를 제거합니다."""
    if not isinstance(value, str):
        value = str(value)
    # 제어문자 제거 (탭·줄바꿈 제외)
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
    return value.translate(HTML_ESCAPE)


def validate_slug(slug: str) -> bool:
    """slug가 안전한 형식인지 검증합니다."""
    return bool(SLUG_PATTERN.match(slug))


def is_safe_path(path: Path) -> bool:
    """경로가 notes/ 폴더 내부에 있는지 확인합니다 (path traversal 방지)."""
    try:
        path.resolve().relative_to(NOTES_DIR.resolve())
        return True
    except ValueError:
        return False


def slugify(text: str) -> str:
    """파일명에서 자동으로 slug를 생성합니다."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text[:100]  # 최대 100자


def parse_tags(raw) -> list:
    """tags 필드를 항상 문자열 리스트로 반환합니다."""
    if isinstance(raw, list):
        return [sanitize_text(str(t).strip()) for t in raw if str(t).strip()]
    if isinstance(raw, str):
        return [sanitize_text(t.strip()) for t in raw.split(',') if t.strip()]
    return []


def collect_notes() -> list:
    """notes/ 폴더를 재귀 탐색하여 노트 데이터를 수집합니다."""

    if not NOTES_DIR.exists():
        print(f"[warn] notes/ 폴더가 없습니다: {NOTES_DIR}")
        return []

    notes = []
    skipped = 0

    # 모든 .md 파일을 재귀 탐색 (깊이 제한 없음)
    for md_file in sorted(NOTES_DIR.rglob("*.md")):

        # ── 보안 검사 ──────────────────────────────────────────────────
        # 1. path traversal 방지
        if not is_safe_path(md_file):
            print(f"[skip] 경로 벗어남: {md_file}")
            skipped += 1
            continue

        # 2. 숨김 파일 / .gitkeep 스킵
        if any(part.startswith('.') for part in md_file.parts):
            continue
        if md_file.name == '.gitkeep':
            continue

        # 3. 파일 크기 제한
        if md_file.stat().st_size > MAX_FILE_BYTES:
            print(f"[skip] 파일 크기 초과 (>{MAX_FILE_BYTES//1024}KB): {md_file.name}")
            skipped += 1
            continue

        # ── frontmatter 파싱 ───────────────────────────────────────────
        try:
            post = frontmatter.load(str(md_file))
        except Exception as e:
            print(f"[skip] frontmatter 파싱 오류 ({md_file.name}): {e}")
            skipped += 1
            continue

        meta = post.metadata

        # ── slug 처리 ──────────────────────────────────────────────────
        raw_slug = meta.get('slug', '') or slugify(md_file.stem)
        slug = slugify(str(raw_slug))

        if not validate_slug(slug):
            print(f"[skip] 유효하지 않은 slug '{slug}': {md_file.name}")
            skipped += 1
            continue

        # ── 필드 수집 및 sanitize ──────────────────────────────────────
        title       = sanitize_text(str(meta.get('title', md_file.stem)))
        date        = sanitize_text(str(meta.get('date', '')))
        category    = sanitize_text(str(meta.get('category', '')))
        description = sanitize_text(str(meta.get('description', '')))
        tags        = parse_tags(meta.get('tags', []))

        # content는 JSON으로 직렬화되므로 별도 이스케이프 불필요
        # (json.dumps가 처리)
        content = post.content

        notes.append({
            "slug":        slug,
            "title":       title,
            "date":        date,
            "category":    category,
            "tags":        tags,
            "description": description,
            "content":     content,
        })

        print(f"[ok] {md_file.relative_to(REPO_ROOT)}  →  slug: {slug}")

    # 날짜 기준 내림차순 정렬 (최신 노트가 먼저)
    notes.sort(key=lambda n: n.get('date', ''), reverse=True)

    print(f"\n총 {len(notes)}개 노트 수집 완료 ({skipped}개 스킵)")
    return notes


def write_output(notes: list) -> None:
    """notes-data.js 파일을 생성합니다."""

    # JSON 직렬화 (ensure_ascii=False → 한글 유지)
    json_str = json.dumps(notes, ensure_ascii=False, indent=2)

    js_content = f"""// notes-data.js
// ⚠️  이 파일은 GitHub Actions가 자동 생성합니다. 직접 수정하지 마세요.
// Generated: auto by scripts/build_notes.py

const notesData = {json_str};
"""

    OUTPUT_FILE.write_text(js_content, encoding='utf-8')
    print(f"[done] {OUTPUT_FILE.relative_to(REPO_ROOT)} 생성 완료 ({len(notes)}개 노트)")


def main():
    notes = collect_notes()
    write_output(notes)

    # 노트가 0개여도 오류로 처리하지 않음 (빈 배열로 정상 생성)
    sys.exit(0)


if __name__ == '__main__':
    main()
