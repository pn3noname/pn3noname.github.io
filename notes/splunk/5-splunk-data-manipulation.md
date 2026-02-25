---
title: "Splunk: Data Manipulation"
slug: "5-splunk-data-manipulation"
date: "2026-02-25"
category: "Splunk"
tags: ["Splunk", "Data Manipulation", "props.conf", "transforms.conf", "Field Extraction", "Data Masking"]
description: "A comprehensive look at Splunk data manipulation — covering configuration files (props.conf, transforms.conf, inputs.conf), fixing event boundaries with regex, parsing multi-line events, masking sensitive data with SEDCMD, and extracting custom fields using field transforms."
---

source: https://tryhackme.com/room/splunkdatamanipulation

# 1. Splunk Data Processing: Overview
## Data parsing은 관련 필드를 추출하고 효율적인 분석을 위해 데이터를 구조화된 형식으로 변환하는 과정을 포함함
## 과정
### 1. Understand the Data Format
- 파싱하려는 데이터 형식 이해하기
- Splunk는 CSV, JSON, XML, syslog 등 다양한 데이터 형식을 지원함
- 데이터 소스의 형식과 추출하려는 관련 필드 확인할 것

### 2. Identify the Sourcetype
- Splunk에서 sourcetype은 인덱싱되는 데이터의 형식을 나타냄
- 이를 통해 Splunk는 적절한 parsing rules (구문 분석 규칙)을 적용할 수 있음
- 데이터 소스에 미리 정의된 sourcetype이 없는 경우, Splunk에서 사용자 지정 sourcetype을 생성할 수 있음

### 3. Configure `props.conf`
- `props.conf` 파일은 특정 소스 유형 또는 데이터 소스에 대한 파싱 설정을 정의함
- 이 파일은 `$SPLUNK_HOME/etc/system/local` 디렉터리에 있음
- `props.conf` 파일 구성 방법의 예
```bash
[source::/path/to/your/data]
sourcetype = your_sourcetype
```
  - `your_sourcetype`은 해당 데이터에 할당할 소스 유형의 이름

### 4. Define Field Extractions
- Regular Expressions (Regex)를 정의하거나 미리 정의된 추출 기법을 사용하여 데이터에서 필드를 추출할 수 있음
- `props.conf` 파일에서 필드 추출을 정의하는 예
```bash
[your_sourcetype]
EXTRACT-fieldname1 = regular_expression1
EXTRACT-fieldname2 = regular_expression2
```
  - 추후 `your_sourcetype`을 정의한 실제 소스 유형 이름으로 바꾸기
  - `regular_expression1 or 2`는 원하는 값을 일치시키고 추출하는 데 사용되는 정규 표현식

### 5. Save and Restart Splunk
- `props.conf` 파일을 변경한 후에는 파일을 저장하고 Splunk를 재시작하여 새 구성을 적용
- Splunk 웹 인터페이스 또는 명령줄을 사용하여 이 작업을 수행할 수 있음

### 6. Verify and Search the Data
- Splunk가 재시작되면 데이터가 올바르게 파싱되었는지 검색하고확인 가능
- 추출된 필드를 사용하여 데이터를 효과적으로 필터링하고 분석 가능
  

# 2. Exploring Splunk Configuration files
## Splunk는 데이터 처리 및 인덱싱의 다양한 측면을 제어하기 위해 여러 설정 파일을 사용함
## Splunk configuration files
<img width="641" height="542" alt="image" src="https://github.com/user-attachments/assets/f2366cbd-52d1-4abe-9603-878a19fb8f54" />
<img width="641" height="542" alt="image" src="https://github.com/user-attachments/assets/42a6ac9d-0118-45a7-9239-c2082056b0b2" />
<img width="641" height="542" alt="image" src="https://github.com/user-attachments/assets/9566c09b-798c-41b9-8bde-8d1b3b383e56" />
<img width="640" height="318" alt="image" src="https://github.com/user-attachments/assets/1c3b9f76-f733-4703-a569-938b91b82522" />
  
