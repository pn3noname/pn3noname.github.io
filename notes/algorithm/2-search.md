---
title: "Search Algorithms 101"
slug: "2-search"
date: "2026-02-18"
category: "Algorithm"
tags: ["Linear Search", "Binary Search", "Two Crystal Balls Problem", "Greedy Algorithm"]
description: "Covers linear search, binary search, and the Two Crystal Balls problem, along with an introduction to greedy algorithms. Includes pseudocode, implementation details, and complexity analysis for each approach."
---

source: https://frontendmasters.com/courses/algorithms/binary-search-algorithm/

# 1. Linear Search
## 1. 기본 개념
- 선형 검색은 가장 기본적인 검색 알고리즘
- 배열이나 리스트의 처음부터 끝까지 순차적으로 모든 요소를 확인하면서 원하는 값을 찾는 방식

## 2. 특징
- 구현이 매우 간단함
- 정렬되지 않은 데이터에서도 사용 가능
- 시간 복잡도: O(n) -> 최악의 경우 모든 요소를 확인해야 함
- 공간 복잡도: O(1) -> 추가 메모리가 거의 필요 없음

## 3. 동작 과정
### 1. 배열의 첫 번째 요소부터 시작
### 2. 현재 요소가 찾는 값인지 확인
### 3. 맞다면 해당 위치 반환, 아니면 다음 요소로 이동
### 4. 배열 끝까지 반복하며 값을 찾지 못하면 "찾을 수 없음" 반환


# 2. Binary Search
## 1. 기본 개념
- 이진 검색은 정렬된 배열에서 사용할 수 있는 효율적인 검색 알고리즘
- 중간 요소를 확인하고 찾는 값이 중간값보다 작은지 큰지에 따라 검색 범위를 절반으로 줄여나가는 방식

## 2. 특징
- 정렬된 데이터에서만 사용 가능
- 선형 검색보다 훨씬 빠름
- 시간 복잡도: O(log n) -> 매 단계마다 검색 범위가 절반으로 줄어듦
- 공간 복잡도: 반복적 구현 시 O(1), 재귀적 구현 시 O(log n)

## 3. 동작 과정
### 1. 배열의 중간 요소를 확인
### 2. 중간 요소가 찾는 값과 일치하면 해당 위치 반환
### 3. 찾는 값이 중간 요소보다 작으면 왼쪽 절반에서 검색 계속
### 4. 찾는 값이 중간 요소보다 크면 오른쪽 절반에서 검색 계속
### 5. 범위가 더 이상 없을 때까지 반복하고, 찾지 못하면 "찾을 수 없음" 반환

> [!INFO]
> # 두 알고리즘의 비교
> 예를 들어, 100만 개의 요소가 있는 배열에서 선형 검색은 최악의 경우 100만 번의 비교가 필요하지만, 이진 검색은 최대 약 20번의 비교만으로 찾을 수 있음
> 
> <img width="627" height="178" alt="image" src="https://github.com/user-attachments/assets/ab27def9-21c1-4ee6-85a9-d7b4e04999d6" />


## 4. 알고리즘 구현 방법
### 1. 주요 변수
- `lo`: 탐색 시작 지점 (포함)
- `hi`: 탐색 끝 지점 (미포함)
- `mid`: 중간 지점 인덱스
- `array`: 탐색할 정렬된 배열
- `needle`: 찾고자 하는 값

### 2. 의사코드 (Pseudocode)
```
function search(array, lo, hi, needle):
	do:
		mid = lo + (hi - lo) / 2     // 중간 지점 계산
		value = array[mid].          // 중간 지점의 값 가져오기

		if value == needle:          // 값을 찾았을 경우
			return true (또는 mid)
		else if value < needle:      // 찾는 값이 중간값보다 클 경우
			lo = mid + 1             // 오른쪽 부분 배열 탐색
		else:
			hi = mid                 // 왼쪽 부분 배열 탐색
		while lo < hi                // 탐색 범위가 유효할 때까지 반복

		return false (또는 -1)        // 값을 찾지 못했을 경우
```

