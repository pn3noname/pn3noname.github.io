---
title: "Core Data Structures & Sorting Algorithms"
slug: "3-sort"
date: "2026-02-19"
category: "Algorithm"
tags: ["Bubble Sort", "Linked List", "Queue", "Stack", "Big O"]
description: "A deep dive into Bubble Sort, Linked Lists, Queues, and Stacks — exploring how pointer manipulation enables O(1) operations, when linked lists outperform arrays, and how these foundational structures power real-world systems like video decoders and call stacks."
---

source: https://frontendmasters.com/courses/algorithms/bubble-sort/

# 1. Bubble Sort
## 1. 버블 정렬을 선택한 이유
- 일반적인 알고리즘 책에서 삽입 정렬로 시작하는 것과 달리, 버블 정렬부터 설명하는 이유
	- 삽입 정렬의 문제점: 카드 덱 예제가 이해하기 어려움
	- 버블 정렬의 장점:
		1. 시각적으로 이해하기 매우 쉬움
		2. 단 3줄의 코드로 구현 가능
		3. 극도로 간단한 알고리즘

## 2. 버블 정렬의 특징
- 매우 간단한 정렬 알고리즘으로 구현이 쉬움
- 제자리 정렬 (in-place sorting): 추가 메모리 공간을 거의 사용하지 않음
- 이진 탐색보다도 구현이 간단함
- 성능상의 한계
	- 불변 배열 (immutable array)에서 사용하면 성능이 매우 나빠짐
	- 역순으로 정렬된 배열의 경우 최악의 성능을 보임
	- 실제 개발에서는 거의 사용되지 않는 비효율적인 알고리즘

## ​3. 정렬된 배열의 정의
- 수학적으로 정렬된 배열의 정의:
	- 배열의 모든 i번째 위치에서 `x[i] ≤ x[i+1]`이 성립해야 함
	- 이 조건이 전체 배열에 대해 성립해야 정렬된 것

## 4. 버블 정렬 알고리즘 동작 원리
- 예시 배열: `[1, 3, 7, 4, 2]`
- 핵심 원리:
	- 0번째 위치부터 시작해서 배열 끝까지 진행
	- 각 위치에서 다음 요소와 비교
	- 현재 요소가 다음 요소보다 크면 위치를 교환
- 1회 반복 과정:
	1. 1과 3 비교 -> 교환 안함
	2. 3과 7 비교 -> 교환 안함
	3. 7과 4 비교 -> 7 > 4이므로 교환 -> `[1, 3, 4, 7, 2]`
	4. 7과 2 비교 -> 7 > 2이므로 교환 -> `[1, 3, 4, 2, 7]`
- 결과: 1회 반복 후 가장 큰 값 (7)이 마지막 위치에 배치됨
- 2회 반복 과정: 마지막 위치는 이미 정렬되었으므로 제외하고 진행
- 3회 반복 과정: 뒤의 두 위치는 제외하고 진행
- 이런 식으로 검사할 범위가 점점 줄어듦
- 한 개 요소만 남을 때까지 반복 (한 개 요소는 항상 정렬된 상태)
- 코드
```typescript
export default function bubble_sort(arr: number[]): void {
	for (let i = 0; i < arr.length; i++) {
		for (let j = 0; j < arr.length - 1 - i; j++) {
			if (arr[j] > arr[j + 1]) {
				const temp = arr[j];
				arr[j] = arr[j + 1];
				arr[j + 1] = temp;
			}
		}
	}
}
```

## 5. 시간 복잡도 분석
- 반복 횟수:
	- 1회차: n번 비교
	- 2회차: n-1번 비교
	- 3회차: n-2번 비교
	- ...
	- 마지막: 1번 비교
- 가우스의 일화를 통한 설명:
	- 1부터 100까지 더하는 문제를 가우스가 10초 만에 해결
	- 방법: 1+100=101, 2+99=101, ..., 50+51=101
	- 총 50개의 101 -> 101x50 = 5050
	- 일반화: `n(n+1)/2`
