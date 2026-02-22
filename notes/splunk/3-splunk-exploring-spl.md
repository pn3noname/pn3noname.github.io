---
title: "Splunk: Exploring SPL"
slug: "3-splunk-exploring-spl"
date: "2026-02-22"
category: "Splunk"
tags: ["Splunk", "SPL", "Filtering", "Transformational Commands", "Chart"]
description: "A hands-on guide to Splunk's core architecture — Forwarder, Indexer, and Search Head — and SPL commands for filtering (search, dedup, rename), structuring results (table, head, tail, sort, reverse), and transforming data with statistical and chart commands (top, rare, stats, chart, timechart)."
---

source: https://tryhackme.com/room/splunkexploringspl

# 1. Splunk 관리 명령어
## 1. 상태 확인
  ```bash
  sudo /opt/splunk/bin/splunk status
  ```

## 2. 수동 시작
  ```bash
  sudo /opt/splunk/bin/splunk start
  ```

## 3. 중지
  ```bash
  sudo /opt/splunk/bin/splunk stop
  ```

## 4. 재시작
  ```bash
  sudo /opt/splunk/bin/splunk restart
  ```

## 5. 자동 시작 활성화 (필요 시)
  ```bash
  sudo /opt/splunk/bin/splunk enable boot-start
  ```

## 6. 자동 시작 비활성화 (필요 시)
  ```bash
  sudo /opt/splunk/bin/aplunk disable boot-start
  ```

## 2. Splunk Component
### 1. Splunk Forwarder
  - 모니터링하려는 엔드포인트에 설치되는 경량 에이전트
  - 주요 임무: 데이터를 수집하여 Splunk 인스턴스로 전송
  - 주요 데이터 소스의 예
    - 웹 트래픽을 생성하는 웹 서버
    - Windows Event Logs, PowerShell, Sysmon 데이터를 생성하는 Windows 머신
    - 호스트 중심 로그를 생성하는 Linux 호스트
    - DB 연결 요청, 응답, 오류를 생성하는 DB
  - 포워더는 로그 소스로부터 데이터를 수집하여 Splunk Indexer로 전송함

### 2. Splunk Indexer
  - 포워더로부터 받은 데이터를 처리하는 주요 역할 수행
  - 데이터를 구문 분석하고 필드-값 쌍으로 정규화, 카테고리화, 결과를 이벤트로 저장하여 처리된 데이터를 쉽게 검색하고 분석할 수 있게 만듦
  - 여기서 저장된 데이터는 Search Head에서 검색 가능

### 3. Search Head
  - Search & Reporting 앱 내에서 사용자가 인덱싱된 로그를 검색할 수 있는 곳
  - 검색은 SPL (Search Processing Language)을 사용하여 수행되며, 이는 인덱싱된 데이터를 검색하기 위한 강력한 쿼리 언어
  - 사용자가 검색을 수행하면 요청이 인덱서로 전송되고, 관련 이벤트들이 필드-값 쌍으로 반환됨
  - Search Head는 결과를 표 형태로 변환하고 원형 차트, 막대 차트, 열 차트와 같은 시각화로 표현 가능

## 3. Filtering the Results in SPL
- Search
  ```bash
  index=windowslogs | search Powershell
  ```

- dedup
  - 검색 결과에서 중복된 필드를 제거하는 데 사용되는 명령어
  ```bash
  index=windowslogs | table EventID User Image Hostname | dedup EventID
  ```
  
<img width="1320" height="1074" alt="image" src="https://github.com/user-attachments/assets/2f8b6cff-1a34-434d-9197-2ee6a40090bc" />

- Rename
  - 검색 결과에서 필드 이름을 변경할 수 있음
  - 필드 이름이 일반적이거나 로그인 경우, 또는 출력에서 필드 이름을 업데이트해야 하는 경우에 유용함
  ```bash
  index=windowslogs | fields + host + User + SourceIp | rename User as Employees
  ```

- Windows 로그에서 각 호스트별로 하나의 이벤트만 가져와서, 시간•이벤트ID•호스트명•소스명을 표시하되, 오래된 순서대로 보여주는 쿼리의 예
  ```bash
  index=windowslogs | dedup Hostname | table _time EventID Hostname SourceName | reverse
  ```

## 4. SPL - Structuring the Search Results
- Table
  - `table` 명령을 사용하면 선택한 필드만 열로 포함하는 테이블을 만들 수 있음
  ```bash
  index=windowslogs | table EventID Hostname SourceName
  ```

- Head
  - 이 명령은 숫자를 지정하지 않으면 처음 10개의 이벤트를 반환함
  ```bash
  index=windowslogs | table _time EventID Hostname SourceName | head 5
  ```

- Tail
  ```bash
  index=windowslogs | table _time EventID Hostname SourceName | tail 5
  ```

- sort
  - 필드를 오름차순 또는 내림차순으로 정렬 가능
  ```bash
  index=windowslogs | table _time EventID Hostname SourceName | sort Hostname
  ```

- Reverse
  - Splunk는 기본적으로 최신 이벤트부터 보여주는데 (시간 순으로 내림차순 정렬), `reverse`를 사용하면 가장 오래된 이벤트부터 보여줌 (oldest first)
  ```bash
  index=windowslogs | table _time EventID Hostname SourceName | reverse
  ```

## 5. Transformational Commands in SPL
- 변환 명령어는 필드-값 쌍의 결과를 데이터 구조로 변경하는 명령어
- 각 이벤트의 특정 값을 통계 목적으로 쉽게 활용할 수 있는 숫자 값으로 변환하거나 결과를 시각화로 전환함
- 이러한 변환 명령어를 사용하는 검색을 Transforming Searches (변환 검색)이라고 함

### 1. General Transformational Commands
  - Top
    - 상위 10개 이벤트에 대한 빈도가 높은 값을 반환함
    ```bash
    index=windowslogs | top limit=7 Image
    ```

  - Rare
    - `top` 명령어와는 반대로 빈도가 가장 낮은 값 또는 하위 10개 결과를 반환함
    ```bash
    index=windowslogs | rare limit=7 Image
    ```

  - Highlight
    - 필드가 강조 표시된 원시 이벤트 모드로 결과를 표시함
    ```bash
    index=windowslogs | highlight User, host, EventID, Image
    ```
      
<img width="612" height="616" alt="image" src="https://github.com/user-attachments/assets/107c6267-8842-4b49-8c0f-868c951770e3" />

### 2. STATS Commands
  - SPL은 값에 대한 통계를 계산하는 데 도움이 되는 다양한 stats 명령어를 지원함
<img width="651" height="363" alt="image" src="https://github.com/user-attachments/assets/69a47d29-2290-4be5-8ff5-03f2c2ad9389" />

### 3. Splunk Chart Commands
  - 데이터를 테이블 또는 시각화 형태로 표현하는 데 사용되는 매우 중요한 유형의 변환 명령어

  - Chart
    - chart 명령어는 데이터를 테이블 또는 시각화로 변환하는 데 사용됨
    ```bash
    index=windowslogs | chart count by User
    ```

  - Timechart
    - 언급된 함수를 따르는 필드를 포함하는 시계열 차트를 반환함
    - 종종 stats 명령어와 결합됨
    ```bash
    index=windowslogs | timechart count by Image
    ```

  - Question: Create a pie-chart using the chart command - what is the count for the conhost.exe process?
    - `index=windowslogs | chart count by Image`
<img width="607" height="343" alt="image" src="https://github.com/user-attachments/assets/0d5cf781-dbcf-414c-9f00-52a6c6829524" />
    - 70