### 3. 중요 포인트
#### 1. 항상 정렬된 배열에서만 사용해야 함
#### 2. `lo`는 포함 (inclusive), `hi`는 미포함 (exclusive)으로 처리함
#### 3. 종료 조건은 `lo < hi`가 아닐 때임 (탐색 범위가 없어질 때)
#### 4. 값을 찾지 못했을 경우, -1이나 false를 반환하는데, 이를 '센티넬 (sentinel) 값'이라고 부름


> [!INFO]
> # sentinel 값
> ## 사용 목적
> ### 1. 데이터 종료 표시
> - 데이터 스트림이나 배열, 리스트 등의 끝을 나타내기 위해 사용됨
> - 예: c언어에서 문자열의 끝을 나타내는 널 (NULL) 문자 ('\0')가 대표적인 센티넬 값
> ### 2. 특별한 상태 표시
> - 특정 함수나 알고리즘에서 특별한 상태나 조건을 나타내기 위해 사용됨
> - 일반적인 데이터 값과는 구분되는 특수한 값을 사용함
> ### 3. 오류 상태 표시
> - 함수가 실패했거나 비정상적인 상황이 발생했음을 나타내기 위해 사용됨
> - 예: 많은 함수에서 -1이나 NULL을 반환하여 오류를 표시함
>
> - 센티넬 값은 일반적으로 해당 데이터 타입에서 실제 데이터로는 거의 사용되지 않을 값을 선택함
> - 이는 일반 데이터와 센티넬 값 사이의 충돌을 방지하기 위함
> - 예:
> 	- 정수형 데이터에서 -1이나 최대값 (MAX_INT) 등을 센티넬 값으로 사용
> 	- 포인터에서는 NULL을 센티넬 값으로 사용
> 	- 문자열에서 특수 문자를 센티넬 값으로 사용
> - 센티넬 값은 알고리즘의 흐름을 제어하거나 특별한 케이스를 표시하는 데 매우 유용한 프로그래밍 기법

## 5. 이진 검색 구현
### 1. 기본 설정
- 함수는 'haystack (배열)'과 'needle (찾고자 하는 값)'을 매개변수로 받음
- 반복문으로 do-while 루프 사용 (다른 반복문도 사용 가능)
- 초기 변수 설정: lo=0 (시작점), hi=haystack.length (끝점)

### 2. 핵심 로직
- 중간점 (midpoint) 계산: `const m = Math.floor((lo + hi - l) / 2)`
  - warning! 2로 나누는 것을 잊지 말 것!
- 현재 중간값 가져오기: `const value = haystack[m]`
- 반복 조건: `while (lo < hi)`

### 3. 검색 조건 처리
- 중간값이 찾는 값과 같은 때: `value === needle`이면 `return true`로 찾았음을 반환
- 중간값이 찾는 값보다 클 때: `value > needle`이면 오른쪽 부분은 모두 큰 값이므로 `hi = m`으로 검색 범위 축소
- 중간값이 찾은 값보다 작을 때: 그 외의 경우 (else)에는 `lo = m + 1`로 왼쪽 부분 제외

> [!IMPORTANT]
> # `lo = m + 1`인 이유
> ## 1. 현재 중간값 `m`은 이미 확인했음: `value < needle`이므로 `m` 위치의 값은 우리가 찾는 값이 아님
> ## 2. 중간값보다 작은 모든 값들도 제외: 배열이 정렬되어 있으므로, `m`보다 왼쪽에 있는 모든 값들 (`lo`부터 `m`까지)은 우리가 찾는 값보다 작음
> ## 3. lo는 inclusive이므로: 다음 검색 범위에서 `m+1`부터 시작해야 함
> - 만약 `lo = m`으로 설정하면, 다음 반복에서 또 같은 `m` 값을 확인하게 되어 무한루프 위험
> 
> 예:
> ```
> 배열: [1, 3, 5, 7, 9], needle = 7
> lo = 0, hi = 5, m = 2, value = 5
> 5 < 7이므로 오른쪽 절반을 검색해야 함
> lo = m + 1 = 3 (인덱스 3부터 시작 = 값 7부터)
> ```
> 
> 반대로 `hi = m`에서는 +1을 하지 않는 이유:
> - hi는 exclusive이므로 `m`을 포함하지 않음
> - 이미 `m`을 제외한 범위가 됨
> 
> 위의 내용이 이진 검색에서 흔히 발생하는 "off-by-one error"를 피하는 핵심