- 시간 복잡도 계산:
	- 총 비교 횟수: `n + (n-1) + (n-2) + ... + 1 = n(n+1)/2`
	- 전개: `(n² + n)/2`
	- 상수 제거: n² + n
	- 최고차항만 고려: O(n²)
- n이 커질수록 n²항이 지배적이 되어 n항은 무시할 수 있게 됨
- 버블 정렬은 구현이 매우 간단하지만 O(n²)의 시간 복잡도를 가져 큰 데이터셋에는 비효율적인 알고리즘

# 2. Linked List Data Structures
## 1. 배열의 한계점
### JavaScript 배열의 특성
- JavaScript의 배열은 사실 진정한 배열이 아님
- `push()`, 삽입, 삭제 등이 가능하고 인덱스가 자동으로 조절됨
- 실제 배열 위에 추가적인 구조가 존재

### 전통적인 배열의 문제점
- 삭제: 실제로 삭제할 수 없고 0으로 만들 뿐
- 삽입: 실제 삽입이 불가능
- 크기 고정: 배열은 크기가 고정되어 있음

## 2. 연결 리스트란?
### 기본 개념
- 첫 번째 진짜 자료구조로 간주
- 노드 기반 자료구조 (Node-based data structure)
- 연결 리스트에는 index가 없음
- 각 노드는 데이터를 감싸는 컨테이너 역할

### 노드 구조
```typescript
type Node<T> = {
	value: T;       // 실제 데이터
	next?: Node<T>;
}
```

### 동작 원리
- 각 노드가 값과 다음 노드에 대한 참조를 가짐
- 체인처럼 연결된 구조
- 헤드 (head)부터 시작해서 순차적으로 접근

## 3. 단일 연결 리스트 vs 이중 연결 리스트
### 단일 연결 리스트 (Singly Linked List)
- 각 노드가 다음 노드만 참조
- A -> B -> C -> D
- 한 방향으로만 이동 가능
- 뒤로 돌아갈 수 없음

### 이중 연결 리스트 (Doubly Linked List)
- 각 노드가 이전 노드와 다음 노드 모두 참조
- A ⇄ B ⇄ C ⇄ D
- 양방향 이동 가능
- `previous`와 `next` 속성 보유

## 4. 연결 리스트의 주요 연산
### 삽입 (Insertion): O(1)
- A와 B 사이에 F를 삽입하는 경우:
	1. A의 next를 F로 설정
	2. F의 next를 B로 설정
	3. B의 previous를 F로 설정
	4. F의 previous를 A로 설정
- 시간 복잡도: O(1) - 상수 시간

### 삭제 (Deletion): O(1)
- C 노드를 삭제하는 경우( = C.prev & B.next = C.next):
	1. B의 next를 D로 설정 (C.next)
	2. D의 previous를 B로 설정 (C.previous)
	3. C의 next와 previous를 null로 설정 (C.prev = C.next = null)
	4. C의 값을 반환 (ret C.val)
- 시간 복잡도: O(1) - 상수 시간

## 5. 연결 리스트의 장점
### 효율적인 삽입 / 삭제
- 배열과 달리 요소를 이동시킬 필요 없음
- 링크만 조정하면 되므로 O(1) 시간
- 입력 크기와 무관하게 일정한 시간

### 동적 크기
- 필요에 따라 크기 조정 가능
- 메모리를 효율적으로 사용

## 6. 연결 리스트의 단점
### 인덱스 접근 불가
- 배열처럼 `arr[i]`로 직접 접근 불가
- n번째 요소에 접근하려면 처음부터 순차적으로 이동해야 함
- 접근 시간: O(n)

### 메모리 오버헤드
- 각 노드마다 포인터를 위한 추가 메모리 필요
- 힙 (heap) 메모리 사용으로 스택보다 비용 증가

