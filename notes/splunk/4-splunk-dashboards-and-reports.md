---
title: "Splunk: Dashboards and Reports"
slug: "4-splunk-dashboards-and-reports"
date: "2026-02-24"
category: "Splunk"
tags: ["Splunk", "SPL", "Dashboard", "Visualization", "Line chart", "SOC", "Log Analysis"]
description: "An overview of Splunk's reporting and visualization features — exploring how to reuse saved searches as reports, consolidate multiple results into dashboards with various chart types, and set up alerts that notify analysts the moment a suspicious pattern, such as a brute-force login attempt, is detected."
---

source: https://tryhackme.com/room/splunkdashboardsandreports

# 1. Creating Reports for Recurring Searches
  - host들은 서로 다른 수의 이벤트를 전송하는데, 주어진 기간 (ex: 전체 기간, 24시간 동안) 동안 각 VPN 사용자가 로그인한 횟수를 확인하는 방법
    - `host=vpn_server | stats count by Username`
<img width="642" height="483" alt="image" src="https://github.com/user-attachments/assets/bc6880ce-424e-401e-b801-0e6875392901" />

  - 위의 내용을 바탕으로 새로운 보고서를 만들고 싶다면 `Save As (다른 이름으로 저장)`으로 할 수 있음
<img width="642" height="483" alt="image" src="https://github.com/user-attachments/assets/95f6282c-d98f-4a1f-8eee-b9fe7fc5d922" />
  
<img width="520" height="344" alt="image" src="https://github.com/user-attachments/assets/fe047875-b1c2-4f34-99d1-879cdca6bfa4" />

  - Time-range picker (시간 범위 선택기)에 `yes`로 선택함으로써, 보고서를 실행하면 시간 범위 선택기 옵션이 표시됨    
  - Report (보고서) 탭을 선택하면 방금 만든 VPN users 보고서를 확인할 수 있음
<img width="644" height="315" alt="image" src="https://github.com/user-attachments/assets/bf50eac7-4084-4cac-bfe9-80b4a22d19bf" />


# 2. Creating Dashboards for Summarizing Results
  - Dashboards는 일반적으로 데이터의 가장 중요한 부분을 간략하게 개괄적으로 보여주기 위해 만들어짐
  - Dashboards는 특정 기간 동안 발생한 사고 건수처럼 경영진에게 데이터를 보여줄 때 유용하며, SOC 분석가들이 어떤 부분에 집중해야 하는지 파악할 때도 도움이 됨
  - ex: 데이터 소스에서 급증이나 급감을 식별해 실패한 로그인 시도가 갑자기 증가했는지 등
  - Dashboards의 주요 목적: 사용 가능한 정보를 시각적으로 빠르게 개괄적으로 보여주는 것
  - 아래의 예시에서 보다시피 권한을 `Shared in App (앱 내 공유)`로 설정하면 Splunk의 다른 사용자도 대시보드를 볼 수 있음
<img width="520" height="609" alt="image" src="https://github.com/user-attachments/assets/f97c8810-3c06-41b1-aea1-38b2ffed8143" />
	  
  - Classic Dashboard 선택 -> 만들기 -> `Add Panel` 선택하면 오른쪽 사이드 메뉴가 나타남
<img width="643" height="271" alt="image" src="https://github.com/user-attachments/assets/8251895a-005d-4d6a-9a07-7948e42bc48d" />

  - 오른쪽 사이드 메뉴에서 `New from Report (보고서에서 새로 만들기)` 선택 -> `VPN users` -> `Add to Dashboard (대시보드에 추가)`
<img width="643" height="410" alt="image" src="https://github.com/user-attachments/assets/1c5ab846-d0e6-4528-9e84-e7b26c6bde67" />

  - 보고서 형태로도 확인할 수 있는데 굳이 대시보드에 추가하는 이유
    - 대시보드에서는 메뉴에서 visualization (시각화) 방식을 선택할 수 있음
<img width="606" height="437" alt="image" src="https://github.com/user-attachments/assets/206dd881-1379-402f-b72c-88ffb6c8e744" />

<img width="606" height="361" alt="image" src="https://github.com/user-attachments/assets/5cbb83c1-9fe5-4c0d-b7f2-fe51bc0a212a" />
  
  - Question: Create a dashboard from the web-server logs that show the status codes in a line chart. Which status code was observed for the least number of times?
    1. `검색`에서 `host=web-server | stats count by status_code` 명령어 입력 (전체 시간)
    2. `다른 이름으로 저장`에서 `보고서` 선택
    3. 제목: `web-server` 지정하고 저장
    4. 대시보드 -> 새 대시보드 만들기 -> 대시보드 제목: `web-server logs` & 권한: `앱에서 공유됨` & 클래식 대시보드 -> 만들기
    5. +패널 추가 선택 -> 보고서에서 새로 만들기: `web-server` 선택 -> 대시보드에 추가
    6. 시각화 선택 -> Line Chart 선택 
<img width="606" height="176" alt="image" src="https://github.com/user-attachments/assets/f594048f-b0f8-48aa-b824-b7fa80e130cc" />
      - 400
  - Summary
    - Reports (보고서): 반복적으로 검색을 실행해야 할 때
    - Dashboards (대시보드): 여러 보고서를 하나로 묶거나 시각화를 만들어야 할 때

# 3. Alerting on High Priority Events
  - Reports나 Dashboards는 정해진 시간 간격으로만 사용자에게 표시됨
  - 때때로 특정 이벤트가 발생할 때 알림을 받고 싶을 때가 있음 (ex: 하나의 계정에서 실패한 로그인 횟수가 임계값에 도달하면 이는 무차별 대입 공격을 의미하는데, 이런 일이 발생하는 즉시 알림을 받고 싶음)
  - Splunk에서 이 알림을 설정할 수 있음