> [!INFO]
> # Off-by-one error
> - 프로그래밍에서 가장 흔한 실수 중 하나로, 인덱스나 카운터를 1만큼 잘못 계산하는 오류
> - 정확하게 처리하지 않으면 무한루프나 잘못된 결과를 만들어내는 까다로운 버그
> 
> ## 1. 배열 인덱스 실수
> ```javascript
> // 잘못된 예: off-by-one error
> const arr = [1, 2, 3, 4, 5];
> for (let i = 1; i <= arr.length; i++) { // 1부터 시작, <= 사용
> 	console.log(arr[i]); // 2, 3, 4, 5, undefined (마지막에 오류)
> }
> 
> // 올바른 예
> for (let i = 0; i < arr.length; i++) { // 0부터 시작, < 사용
> 	console.log(arr[i]); // 1, 2, 3, 4, 5
> }
> ```
> 
> ## 2. 이진 검색에서의 off-by-one error
> ```javascript
> // 문제가 될 수 있는 경우들
> lo = m;                      // m을 다시 포함시켜 무한루프 위험
> hi = m + 1;                // 경계를 잘못 설정
> ```
> 
> ## 3. 일상적인 예시들
> - 문자열 길이: "Hello"의 길이는 5이지만, 마지막 문자의 인덱스는 4
> - 반복문 범위: 10번 반복하려면 `i < 10`이어야 하는데, `i <= 10`으로 써서 11번 반복
> - 날짜 계산: 1월 1일부터 1월 5일까지는 5일이 아니라 4일 차이
> 
> ## 4. 왜 이진 검색에서 중요한가?
> ```javascript
> // 만약 lo = m으로 했다면
> lo = 0, hi = 2, m = 1
> lo = m = 1           // 다음에 또 m = 1이 나올 수 있음 -> 무한루프
> 
> // lo = m + 1로 하면
> lo = m + 1 = 2     // 확실히 범위가 줄어듦
> ```

### 4. 코드
```javascript
// haystack: number[]
// needle: number

let lo = 0;
let hi = haystack.length - 1;

while (lo <= hi) {
	let m = Math.floor((lo + hi) / 2);

	if (needle === haystack[m]) {
		return true;
	}
	else if (needle < haystack[m]) {
		hi = m - 1;
	}
	else {
		lo = m + 1;
	}
	return false;
}
```

# 3. Two Crystal Balls Problem
## 1. 문제 설명
- 특정 높이에서 떨어뜨리면 깨지는 두 개의 수정구슬
- 이 구슬들이 정확히 어느 지점에서 깨지는지를 가장 효율적인 방법으로 찾아야 함
- 예: 100층 건물에서 몇 층부터 구슬이 깨지는지 찾는 문제

## 2. 문제의 본질 (일반화)
- 거짓 (false)들로 가득한 배열이 있고
- 어느 지점부터는 참 (true)이 되어 계속 참을 유지
- 이 전환점을 찾는 것이 목표

## 3. 기존 접근법들의 한계
### 1. 선형 탐색 (Linear Search)
- 처음부터 하나씩 확인
- 시간복잡도: O(N)
- 두 번째 구슬을 전혀 활용하지 못함

### 2. 이진 탐색 (Binary Search)
- 중간 지점부터 시작
- 만약 중간에서 깨진다면? -> 구슬 하나 소모
- 나머지 구슬로는 처음부터 선형 탐색 해야 함
- 결국 최악의 경우 O(N)

## 4. 최적해: √N 접근법
- 제곱근 단위로 점프하기

### 1. 알고리즘 과정
#### 1. √N만큼 점프하면서 첫 번째 구슬로 테스트
#### 2. 구슬이 깨질 때까지 계속 점프
#### 3. 깨지면 마지막으로 안전했던 지점으로 돌아가기
#### 4. 두 번재 구슬로 선형적으로 탐색 (최대 √N 거리)

