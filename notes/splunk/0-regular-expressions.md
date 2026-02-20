---
title: "Regular Expressions; Regex"
slug: "0-regular-expressions"
date: "2026-02-20"
category: "Splunk"
tags: ["Regex", "Charsets", "Wildcards", "Metacharacters"]
description: "A practical introduction to regular expressions covering four core concepts — charsets, wildcards, metacharacters with repetition syntax, and grouping with anchors — as a foundation for working with Splunk's search and filtering capabilities."
---

source: https://tryhackme.com/room/catregex

# 1. Charsets (문자 집합)
  - 파일이나 텍스트 불록에서 특정 문자열을 검색할 때는 `grep 'string' <file>`처럼 그대로 검색하면 되지만, 텍스트의 패턴을 검색하고 싶다면 Regex를 사용하면 됨 (ex: 특정 글자로 시작하는 단어나 숫자로 끝나는 단어)
  - Charsetsdms 대괄호 `[ ]` 안에 매칭하고 싶은 문자나 문자 범위를 넣어서 정의함. 그럼 검색 중인 파일 / 텍스트에서 정의한 패턴이 나타나는 모든 곳을 찾아줌

## 1. 기본 사용법
  - `[abc]`는 `a`, `b`, `c`를 매칭함 (각 글자가 나타나는 모든 위치)
  - `[abc]zz`는 `azz`, `bzz`, `czz`를 매칭함

## 2. 범위 지정
  - `-` 대시를 사용하여 범위를 정의할 수 있음

## 3. 범위 조합
  - `[a-cx-z]zz`는 `azz`, `bzz`, `czz`, `xzz`, `yzz`, `zzz`를 매칭함
  - 모든 알파벳 문자를 매칭하는 데 사용할 수 있음
    - `[a-zA-Z]`는 모든 단일 글자를 매칭함 (소문자 또는 대문자)

## 4. 숫자 사용
  - `file[1-3]`은 `file1`, `file2`, `file3`을 매칭함

## 5. 제외 패턴
  - `^` 캐럿 기호를 사용하여 문자 집합에서 문자를 제외하고 나머지 모든 것을 포함할 수 있음
  - `[^k]ing`은 `ring`, `sing`, `$ing`을 매칭하지만 `king`은 매칭하지 않음
  - 단일 문자뿐만 아니라 문자 집합도 제외할 수 있음
    - `[^a-c]at`은 `fat`와 `hat`을 매칭하지만, `bat`이나 `cat`은 매칭하지 않음

## 6. 주의사항
### 1. 문자열 != 문자 집합
  - 문자 집합 `[abc]`는 문자열 `abc`를 매칭하지만, `cba`와 `ca`도 매칭함
  - 문자열을 매칭하는 것이 아니라, 해당 문자열에서 지정된 문자가 나타나는 모든 경우를 매칭함

### 2. 문자 집합을 지정할 때는 질문에 나타난 순서대로 글자을 입력해야 함

### 3. 특정 문자열과 매칭되는 다양한 패턴이 많이 있음, 즉, 정답이 여러 개일 수 있는데, 일반적으로 정답이라 함은 해당 질문에 대해 가장 효율적인 정규식임

### Questions
 1. Match all of the following characters: c, o, g
  -> [cog]

 2. Match all of the following words: cat, fat, hat
  -> [cfh]at

 3. Match all of the following words: Cat, cat, Hat, hat
  -> [CcHh]at

 4. Match all of the following filenames: File1, File2, file3, file4, file5, File7, fild9
  -> [Ff]ile[1-9]

 5. Match all of the filenames of question 4, except "File" (use the hat symbol)
  -> [Ff]ile[^7]


# 2. Wildcards and optional characters (와일드카드와 선택적 문자)
## 모든 단일 문자 (줄바꿈 제외)와 일치하는 데 사용되는 와일드카드는 `.` 점
  - ex: `a.c` = `aac`, `abc`, `a0c`, `a!c`

## `?`물음표를 사용하여 패턴에서 문자를 선택 사항으로 설정 가능
  - ex: `abc?` = `ab`, `abc` (∵ `c`가 선택 사항)

## Literal dot (`.`)을 검색하려면 `\` 역슬래시로 escape해야 함
  - ex: `a.c` = `abc` or `a@c`
  - ex: `a\.c` = (only) `a.c`

## Questions
  1. Match all of the following words: Cat, fat, hat, rat
      -> .at
  
  2. Match all of the following words: Cat, cats
      -> [Cc]ats?
  
  3. Match the following domain name: cat.xyz
    -> `cat\.xyz`

  4. Match all of the following domain names: cat.xyz, cats.xyz, hats.xyz
    -> `[ch]ats?\.xyz`

  5. Match every 4-letter string that doesn't end in any letter from n to z
    -> ...[^n-z]

  6. Match bat, bats, hats, hats, but not rat or rats (use the hat symbol)
    -> [^r]ats?