## Splunk 주요 설정 파일 정리
### 1. `inputs.conf`
- 목적: 데이터 입력을 정의하고 다양한 소스로부터 데이터를 수집하는 방법을 설정
- ex: 특정 로그 파일을 모니터링하려는 경우, `inputs.conf`를 다음과 같이 설정할 수 있음
```bash
[monitor:///path/to/logfile.log]
sourcetype = my_sourcetype
```

### 2. `props.conf`
- 목적: 다양한 sourcetype에 대한 파싱 규칙을 지정하여 필드를 추출하고 필드 추출 규칙을 정의
- ex: `my_sourcetype`이라는 커스텀 sourcetype이 있고 정규 표현식을 사용하여 필드를 추출하려는 경우, `props.conf`에서 정의
```bash
[my_sourcetype]
EXTRACT-field1 = regular_expression1
EXTRACT-field2 = regulat_expression2
```

### 3. `transforms.conf`
- 목적: 인덱싱된 이벤트에 대한 필드 변환 및 보강을 정의
- ex: 기존 필드 값을 기반으로 새로운 이벤트 필드를 추가하려는 경우, `transforms.conf`를 사용
```bash
[add_new_field]
REGEX = existing_field=(.*)
FORMAT = new_field::$1
```
  
### 4. `indexes.conf`
- 목적: Splunk의 인덱스 설정을 관리하며, 저장소, 보존 정책 및 액세스 제어를 포함
- ex: `my_index`라는 새 인덱스를 특정 설정으로 생성하려는 경우, `indexes.conf`를 설정
```bash
[my_index]
homePath = $SPLUNK_DB/my_index/db
coldPath = $SPLUNK_DB/my_index/colddb
thawedPath = $SPLUNK_DB/my_index/thaweddb
maxTotalDataSizeMB = 100000
```

### 5. `outputs.conf`
- 목적: 원격 Splunk 인스턴스나 서드파티 시스템과 같은 다양한 출력으로 인덱싱된 데이터를 전송하기 위한 대상 및 설정을 지정
- ex: 인덱싱된 데이터를 원격 Splunk 인덱서로 전달하려는 경우, `outputs.conf`를 설정
```bash
[tcpout]
defaultGroup = my_indexers
[tcpout:my_indexers]
server = remote_indexer:9997
```

### 6. `authentication.conf`
- 목적: 인증 설정 및 사용자 인증 방법을 관리
- ex: Splunk 사용자에 대해 LDAP 인증을 활성화하려는 경우, `authentication.conf`를 설정
```bash
[authentication]
authSettings = LDAP
[authenticationLDAP]
SSLEnabled = true
```
  
## STANZAS in Splunk Configurations
- STANZAS
  - Splunk 구성 파일에서 사용되는 설정 블록 (특정 설정들을 그룹화해서 묶어놓은 섹션)
  - 구조
```bash
[스탠자_이름]
설정1 = 값1
설정2 = 값2
설정3 = 값3
```
  - 스탠자를 사용하는 이유
    1. 조직화: 관련된 설정들을 한 곳에 묶어서 관리하기 쉽게 만듦
    2. 구분: 여러 소스타입이나 다른 데이터 형식에 대한 각각 다른 설정을 적용할 수 있음
    3. 가독성: 어떤 설정이 어떤 데이터에 적용되는지 명확하게 알 수 있음

- Splunk 구성에는 데이터가 처리되고 인덱싱되는 방식을 정의하는 다양한 STANZA 구성이 포함되어 있음
- 이러한 스탠자들은 특정 목적을 가지고 있으며, 이것들이 무엇이고 어떻게 사용되는지 이해하는 것이 중요함
- 일반적인 스탠자들에 대한 간단한 요약
<img width="600" height="564" alt="image" src="https://github.com/user-attachments/assets/6a0ef766-0bc1-4aba-8d5a-3765df44245f" />
<img width="600" height="475" alt="image" src="https://github.com/user-attachments/assets/2d8f23b3-e0c7-4974-ad93-34b6e2b66753" />
<img width="600" height="182" alt="image" src="https://github.com/user-attachments/assets/b68992a0-8aa9-4972-adaf-367a9a5c7b79" />