### 2. 시간복잡도 분석
- 점프 횟수: 최대 √N번
- 선형 탐색: 최대 √N번
- 총 시간복잡도: √N + √N = 2√N = O(√N)

### 3. 핵심 아이디어
- 기존 이진 탐색이 N/2 단위로 점프하여 문제가 생겼다면, √N 단위로 점프함으로써 두 구슬을 모두 효과적으로 활용할 수 있게 됨
- 이는 선형 탐색 O(N)보다 훨씬 효율적이면서도, 제약 조건 (구슬 2개)을 잘 활용한 창의적인 해결책


> [!QUESTION]
> # 수정구슬이 하나만 있어도 같은 알고리즘이 작동하지 않을까?
> ## 1. 수정구슬이 하나만 있을 때의 문제점
> - 수정구슬이 하나뿐이라면, 유일한 방법은 선형 탐색 (Linear Search)
> - 1층부터 차례대로 올라가면서 테스트
> - 구슬이 깨질 때까지 한 층씩 확인
> - 시간복잡도: O(N) -> 매우 비효율적
> ## 2. 왜 √N 알고리즘에는 두 개가 필요한가?
> - √N 알고리즘이 작동하는 핵심은 두 단계 과정
> ### 1. 1단계: 첫 번째 구슬로 √N씩 점프
> - √N 간격으로 큰 점프를 하며 테스트
> - 구슬이 깨질 때까지 여러 층을 건너뛰기
> ### 2. 2단계: 두 번째 구슬로 정확한 지점 찾기
> - 첫 번째 구슬이 깨진 후
> - 마지막 안전한 층으로 돌아가서
> - 두 번째 구슬로 선형 탐색 (최대 √N 범위)
>
> ## 3. 핵심 포인트
> - √N만큼 점프한다는 것은 특정 수의 층을 건너뛴다 (skipping)는 의미
> - 수정구슬 중 하나가 깨지면, 목표 층이 마지막 '안전한' 층과 현재 층 사이 어딘가에 있다는 것을 알 수 있음
> - 그래서 그 안전한 층부터 선형 탐색을 통해 목표 층을 찾는 것
> ## 4. 결론
> - 구슬 1개: 처음부터 끝까지 선형 탐색만 가능 -> O(N)
> - 구슬 2개: 점프 + 정밀 탐색의 조합 가능 -> O(√N)
> - 두 번째 구슬이 있기 때문에 실험적으로 큰 점프를 시도할 수 있고, 실패해도 다시 정밀하게 찾기가 가능한 것임

## 5. Crystal Ball Problem 알고리즘 구현
### 1. 문제 개요
- 높은 건물에서 수정구를 떨어뜨릴 때, 어느 층부터 깨지는지 찾는 문제
- 배열로 표현: `[false, false, false, true, true, ture]` (false=안 깨짐, true=깨짐)
- 목표: 수정구가 처음으로 깨지는 층 (인덱스)을 찾기

### 2. 왜 이진 탐색이 안 되는가?
- 이진 탐색으로 중간 지점에서 수정구를 떨어뜨렸는데 깨졌다면?
- 남은 수정구가 1개 뿐이므로, 처음부터 그 지점까지 선형적으로 하나씩 확인해야 함
- 결국 최악의 경우 N/2만큼 확인해야 하므로 여전히 선형 시간

### 3. 해결책: √N 점프 알고리즘
#### 1. 핵심 아이디어
##### 1. 첫 번째 수정구: √N만큼 점프하면서 깨지는 지점 찾기
##### 2. 두 번째 수정구: 깨진 지점에서 √N만큼 뒤로 돌아가서 선형 탐색