## 7. 구현 시 주의사항
### 연산 순서의 중요성
- 링크를 끊기 전에 새로운 연결을 먼저 설정
- 잘못된 순서로 하면 노드에 접근할 수 없게 됨

### 경계 조건 처리
- null 체크, undefined 체크 필요
- 첫 번째나 마지막 노드 처리 시 특별한 주의

## 8. 핵심 개념 정리
- 연결 리스트는 메모리를 직접 할당하고 관리하는 첫 번째 자료구조로, 포인터를 통해 메모리를 순회하는 방식을 배울 수 있는 중요한 개념
- 배열의 고정된 한계를 극복하고 동적인 자료 관리를 가능하게 해주는 핵심적인 자료구조


> [!INFO]
> # 연결 리스트의 삽입과 삭제의 시간 복잡도가 O(1)일 때의 중요한 전제 조건
> ## 핵심 포인트: "어디에" 삽입 / 삭제 하는지가 중요함
> ### 1. O(1)인 경우: 위치를 이미 알고 있을 때
> 	기존: A -> B -> C -> D
> 	
> 	B와 C 사이에 X를 삽입하고 싶은데, 이미 B 노드의 참조 (포인터)를 가지고 있다면:
> 	
> 	1. X.next = B.next (X가 C를 가리키게)
> 	2. B.next = X (B가 X를 가리키게)
> 	
> 	A -> B -> X -> C -> D
> - 왜 O(1)인가?
> 	- 포인터 2개만 바꾸면 끝
> 	- 데이터를 이동시킬 필요 없음
> 	- 노드를 찾아 헤매지 않음 (이미 위치를 알고 있으므로)
> ### 2. O(n)인 경우: 위치를 찾아야 할 때
> 	"3번째 위치에 삽입해줘"라고 하면:
> 	
> 	1. head부터 시작해서 1 -> 2 -> 3 순차 탑색 (O(n))
> 	2. 찾은 후 삽입 (O(1))
> 	3. 총 시간 복잡도: O(n)
> 	
> ### 3. 배열과의 비교
> 	배열의 중간 삽입:
> 	[A, B, C, D]에서 B 뒤에 X 삽입
> 	
> 	4. C와 D를 한 칸씩 뒤로 밀어야 함
> 	5. [A, B, _ , C, D] -> [A, B, X, C, D]
> 	6. 시간 복잡도: O(n) (데이터 이동 때문에)
> 	
> 	연결 리스트의 삽입 (위치를 안다면):
> 	포인터만 바꾸면 끝 -> O(1)
> 	
> ### 실제로는 ...
> 	대부분의 경우 "어디에 삽입할지" 먼저 찾아야 하므로:
> 	- 찾기: O(n)
> 	- 삽입: O(1)
> 	- 전체: O(n)
> 	하지만 head나 tail에 삽입하거나, 이미 노드 찹조를 가지고 있는 경우에는 O(1)


# 3. Linked List Complexity
## 1. 기본 연산들
- 만약 다섯 번째 값을 요청한다면, 이런 구조에서는 다섯 번째 값을 바로 가져올 방법이 없음
- 문자 그대로 0부터 5까지의 루프를 작성해야 하고, `current = current.next`와 같은 방식으로 올바른 값에 도달할 때까지 순회해야 함
- 중요한 점
	- 포함하는 노드 (containing node) 자체를 반환해서는 안 됨
	- 그럴 경우, 내부 구조가 노출되어 누군가에게 next와 previous 값을 조작할 수 있고, 그러면 전체 리스트가 망가짐
	- 이는 실용적인 구현 관점에서 중요함
	- 포함하는 노드는 우리는 위한 추상화일 뿐, 외부 세계를 위한 것이 아님

## 2. 시간 복잡도 분석
### 헤드 (Head)와 테일 (Tail) 접근
- 헤드와 테일 가져오기: 상수 시간 (O(1)) 연산
- 연결 리스트 구현이 첫 번째 항목을 가리키는 단일 참조 (head)를 가지고 있다면, 리스트의 크기에 관계없이 헤드 가져오기는 상수 연산이 됨
- 테일에 대해서도 이미 정의된 포인터가 있기 때문에 상수 연산이 가능함