# 3. Creating a Simple Splunk App
## Splunk 설치 경로 : `/opt/splunk`
## Splunk App Directory
<img width="657" height="286" alt="image" src="https://github.com/user-attachments/assets/0b7dfbdb-9ba1-4548-9f4c-cd83016f3296" />
    
## Splunk Apps 생성하는 방법
### 1. Splunk instance에서 Apps 오른쪽에 있는 톱니바퀴 클릭
<img width="406" height="232" alt="image" src="https://github.com/user-attachments/assets/1dd8ee0a-a748-40bd-b492-34ed9b71ece7" />

### 2. `Create App` 버튼 클릭
<img width="600" height="229" alt="image" src="https://github.com/user-attachments/assets/12e6b0e7-8a59-4895-8451-90f53704f74c" />

### 3. 각 항목에 필요한 정보를 채워넣기
- `Folder name` 아래에 나오는 파일 경로는 `/opt/splunk/etc/app`
<img width="576" height="482" alt="image" src="https://github.com/user-attachments/assets/371e0d86-f2ad-4548-b86c-e452093e87bf" />

### 4. `Launch App` 눌러서 확인
<img width="598" height="198" alt="image" src="https://github.com/user-attachments/assets/75e8dbef-0889-4abd-86c2-a8f953b0f282" />

### 5. 터미널로 돌아와서 `cd /opt/splunk/etc/apps`에서 `ls` 명령어를 사용하여 새로 생성한 `NewApp` 찾아서 `ls` 명령어로 파일 목록 읽기
<img width="598" height="454" alt="image" src="https://github.com/user-attachments/assets/3be0be7d-317e-46d3-93e4-3acca039cf85" />

### 6. Create a Python script to generate sample logs
- `bin` 디렉토리에서 새로운 파이썬 파일 생성하기
```bash
nano samplelogs.py
```
- 생성된 파일 안에 `print("This is a sample log...")`라는 내용 저장

- 이후, 다음의 명령어로 결과 확인
```bash
/opt/splunk/etc/apps/NewApp/bin# python3 samplelogs.py
This is a sample log...
```

- `/opt/splunk/etc/apps/NewApp/bin/samplelogs.py`의 경로를 다른 곳에 잘 적어두기

### 7. Creating `Inputs.conf`
- `/opt/splunk/etc/apps/NewApp/default` 의 경로에서 `default` 폴더 안에 `inputs.conf` 파일 생성
```bash
nano inputs.conf
```

- 생성된 파일 안에 다음과 같은 내용 저장
```bash
[script:///opt/splunk/etc/apps/NewApp/bin/samplelogs.py]
index = main
source = test_log
sourcetype = tesing
interval = 5
```
  - `samplelogs.py` 스크립트의 출력을 가져와 5초마다 main 인덱스를 사용하여 Splunk로 전송하는 설정

### 8. Splunk restart
```bash
/opt/splunk/bin/splunk restart
```

### 9. Splunk instance로 돌아가서 `index=main` & `All time(real-time)`으로 검색 시작


# 4. Event Boundaries - Understanding the problem
- Splunk에서 Event breaking (이벤트 분할)이란 지정된 경계를 기준으로 원시 데이터를 개별 이벤트로 나누는 것을 의미함
- Splunk는 이벤트 구분 규칙을 사용하여 한 이벤트가 끝나고 다음 이벤트가 시작되는 지점을 식별함
- 방법
## 1. `/home/ubuntu/Downloads/scripts`의 경로에서 `vpnlogs` 파일을 찾아 읽기
<img width="598" height="263" alt="image" src="https://github.com/user-attachments/assets/86b88d45-bf43-48ab-88d2-632b39d4ba6b" />