#### 2. 알고리즘 단계 (코드)
```javascript
export default function two_crystal_balls(breaks: boolean[]): number {
	// breaks 배열의 의미
	// breaks[i] = true: i층에서 크리스탈 볼이 깨짐
	// breaks[i] = false: i층에서 크리스탈 볼이 안전함

	const jmpAmount = Math.floor(Math.sqrt(breaks.length));

	let i = jmpAmount;
	for (; i < breaks.length; i += jmpAmount) {
		if (breaks[i]) { // breaks[i]가 true라면 (= if (breaks[i] === true))
			break;
		}
	}

	i -= jmpAmount; // 마지막으로 안전했던 층으로 돌아감

	// 안전했던 층부터 시작해서 한 층씩 올라가며 탐색
	for (let j = 0; j <- jmpAmount && i < breaks.length; ++j, ++i) {
		if (breaks[i]) {
			return i;
		}
	}
	return -1;
}
```

### 4. 시간 복잡도 분석
#### 1. 최악의 경우
##### 1. 첫 번째 단계: √N번 점프
##### 2. 두 번째 단계: √N번 선형 탐색
##### 3. 총 시간 복잡도: O(√N + √N) = O(√N)

#### 2. 왜 √N이 최적인가?
- √N보다 작게 점프하면: 점프 횟수가 증가
- √N보다 크게 점프하면: 선형 탐색 구간이 증가
- √N이 두 구간의 균형점

### 5. 다른 루트 값들과의 비교
- 세제곱근(∛N): 점프 거리는 줄어들지만 점프 횟수가 증가하여 비효율적
- 네제곱근이나 더 높은 루트: 선형 탐색에 가까워져서 비효율적
- √N이 최적의 균형점

### 6. 핵심 포인트
#### 1. 이진 탐색은 수정구 문제에서 선형 시간이 됨
#### 2. √N 점프로 O(√N) 시간 복잡도 달성
#### 3. 첫 번째 수정구로 대략적 위치 파악, 두 번째로 정확한 위치 찾기
#### 4. √N이 점프 거리와 선형 탐색 거리의 최적 균형점