### 삭제 (Deletion) 연산
- 앞이나 뒤에서의 삭제: 상수 시간 연산
- 삭제 알고리즘만 적용하면 됨
- 중간에서의 삭제: 해당 지점까지 순회해야 하므로 비용이 큼
- 두 가지 연산 비용이 있음: 순회 + 삭제
- 양 끝에서의 삭제는 상수 시간이지만, 중간에서의 삭제는 순회가 비싸면 비용이 큼
- 삭제 자체는 비용이 크지 않음

### 삽입 (Insertion) 연산
- 앞에 추가 (Prepending)와 뒤에 추가 (Appending): 상수 시간
- head나 tail에서 링크만 끊으면 되므로 매우 빠름
- 중간 삽입: 다시 순회가 문제
- 빠르게 순회할 수 있다면 삽입도 빠름

## 3. 연결 리스트의 장단점
### 장점
- 원하는 크기로 만들 수 있음
- 앞이나 뒤에서의 삭제가 극도로 빠름
- 이 장점이 매우 중요함. 많은 구조에서 "가장 오래된 항목을 삭제"하고 싶을 때가 있는데, 가장 오래된 항목이 테일에 정리되어 있으면 상수 연산으로 매우 빠르게 처리 가능

### 단점
- 좀 더 복잡함
- 연속적인 메모리가 아님
- 연속적인 메모리에 대한 컴퓨터 최적화들이 있지만, 중요한 것은 이런 것들을 저장할 수 있다는 점임

## 4. 연결 리스트의 중요성
- 모든 연결 리스트는 그래프
- 모든 연결 리스트는 기술적으로 트리
- 연결 리스트는 가장 기본적인 단위로써, 연결 리스트에서 순회하고 움직이는 방법을 이해한다면, 다른 모든 데이터 구조들을 이해할 수 있음 (다른 복잡한 데이터 구조들 (그래프, 트리)의 기반이 됨)

# 4. Queue
## 1. 자료구조 vs 알고리즘의 구분
- 자료구조와 알고리즘의 구분이 모호할 수 있음
- 연결 리스트의 경우, 실제 구조 자체는 자료구조이지만, 삽입 과정은 알고리즘적 측면이 있음

## 2. Queue의 정의와 특징
- 큐는 연결 리스트 위에 구현된 특별한 자료구조
- FIFO (First In First Out) 구조
- 영국에서는 "queue"라고 부르고, 미국에서는 "line"이라고 부름 (줄서기와 같은 개념)

## 3. Queue의 구현 방식
### 기본 구조
- Head: 큐의 앞쪽 (데이터가 나가는 곳)
- Tail: 큐의 뒤쪽 (데이터가 들어가는 곳)
- 단일 연결 리스트로 충분함 (이중 연결 리스트 불필요)
### 삽입 (Enqueue) 연산
```typescript
this.tail.next = newNode;
this.tail = newNode;
```
- 새로운 요소를 꼬리 (tail) 뒤에 추가
- 꼬리 포인터를 새로운 노드로 업데이트
### 제거 (Dequeue) 연산
```typescript
const oldHead = head;
head = head.next;  // head를 A -> B로 이동
oldHead.next = null;  // A를 없애줌
return oldHead.value;
```
- 머리 (head)에서 요소를 제거
- 머리 포인터를 다음 노드로 이동
- 제거된 노드의 값을 반환
### Peek 연산
```typescript
return head.value;
```
- 큐의 첫 번째 요소를 제거하지 않고 확인