## 2. 해당 파일을 새로 만든 Splunk 앱인 `DataApp`의 `bin`으로 복사하기
- `cp /home/ubuntu/Downloads/scripts/vpnlogs /opt/splunk/etc/apps/DataApp/bin/`
- `chmod +x /opt/splunk/etc/apps/DataApp/bin/vpnlogs`
<img width="598" height="150" alt="image" src="https://github.com/user-attachments/assets/61621635-2b3b-4efe-8882-26f16c8f1958" />
  
## 3. DataApp의 `default`로 들어가서 `inputs.conf` 파일 수정하기
- `nano inputs.conf`
```bash
[script:///opt/splunk/etc/apps/DataApp/bin/vpnlogs]
index = main
source = vpn
sourcetype = vpn_logs
interval = 5
```

## 4. Restart Splunk
- `/opt/splunk/bin/splunk restart`

## 5. Splunk inetrface에서 Search Query: `index=main sourcetype=vpn_logs`로 설정하고 time range를 `All time (Real-time)`으로 설정하면 해당 로그들을 불러올 수 있음
<img width="598" height="311" alt="image" src="https://github.com/user-attachments/assets/4c687de5-6a53-4da4-bfa5-cca44920cbbe" />

- 하지만, Splunk가 각 이벤트의 경계를 제대로 구분하지 못하고 여러 이벤트를 하나의 이벤트로 인식하여 `CONNECT`와 `DISCONNECT`가 한 로그 안에 섞여서 표현됨

## 6. Fixing the Event Boundary
### 1. Splunk에서 이벤트를 구분하도록 구성하려면 `props.conf` 파일을 일부 수정해야 하는데, 이 경우 먼저 이벤트의 끝을 판별하는 정규식을 만들어야 함
<img width="559" height="355" alt="image" src="https://github.com/user-attachments/assets/3a9a776a-9a9b-4fe7-b086-f10401c15b3a" />

### 2. `/opt/splunk/etc/apps/DataApp/default`의 경로에 `nano props.conf`를 입력하여 새로운 파일 생성하기
```bash
[vpn_logs]
SHOULD_LINEMERGE = true
MUST_BREAK_AFTER = (DISCONNECT|CONNECT)
```

### 3. Restart Splunk
- `/opt/splunk/bin/splunk restart`
<img width="559" height="487" alt="image" src="https://github.com/user-attachments/assets/3100c453-2bad-492d-9a0f-0c4c68b0da6f" />

### Questions
#### 1. Which configuration file is used to specify parsing rules?
- `props.conf`

#### 2. What regex is used in the above case to break the Events?
- `(DISCONNECT|CONNECT)`

#### 3. Which stanza is used in the configuration to force Splunk to break the event after the specified pattern?
- `MUST_BREAK_AFTER`


# 5. Parsing Multi-line Events
## 다양한 로그 소스는 각기 다른 방식으로 로그를 생성함
## 어떤 로그 소스는 Windows 이벤트 로그와 같이 여러 줄로 구성된 이벤트 로그를 생성하기도 함
## ex: `authentication_logs` 스크립트에서 생성된 샘플 이벤트 로그
```c
[Authentication]:A login attempt was observed from the user Michael Brown and machine MAC_01
at: Mon Jul 17 08:10:12 2023 which belongs to the Custom department. The login attempt looks suspicious.
```
## `inputs.conf` 파일을 업데이트하여 위의 스크립트를 포함시키고 Splunk가 의도한 대로 이벤트를 분할하는지 확인하기
### 1. `/home/ubuntu/Downloads/scripts`의 경로에서 `autthentication_logs` 파일을 찾아 읽기
<img width="601" height="127" alt="image" src="https://github.com/user-attachments/assets/d05139ac-8f71-4d8c-9533-c4dfa4569484" />

### 2. 해당 파일을 새로 만든 Splunk 앱인 `DataApp`의 `bin`으로 복사하기
- `cp /home/ubuntu/Downloads/scripts/authentication_logs /opt/splunk/etc/apps/DataApp/bin/`
- `chmod +x /opt/splunk/etc/apps/DataApp/bin/vpnlogs`