> [!INFO]
> # 탐욕적 접근법 (Greedy Algorithm)
> - 매 순간 가장 좋아 보이는 선택을 하는 알고리즘 설계 기법
> ## 1. 탐욕적 접근법의 특징
> ### 1. 핵심 원리
> - 현재 상황에서 최선의 선택을 함
> - 미래의 결과를 고려하지 않음
> - 지역적 최적해 (local optimum)를 선택해서 전역적 최적해 (global optimum)를 찾으려 함
> ### 2. 일반적인 절차
> #### 1. 선택: 현재 상황에서 최선의 선택을 한다
> #### 2. 적용: 선택한 것을 현재 해에 추가한다
> #### 3. 확인: 문제가 해결되었는지 확인한다
> #### 4. 반복: 해결되지 않았다면 1단계로 돌아간다
> 	
> ## 2. 대표적인 예시들
> ### 거스름돈 문제
> ```typescript
> // 730원을 거슬러 줄 때 (동전: 500원, 100원, 50원, 10원)
> function makeChange (amount: number): number[] {
> 	const coin = [500, 100, 50, 10];
> 	const result = [];
> 	amount = 730;
> 	
> 	for (const coin of coins) {
> 		while (amount >= coin) {
> 			result.push(coin); // 사용한 동전을 배열의 끝에 추가
> 			amount -= coin; // 탐욕적 선택: 가장 큰 동전부터
> 		}
> 	}
> 	return result; // [500, 100, 100, 10, 10, 10]
> }
> ```
> ### 활동 선택 문제
> #### 1. 시각적 표현
> 시간:  0   1   2   3   4   5   6   7   8   9
> 활동A:        [----A----]
> 활동B:             [--B--]                        (A와 겹침 - 제외)
> 활동C:   [--------C--------]             (A,D와 겹침 - 제외)
> 활동D:                        [--D--]             (선택)
> 활동E:                                   [E]          (선택)
> 활동F:                         [----F----]      (D,E와 겹침 - 제외)
> 선택됨:        [----A----]  [--D--]  [E]
> #### 2. 문제 상황
> - 한 개의 강의실이 있고, 여러 활동들이 각각 시작 시간과 끝나는 시간을 가지고 있음
> - 겹치지 않으면서 최대한 많은 활동을 선택해야 함
> #### 3. 구체적인 예시
> ```typescript
> const activities = [
> 	{ name: 'A', start: 1, end: 4 }, // 1시~4시 
> 	{ name: 'B', start: 3, end: 5 }, // 3시~5시 
> 	{ name: 'C', start: 0, end: 6 }, // 0시~6시 
> 	{ name: 'D', start: 5, end: 7 }, // 5시~7시 
> 	{ name: 'E', start: 8, end: 9 }, // 8시~9시 
> 	{ name: 'F', start: 5, end: 9 } // 5시~9시
> ];
> ```
> #### 4. 알고리즘 단계별 실행
> ##### 1. 끝나는 시간 순으로 정렬
> ```typescript
> activities.sort((a, b) => a.end - b.end);
> ```
>
> 정렬 후:
> ```typescript
> const activities = [
> 	{ name: 'A', start: 1, end: 4 }, // 4시 끝
> 	{ name: 'B', start: 3, end: 5 }, // 5시 끝
> 	{ name: 'C', start: 0, end: 6 }, // 6시 끝
> 	{ name: 'D', start: 5, end: 7 }, // 7시 끝 
> 	{ name: 'E', start: 8, end: 9 }, // 9시 끝
> 	{ name: 'F', start: 5, end: 9 } // 9시 끝
> ];
> ```
> ##### 2. 탐욕적 선택 과정
> ```typescript
>	function activitySelection(activities) { 
>		activities.sort((a, b) => a.end - b.end); 
>		const result = [activities[0]]; // 첫 번째 활동은 무조건 선택 
>		let lastEnd = activities[0].end; 
>		for (let i = 1; i < activities.length; i++) { 
>			if (activities[i].start >= lastEnd) { 
>				result.push(activities[i]); 
>				lastEnd = activities[i].end; 
>			} 
>		} 
>		return result; 
>	}
> ```
> 
> ![[Pasted image 20250601170931.png]]
> ![[Pasted image 20250601170954.png]]
> 
> ```typescript
> 	// 가장 많은 활동을 선택하기
> 	function activitySelection (activities: {start: number, end: number} [] ) {
> 		activities.sort((a, b) => a.end - b.end); // 끝나는 시간 순 정렬
> 		
> 		const result = [activities[0]]; // 첫 번재 활동은 무조건 선택
> 		let lastEnd = activities[0].end;
> 		
> 		for (let i = 1; i < activities.length; i++) {
> 			if (activities[i].start >= lastEnd) { // 탐욕적 선택: 가장 빨리 끝나는 것
> 				result.push(activities[i]);
> 				lastEnd = activities[i].end;
> 			}
> 		}
> 		return result;
> 	}
> ```

#### 3. Two Crystal Balls에서의 탐욕적 접근
##### 탐욕적 선택들:
1. √n 간격으로 점프: 가장 효율적인 간격
2. 깨지면 즉시 중단: 불필요한 테스트 피하기
3. 이전 안전 지점부터 선형 탐색: 확실한 구간에서만 탐색
##### 각 단계에서의 "탐욕적" 판단:
1. 1단계: "지금 당장 가장 빠르게 구간을 좁힐 수 있는 방법은?"
2. 2단계: "남은 볼 1개로 가장 확실하게 찾을 수 있는 방법은?"

#### 4. 탐욕법의 장단점
##### 1. 장점
- 구현이 간단
- 속도가 빠름
- 직관적으로 이해하기 쉬움
##### 2. 단점
- 항상 최적해를 보장하지 않음
- 문제에 따라 적용 불가능
##### 3. 탐욕법이 최적해를 보장하는 조건
1. 탐욕적 선택 속성: 지역적 최적 선택이 전역적 최적해로 이어짐
2. 최적 부분 구조: 문제의 최적해가 부분 문제의 최적해를 포함
##### 4. Two Crystal Balls 문제에서 탐욕법을 쓰는 이유는 √n 간격이 수학적으로 최적이라는 것이 증명되어있기 때문

#### 5. 다른 접근법과의 비교
<img width="535" height="145" alt="image" src="https://github.com/user-attachments/assets/6098f89b-294e-4ff4-9008-3030188e221a" />