> [!INFO]
> # PEEK 연산의 개념
>  - Peek 연산은 자료구조에서 매우 중요한 개념으로, "엿보기" 또는 "미리 보기"라는 의미
> ## 1. 기본 정의
>  - Peek은 자료구조의 다음에 처리될 요소를 제거하지 않고 단순히 확인만 하는 연산
>  - 큐에서의 Peek
>  ```typescript
>  // 큐에서 peek 연산
>  peek(): T {
> 	 return this.head.value;  // 제거하지 않고 값만 반환
>  }
>  ```
>
>  - 큐의 맨 앞 (head)에 있는 요소를 확인
>  - 요소를 제거하지 않음
>  - 큐의 상태는 그대로 유지
> ## 2. Peek vs Dequeue 비교
> <img width="677" height="100" alt="image" src="https://github.com/user-attachments/assets/708d2602-6bc8-41b4-8b54-3b1bfc127ee1"/>
>
> ## 3. 성능 특성
>  - 시간 복잡도: O(1) - 상수 시간
>  - 공간 복잡도: O(1) - 추가 메모리 사용 없음
> ## 4. 핵심 포인트
>  - Peek 연산의 가장 중요한 특징은 "Look but don't touch" 원칙
>  - 즉, 데이터를 확인은 하지만 자료구조의 상태를 변경하지 않아서, 나중에 다시 같은 요소에 접근할 수 있음
>  - 이는 조건부 처리나 미리 확인이 필요한 알고리즘에서 매우 유용함

## 4. 성능 특성
- 삽입 (Enqueue): O(1) - 상수 시간
- 제거 (Dequeue): O(1) - 상수 시간
- Peek: O(1) - 상수 시간
- 모든 연산이 리스트를 순회하지 않고 포인터만 조작하므로 매우 효율적임

## 5. 실용적 활용 사례
- 비디오 디코더에서 비디오 데이터를 올바른 순서로 버퍼링하기 위해 큐를 사용할 수 있음
- 비디오 디코더에서 큐를 사용하는 이유
	- 순서가 중요한 데이터를 처리할 때
	- 들어온 순서대로 처리해야 할 때
	- 실시간성이 중요할 때
	- 효율적인 버퍼링이 필요할 때
- 비디오는 시간 순서가 절대적으로 중요한 데이터이기 때문에, FIFO 방식의 큐가 가장 적합한 자료구조

## 6. 핵심 개념
- 큐는 제약을 가함으로써 성능을 최적화한 자료구조
- 일반적인 연결 리스트의 기능을 제한하여 특정 용도 (FIFO)에 최적화된 매우 빠른 자료구조를 만든 것

## 7. Implementing a Queue
### Queue의 기본 개념
- Queue는 FIFO 방식으로 동작하는 자료구조
- Queue가 비교적 간단한 자료구조이며, 하나의 링크만 관리하면 되므로 구현이 어렵지 않음
- 주요 메서드: enqueue (추가), dequeue (제거), peek (조회)

### 구현 단계
1. 기본 타입 정의
```typescript
type QueueNode<T> = {
	value: T;
	next?: QueueNode<T>;
}

class Queue<T> {
	private head?: QueueNode<T>;
	private tail?: QueueNode<T>;
	public length: number;
}
```

2. 생성자
```typescript
constructor() {
this.head = this.tail = undefined;
this.length = 0;
}
```

3. peek() 메서드
- 큐의 맨 앞 요소를 반환 (제거하지 않음)
- `return this.head?.value;` 형태로 구현

4. dequeue() 메서드 (제거)
- 큐의 맨 앞 요소를 제거하고 반환
- head가 없으면 undefined 반환
- head를 다음 노드로 업데이트
- length 감소

5. enqueue() 메서드 (추가)
- 큐의 맨 뒤에 새 요소 추가
- 두 가지 경우 처리:
	- 빈 큐의 경우: head와 tail을 새 노드로 설정
	- 기존 요소가 있는 경우: tail의 next를 새 노드로 연결하고 tail 업데이트

### 핵심 포인트
#### 메모리 관리
- JavaScript의 가비지 컬렉터 덕분에 수동 메모리 해제가 불필요
- 다른 언어에서는 free() 같은 메모리 해제 작업이 필요