# 3. Metacharacters and repetitions (메타문자와 반복)
- 더 큰 문자 집합을 매칭하는 더 쉬운 방법들이 있음

## 1. 종류
  - `\d`: 숫자 매칭 (ex: `9`)
  - `\D`: 숫자가 아닌 것을 매칭 (ex: `A` or `@`)
  - `\w`: 영숫자 문자를 매칭 (ex: `a` or `3`)
  - `\W`: 영숫자가 아닌 문자를 매칭 (ex: `!` or `#`)
  - `\s`: 공백 문자를 매칭 (스페이스, 탭, 줄바꿈)
  - `\S`: 그 외 모든 것을 매칭 (영숫자 문자와 기호)

- 밑줄 `_`은 `\w` 메타문자에 포함되며 `\W`에는 포함되지 않음
  -> 즉, `\w`는 `test_file`의 모든 단일 문자를 매칭함

- 종종 한 가지 타임의 많은 문자들이 연속으로 나타나는 패턴을 원할 때 반복을 사용하여 이를 해결할 수 있음
  - ex: z{2} = `zz` <- {2}는 앞의 문자 (또는 메타문자, 또는 문자 집합)를 연속으로 두 번 매칭하는 데 사용됨

  - 반복 표현 (앞의 패턴을 몇 번 매칭하는 지)
    - `{12}`: 정확히 12번
    - `{1,5}`: 1번에서 5번
    - `{2,}`: 2번 이상
    - `*`: 0번 이상 (반복이 안되도 되고, 1개여도 되고, 여러 개여도 됨)
    - `+`: 1번 이상

## Questions
  1. Match the following words: catssss
    -> cats{4}

  2. Match all of the following words (use the * sign): Cat, cats, catsss
    -> [Cc]ats*

  3. Match all of the following sentences (use the + sign): regex go br, regex go brrrrrr
    -> regex go br+

  4. Match all of the following filenames: ab0001, bb0000, abc1000, cba0110, c0000 (don't use a metacharacter)
    -> [abc]{1,3}[01]{4}

  5. Match all of the following filenames: File01, File2, file12, File20, File99
    -> `[Ff]ile\d{1,2}`

  6. Match all of the following folder names: kali tools, kali   tools
    -> `kali\s+tools`

  7. Match all of the following filenames: notes~, stuff@, gtfob#, lmaoo!
    -> `\w{5}\W`

  8. Match the string in quotes (use the * sign and the `\s`, `\S` metacharacters): "2f0h@f0j0%!a)K!F49h!FFOK"
    -> `\S*\s*\S*`

  9. Match every 9-character string (with letters, numbers, and symbols) that doesn't end in a "!" sign
    -> `\S{8}[^!]`

  10. Match all of these filenames (use the + symbol): .bash_rc, .unnecessarily_long_filename, and note1
    -> `\.?\w+`


# 4. Starts with/ ends with, groups, and either/ or (시작/끝, 그룹, 그리고 또는 (either / or))
- 줄의 시작이나 끝에서 특정 패턴으로 검색하고 싶을 때 다음의 문자들을 사용함
  `^`: 시작
  `$`: 끝

- `^`모자 기호는 `[ ]`대괄호 안에 있을 때는 문자 집합을 제외하는 데 사용하지만, 그렇지 않을 때는 단어의 시작을 지정하는 데 사용됨

- ex: `abc`로 시작하는 줄을 검색하고 싶다?
  -> `^abc`
- ex: `xyz`로 끝나는 줄을 검색하고 싶다?
  -> `xyz$`

- `either / or`패턴
  - `( )`소괄호로 묶어서 그룹을 정의하고 패턴을 반복하는 데 사용할 수 있음
  - `or`: `|`
  - ex: `during the (day|night)` = `during the day` & `during the night`
  - ex: `(no){5}` = `nonononono`

## Questions
  1. Match every string that starts with "Password:" followed by any 10 characters excluding "0", irrespective of the position.
    -> Password:[^0]{10}

  2. Match "username:" in the beginning of a line (note the space!)
    -> `^username:\s`

  3. Match every line that doesn't start sith a digit (use a metacharacter)
    -> `^\D`

  4. Match this string at the end of a line: EOF$
    -> `EOF\$$`

  5. Match all of the following sentences:
    - I use nano
    - I use vim
    -> I use (nano|vim)

  6. Match all lines that start with $, followed by any single digit, followed by $, followed by one or more non-whitespace characters
    -> `\$\d\$S+`

  7. Match every possible IPv4 address (use metacharacters and groups)
    -> `(\d{1,3}\.){3}\d{1,3}`

  8. Match all of these emails while also adding the username and the domain name (not the TLD) in separate groups (use `\w`): hello@tryhackme.com, username@domain.com, dummy_email@xyz.com
    -> `(\w+)@(\w+)\.com`