### 3. DataApp의 `default`로 경로 수정해서 들어가서 `inputs.conf` 파일 수정하기
- `nano inputs.conf`
```bash
[script:///opt/splunk/etc/apps/DataApp/bin/authentication_logs]
interval = 5
index = main
sourcetype= auth_logs
host = auth_server
```

### 4. Restart Splunk
- `/opt/splunk/bin/splunk restart`

### 5.  Splunk inetrface에서 Search Query: `index=main sourcetype=auth_logs`로 설정하고 time range를 `All time (Real-time)`으로 설정하면 해당 로그들을 불러올 수 있음
<img width="601" height="380" alt="image" src="https://github.com/user-attachments/assets/1e36bf20-3890-4c97-82b4-80d6edc97822" />

- 하지만, Splunk가 두 줄로 된 이벤트를 두 개의 서로 다른 이벤트로 분리하고 경계를 구분하지 못함

### 6. 위의 문제를 해결하기 위해 `props.conf` 파일에 다른 stanzas를 사용할 수 있음
```bash
[auth_logs]
SHOULD_LINEMERGE = true
BREAK_ONLY_BEFORE = \[Authentication\]
```

### 7. Splunk를 restart하고 이전과 같은 Search Query로 다시 수행
<img width="601" height="593" alt="image" src="https://github.com/user-attachments/assets/fc9439bf-dc00-4843-9723-da8dfa0611b8" />


# 6. Masking Sensitive Data
## 1. `/home/ubuntu/Downloads/scripts`의 경로에서 `purchase-details` 파일을 찾아 읽기