#### 제네릭 확용
- `<T>` 제네릭을 사용하여 어떤 타입의 데이터든 저장 가능
- 타입 안전성 보장

#### 연결 리스트 구조
- 각 노드가 다음 노드를 가리키는 단방향 연결 리스트
- head와 tail 포인터로 효율적인 삽입 / 삭제 가능

### 코드
```typescript
type Node<T> = {
	value: T;
	next?: Node<T>,
}

export default class Queue<T> {
	public length: number;
	private head?: Node<T>;
	private tail?: Node<T>;

	constructor() {
		this.head = this.tail = undefined;
		this.length = 0;
	}
	
	enqueue(item: T): void {
		const node = {value: item} as Node<T>;
		this.length++;
		if (!this.tail) {
			this.tail = this.head = node;
			return;
		}
		this.tail.next = node;
		this.tail = node;
	}

	deque(): T | undefined {
		if (!this.head) {
			return undefined;
		}
		this.length--;

		const head = this.head;
		this.head = this.head.next;

		// free
		head.next = undefined;

		// 큐가 비어있을 때 tail을 undefined로 설정
		if (this.length === 0) {
			this.tail = undefined;
		}

		return head.value;
	}

	peek(): T | undefined {
		return this.head?.value;
	}
}
```
- 큐의 dequeue 연산 구현
	- 큐에서 요소를 제거 (dequeue)할 때 typescript 에러가 발생
	- `this.length`가 0이 되면 `tail`도 `undefined`로 설정해야 함
```typescript
if (this.length === 0) {
	this.tail = undeifned;
}
```
- peek 메서드 구현
```typescript
peek() {
	return this.head ? this.head.value : undefined;
}
```

# 5. Stack
## 1. 스택의 기본 개념
- 스택은 연결 리스트를 기반으로 한 자료구조로 다음과 같은 특징을 가짐
	- 노드는 값 (value)과 다음 노드를 가리키는 포인터 (next)를 포함
	- 이중 연결 리스트의 경우 이전 노드를 가리키는 포인터 (previous)도 포함

## 2. 스택 vs 큐의 차이점
- Queue: A -> B -> C -> D 순서로, head와 tail이 있음
- Stack: Queue와 반대 반향으로 작동
	- A -> B -> C -> D에서 head가 맨 앞에 위치
	- 한쪽 끝 (head)에서만 추가와 제거가 이루어짐

## 3. 스택의 시각적 이해
- 스택을 "접시 더미"라고 생각
	- 접시를 쌓을 때는 맨 위에 올리고
	- 접시를 꺼낼 때도 맨 위에서 꺼냄
	- LIFO (Last In, First Out) 원리

## 4. Stack의 주요 연산
### 1. Push (추가) 연산
```
E를 추가할 때:
1. E가 현재 head를 가리키도록 함
2. head를 E로 업데이트
```

### 2. Pop (제거) 연산
```
1. 현재 head를 임시 저장
2. head를 다음 노드로 업데이트
3. 제거된 노드 반환
```

### 3. Peek 연산
- 큐와 동일하게 head의 값을 반환 (제거하지 않음)

## 5. 스택의 실제 활용
1. 함수 호출: 함수를 호출할 때 스택 구조로 관리됨
2. 스택 트레이스: 코드 에러 시 함수 호출 순서를 보여주는 것
3. 메모리 관리: 컴퓨터의 메모리 영역 중 "스택"이라 불리는 부분

## 6. 시간 복잡도
- 모든 스택 연산 (push, pop, peek)은 O(1) 상수 시간
	- 포인터만 업데이트하면 되므로
	- 리스트의 크기나 값의 크기와 무관하게 동일한 시간 소요

## 7. 주의사항
- 스택과 큐를 구현할 때 연산 순서를 잘못하면 데이터를 잃어버릴 수 있음
- 특히 메모리 관리가 중요한 언어에서는 메모리 누수가 발생할 수 있음
