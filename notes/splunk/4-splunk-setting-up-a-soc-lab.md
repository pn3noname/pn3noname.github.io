---
title: "Splunk: Setting up a SOC Lab"
slug: "4-splunk-setting-up-a-soc-lab"
date: "2026-02-23"
category: "Splunk"
tags: ["Splunk", "SOC", "Forwarder", "Log Analysis", "Windows Event Logs", "Linux", "Data Ingestion", "Index"]
description: "A practical walkthrough of building a SOC lab with Splunk — covering CLI commands, data ingestion via Universal and Heavy Forwarders, configuring receivers and indexes, forwarding Linux syslog and Windows Event Logs, and verifying end-to-end log pipelines with the logger utility."
---

source: https://tryhackme.com/room/splunklab

# 1. Splunk: Setting up a Lab
  - Universal Forwarder를 통해 데이터를 수집 & 전송하여 Splunk가 설치된 시스템에서 데이터를 수집, 인덱싱, 검색, 그리고 시각화 등을 하여 로그 분석을 수행할 수 있게 함


# 2. Splunk: Interacting with CLI
## 1. Command: Splunk start
  ```bash
  root@coffely:/opt/splunk#./bin/splunk start
  ```

## 2. Command: Splunk stop
  ```bash
  root@coffely:/opt/splunk#./bin/splunk stop
  ```

## 3. Command: Splunk restart
  ```bash
  root@coffely:/opt/splunk#./bin/splunk restart
  ```

## 4. Command: Splunk status
  ```bash
  root@coffely:/opt/splunk#./bin/splunk status
  ```

## 5. Command: Splunk add oneshot
  - Splunk는 로그 데이터를 수집해서 분석하는 도구인데, 보통은 지속적으로 생성되는 로그 파일을 모니터링 함
  - 하지만 `oneshot`은 한 번만 파일을 읽어서 데이터를 인덱스에 추가하는 방식
  - 사용하는 이유
    - 과거 로그 파일 처리: 이미 완성된 오래된 로그 파일이 있을 때, 그걸 한 번만 읽어서 Splunk에 넣고 싶을 때
    - 테스트용: 새로운 데이터 형식이나 파싱 규칙을 테스트할 때 샘플 파일로 시험해보기
    - 일회성 데이터: 계속 갱신되지 않는 정적인 데이터 파일을 한 번만 가져올 때
  - 일반 모니터링과의 차이
    - 일반 모니터링 (`splunk add monitor`): 파일을 계속 지켜보면서 새로운 내용이 추가되면 자동으로 수집
    - `oneshot`: 파일을 딱 한 번만 읽고 끝. 나중에 파일이 변경되어도 다시 읽지 않음
  - 기본 사용
    ```bash
    root@coffely:/opt/splunk#./bin/splunk add oneshot /var/log/application.log
    ```
  - 특정 인덱스 지정
    ```bash
    root@coffely:/opt/splunk#./bin/splunk add oneshot /var/log/application.log -index main
    ```
  - 소스타입 지정
    ```bash
    root@coffely:/opt/splunk#./bin/splunk add oneshot /var/log/apache/access.log -sourcetype access_combined
    ```

## 6. Command: Splunk search
  ```bash
  root@coffely:/opt/splunk#./bin/splunk search coffely
  ```

## 7. Command: Splunk help
  ```bash
  root@coffely:/opt/splunk#./bin/splunk help
  ```


# 3. Splunk: Data Ingestion
  - Splunk Forwarders
    1. Heavy Forwarders
      - 소스에서 로그를 필터링하거나 분석 또는 변경한 후 대상으로 전달해야 할 때 사용됨
    2. Universal Forwarders
      - 대상 호스트에 설치되는 경량 에이전트로, 주된 목적은 필터나 인덱싱을 적용하지 않고 로그를 수집하여 Splunk 인스턴스 또는 다른 포워더로 전송하는 것
      - 별도로 다운로드해야 하며, 사용 전에 활성화해야 함
  - 기본적으로 Splunk forwarder는 8089 포트에서 실행됨 (시스템에서 해동 호트를 사용할 수 없는 경우 사용자에게 지정 포트를 입력하라는 메시지가 표시되는데 이 때, 8090번 포트를 지정)
  - Splunk Forwarder도 `/opt/`에 파일 저장


# 4. Configuring Forwarder on Linux
## 1. Splunk Configuration
  - 호스트 측에서 데이터를 보낼 위치를 설정하고, Splunk가 데이터를 어디에서 수신하는지 알 수 있도록 구성하기
  - Setttings -> DATA: Forwarding and receiving -> Receive data: Configure receiving -> (Green box) New Receiving Port -> Listen on this port: `9997` -> Save
  - 기본적으로 Splunk 인스턴스는 9997번 포트를 통해 포워더로부터 데이터를 수신함

## 2. Creating Index
  - 수신 포트를 활성화했으므로 다음으로 중요한 단계는 수신된 모든 데이터를 저장할 인덱스를 생성하는 것
  - 인덱스를 지정하지 않으면 수신된 데이터는 기본 인덱스 (main index)에 저장되기 시작함
  - Settings -> DATA: Indexes -> Indexes: (Green box) New Index -> Index Name: Linux_host -> Save