## 2. 해당 파일을 새로 만든 Splunk 앱인 `DataApp`의 `bin`으로 복사하기
- `cp /home/ubuntu/Downloads/scripts/purchase-details /opt/splunk/etc/apps/DataApp/bin/`
- `chmod +x /opt/splunk/etc/apps/DataApp/bin/purchase-details

## 3. DataApp의 `default`로 경로 수정해서 들어가서 `inputs.conf` 파일 수정하기
- `nano inputs.conf`
```bash
[script:///opt/splunk/etc/apps/DataApp/bin/purchase-details]
interval = 5
index = main
source = purchase_logs
sourcetype= purchase_logs
host = order_server
```

## 4. Restart Splunk

## 5. Splunk inetrface에서 Search Query: `index=main sourcetype=purchase_logs`로 설정하고 time range를 `All time (Real-time)`으로 설정하면 해당 로그들을 불러올 수 있음
<img width="640" height="395" alt="image" src="https://github.com/user-attachments/assets/a2af974e-cbca-4a6d-86a5-b465844f82ae" />

- 하지만 각 이벤트에 추가되는 신용카드 정보를 숨겨야 하며, 이벤트 경계도 수정해야 함

## 6. 위의 문제를 해결하기 위해 `regex101.com`을 사용하여 각 이벤트의 끝 경계를 식별하는 정규 표현식 패턴을 생성하고 이를 `props.conf`에 업데이트 함
```bash
[purchase_logs]
SHOULD_LINEMERGE = true
MUST_BREAK_AFTER = \d{4}\.
```

## 7. Splunk를 restart하고 검색 쿼리를 다시 입력하면 다음과 같이 보임
<img width="640" height="372" alt="image" src="https://github.com/user-attachments/assets/8a454011-5a42-4cc9-9740-3bb8b3258d76" />

## 8. 남은 문제는 카드 정보 숨기기
- Splunk에서 `SEDCMD` 구성 설정은 `props.conf` 파일에서 사용되며, 인덱싱 과정에서 데이터를 수정하거나 변환하는 데 사용됨
- 이 설정을 통해 인덱싱되기 전에 들어오는 데이터에 정규 표현식 기반 치환을 적용할 수 있음
- `sedcmd` 설정은 Unix `sed` 명령어의 구문과 기능을 사용함
- `props.conf`에서 `sedcmd`가 작동하는 방식
  1. Splunk 구성 디렉토리 (`default`)에서 `props.conf` 파일 열기
  2. 수정하려는 데이터 소스에 대한 stanza를 찾거나 생성함
  3. 스탠자 아래에 `sedcmd` 설정을 추가함
  4. `sed` 명령어와 유사한 `s/` 구문을 사용하여 정규 표현식 패턴과 교체 문자열을 지정함
- ex
  ```bash
  [source::/path/to/your/data]
  SEDCMD-myField = s/oldValue/newValue/g
  ```
- `sedcmd`는 데이터 변환을 위해 `props.conf`에서 사용되는 구성 설정 중 하나일 뿐. `REGEX`, `TRANSFORMS` 등과 같은 다른 옵션도 사용 가능
- 실제 적용 방법: `default` 경로에서 `props.conf`로 가서 내용 수정하기
  ```bash
  [purchase_logs]
  SHOULD_LINEMERGE = true
  MUST_BREAK_AFTER = \d{4}\.
  SEDCMD-cc = s/-\d{4}-\d{4}-\d{4}/-XXXX-XXXX-XXXX/g
  ```
- Splunk를 restart한 뒤 검색 쿼리를 적용하면 다음과 같이 출력됨
<img width="596" height="591" alt="image" src="https://github.com/user-attachments/assets/4d728f25-c476-4200-ab44-af51bde62f91" />


# 7. Extracting Custom Fields
<img width="679" height="594" alt="image" src="https://github.com/user-attachments/assets/7348da32-b160-42ec-83d9-94a98ce5a8a6" />

- 위의 예시에서 보다시피 `host`, `source`, `sourcetype` 같은 기본 필드만 자동으로 추출됨
- 하지만 로그 안에 있는 `User`, `Server`, `Action` 같은 중요한 정보들은 별도의 필드로 추출되지 않음
- 이 상태에서는 특정 유저가 몇 번 접속했는지, 특정 서버에 대한 Action (연결/해제) 이벤트가 몇 건 있었는지 등과 같은 분석을 하기 어려움 (∵ 유저, 서버, Action이 독립적인 필드가 아니라 Event 문자열 안에 묻혀있기 때문)

## 1. Extracting Username
### 1. 추출하려는 사용자 이름 값을 캡처하는 정규 표현식 패턴 만들기: [R U(U:-n`User:\s([\w\s]+)`
### 2. `default` 경로에 `transforms.conf` 생성하고 업데이트 하기
```bash
[vpn_custom_fields]
REGEX = User:\s([\w\s]+)
FORMAT = Username::$1
WRITE_META = true
```
- `User:` 다음에 나오는 공백(`\s`)과 문자들(`[\w\s]+`)을 추출
- `FORMAT = Username::$1`
  - 추출한 값을 Username이라는 새 필드로 만듦
  - `$1`은 위 REGEX에서 괄호로 캡처한 첫 번째 그룹 (사용자명) <- `([\w\s]+)`
  - 결과: `Username = "John Doe"` 필드가 생성됨
- `WRITE_META = true`: 이 필드를 메타데이터로 저장하여 검색 성능을 향상시킴
### 3. `transforms.conf`에서 최근 변경한 내용을 `props.conf`에 반영하기
- 기존 `[vpn_logs]`의 마지막 줄에 변경 내용 추가하기
<img width="552" height="265" alt="image" src="https://github.com/user-attachments/assets/0a073819-2d35-40e7-94fd-12a1e69aed3c" />

### 4. `fields.conf` 생성하고 업데이트 하기
- `fields.conf` 파일을 생성하고 로그에서 추출할 필드 (사용자 이름)을 지정하기
- `INDEXED = true`는 Splunk에게 인덱싱된 시점에 이 필드를 추출하도록 지시하는 것
  ```bash
  [Username]
  INDEXED = true
  ```
### 5. Splunk를 restart한 뒤, 검색 쿼리를 `index=main sourcetype=vpn_logs`로 적용
<img width="597" height="507" alt="image" src="https://github.com/user-attachments/assets/03974d43-d097-4085-ae73-fb955d08e5d1" />
<img width="597" height="507" alt="image" src="https://github.com/user-attachments/assets/8744f84c-9176-424c-b113-9bee096293d7" />

## 2. Extracting Server and Action
### 1. 추출하려는 사용자 이름, 서버, Action 값을 캡처하는 정규 표현식 패턴 만들기: `User:\s([\w\s]+),.+(Server.+),.+:\s(\w+)`
### 2. `default` 경로에 `transforms.conf` 생성하고 업데이트 하기
```bash
[vpn_custom_fields]
REGEX = User:\s([\w\s]+),.+(Server.+),.+:\s(\w+)
FORMAT = Username::$1 Server::$2 Action::$3
WRITE_META = true
```
### 3. `fields.conf`에 업데이트 하기
- `fields.conf` 파일에 Splunk가 인덱싱 시점에 추출할 필드 이름으로 업데이트하기
- `INDEXED = true`는 Splunk에게 인덱싱된 시점에 이 필드를 추출하도록 지시하는 것
  ```bash
  [Username]
  INDEXED = true
  
  [Server]
  INDEXED = true
  
  [Action]
  INDEXED = true
  ```
### 4. Splunk를 restart한 뒤, 검색 쿼리를 `index=main sourcetype=vpn_logs`로 적용
<img width="597" height="567" alt="image" src="https://github.com/user-attachments/assets/b63163e2-c026-46ff-af90-764a5136b357" />
<img width="597" height="567" alt="image" src="https://github.com/user-attachments/assets/64a86741-964a-4f5f-94d3-85ecab598ecb" />
<img width="597" height="567" alt="image" src="https://github.com/user-attachments/assets/1ac672dd-32b9-4022-a49b-18f1d8fd57ed" />


# 8. Questions
## 1. Extract the Username field from the sourcetype purchase_logs we worked on earlier. How many Users were returned in the Username field after extraction?
### 1. Splunk 앱에서 DataApp을 만들기
### 2. `purchase-details`파일을 `DataApp`의 `bin`으로 복사해오기
<img width="597" height="72" alt="image" src="https://github.com/user-attachments/assets/fd7cb34c-683f-4891-a24e-bd7c34ee7648" />

### 3. `default` 경로로 가서 `inputs.conf` 파일 생성하고 내용 저장하기
<img width="597" height="117" alt="image" src="https://github.com/user-attachments/assets/ad0c6935-e1a0-4aff-9fb6-c2914a8fb315" />

### 4. `props.conf` 파일 생성하고 내용 저장하기
<img width="597" height="94" alt="image" src="https://github.com/user-attachments/assets/e386ca07-b6b4-455c-9ec6-395d3a1f3271" />

### 5. `transforms.conf` 파일 생성하고 내용 저장하기
<img width="597" height="94" alt="image" src="https://github.com/user-attachments/assets/b86428c9-c0e7-458a-9d56-4f6218dd623a" />

### 6. `fields.conf` 파일 생성하고 내용 저장하기
<img width="597" height="58" alt="image" src="https://github.com/user-attachments/assets/3859e2f4-703a-4c97-ac4c-eed68589bf94" />

### 7. Splunk restart하고 검색 쿼리로 `index=main sourcetype="purchase-logs"`
<img width="597" height="380" alt="image" src="https://github.com/user-attachments/assets/f9dbd1ee-76bc-4c21-bcb3-f52644537d45" />

## 2. Extract Credit-Card values from the sourcetype purchase_logs, how many unique credit card numbers are returned against the Credit-Card field?
### 1. `default` 경로로 가서 `transforms.conf` 내용 수정하고 저장하기
<img width="597" height="135" alt="image" src="https://github.com/user-attachments/assets/f80178bf-8deb-4004-9fd9-e53d65acef7a" />

### 2. `fields.conf` 내용 수정하고 저장하기
<img width="597" height="143" alt="image" src="https://github.com/user-attachments/assets/581d5471-17c4-4fe5-b91c-922d05f985c8" />

### 3. Splunk restart하고 검색 쿼리에 `index=main soucetype="purchase-logs"`
<img width="597" height="500" alt="image" src="https://github.com/user-attachments/assets/aed575a3-0070-4730-b44f-48446ee2f1cd" />