## 3. Configuring Forwarder
  - 포워더가 데이터를 올바른 대상으로 전송하도록 구성해야 함
  - Linux host terminal -> `root@coffely:/opt/splunkforwarder/bin# ./splunk add forward-server 10.66.152.135:9997`
<img width="627" height="101" alt="image" src="https://github.com/user-attachments/assets/f024ed4b-5226-409c-b821-76da91d6fff7" />

    - 10.66.152.135: 데이터를 받을 Splunk 인덱서(Indexer) 또는 중앙 Splunk 서버
  - 구조
    - Splunk Forwarder (내 컴퓨터 서버에 설치) = 데이터 수집기: 데이터를 "보내는" 역할
    - Splunk Indexer (10.66.152.135) = 중앙 서버: 데이터를 "받는" 역할
  - 비유: 우체국 집배원 (Forwarder)에게 "이 편지를 서울 본사 (Indexer) 주소 (10.66.152.135)로 보내세요"라고 알려주는 것

## 4. Linux Log Sources
  - Linux는 모든 중요한 로그를 `/var/log` 파일에 저장함
<img width="637" height="439" alt="image" src="https://github.com/user-attachments/assets/0d8c9029-c97b-46f5-841f-b4c329e5e464" />


  - Splunk Forwarder에게 모니터링할 로그 파일 (`/var/log/syslog`) 지정하기
    ```bash
    root@coffely:/opt/splunkforwarder/bin# ./splunk add monitor /var/log/syslog -index Linux_host
    ```
<img width="594" height="69" alt="image" src="https://github.com/user-attachments/assets/bd1e96ef-438d-409c-907c-13a6d3ff96b4" />


## 5. Exploring Inputs.conf
  - 또한 `inputs.conf` 파일을 열어 위에서 사용한 명령 이후에 추가된 구성을 확인 가능
  ```bash
  root@coffely:/opt/splunkforwarder/etc/apps/search/local# ls
  inputs.conf
  ```

## 6. Utilizing Logger Utility
  - Logger는 syslog 파일에 추가될 테스트 로그를 생성하는 내장 명령줄 도구
  - 이미 syslog 파일을 모니터링하고 모든 로그를 Splunk로 전송하고 있으므로, 다음 단계에서 생성되는 로그는 Splunk 로그에서 확인 가능
  ```bash
  tryhackme@coffely:/opt/splunkforwarder/bin# logger "coffely-has-the-best-coffee-in-town"
  ```

  ```bash
  tryhackme@coffely:/opt/splunkforwarder/bin# tail -1 /var/log/syslog
  ```
<img width="642" height="69" alt="image" src="https://github.com/user-attachments/assets/040b3b94-cf3e-4955-b405-92e1e767dd2a" />

<img width="642" height="357" alt="image" src="https://github.com/user-attachments/assets/658e8e4f-89fc-428b-a9a2-3ad1c43a1b34" />


# 5. Splunk: Windows Logs
## 1. Installing and Configuring Forwarder
  - Settings -> Forwarding and receiving -> Receive data: Configure receiving -> Listen on this port: `9997`
  - 기본적으로 Splunk 인스턴스는 포워더로부터 9997번 포트로 데이터를 수신함
  - 이후 UniversalForwarder 설치하면서 Setup 설정
    - Deployment Server: (Hostname or IP) `127.0.0.1:8089`
    - Receiving Indexer: (Hostname or IP) `127.0.0.1:9997`
  - Forwarder까지 설정이 끝나면 Splunk -> Settings -> Distributed Environment: Forwarder management에서 호스트 세부 정보 확인 가능
<img width="597" height="288" alt="image" src="https://github.com/user-attachments/assets/155fe41b-d4d4-48f0-a5eb-73c81297d7ab" />

## 2. Ingesting Windows Logs
  - Splunk -> Settings -> Add Data -> Forward -> Available host(s)에 표시된 `WINDOWS coffelylab`를 더블 클릭하여 Selected host(s)에도 표시되게 하기 -> New Server Class Name: `coffely_lab` -> Next
<img width="597" height="351" alt="image" src="https://github.com/user-attachments/assets/6882e1c2-aaf7-48c5-b515-c33fec70ab32" />

  - Add Data: Local Event Logs -> Select Event Logs에서 Available item(s)의 항목을 더블 클릭하여 Selected item(s)에도 표시되게 하기 -> Next
<img width="597" height="255" alt="image" src="https://github.com/user-attachments/assets/baf93046-535f-45d2-83ab-3b21c07ed181" />

  - Input Settings: Create a new index 선택하여 `win_logs` 생성 -> 드롭다운 메뉴에서 `win_logs` 선택 -> Review -> Submit
<img width="597" height="327" alt="image" src="https://github.com/user-attachments/assets/921a0d9f-f123-41a2-9101-725ad5a80531" />

<img width="597" height="617" alt="image" src="https://github.com/user-attachments/assets/c573dda0-3785-4a3a-9d28-b3dd1b52e7f4" />

  - Question: Search for the events with EventCode=4624. What is the value of the field Message?
    - `source="WinEventLog:*" index="win_logs" EventCode=4624`
