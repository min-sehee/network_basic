# 🌐 Network Basics Lab

이 실습은 네트워크 기초 개념(IP, Port, DNS, TCP, HTTP)을  
**실행 결과를 관찰하며 흐름 중심으로 이해**하는 것을 목표로 합니다.

---

## ⚙️ 요구 사항

```bash
pip install flask
```

---

## 🧪 Lab 1. IP & Port

### 1️⃣ 내 네트워크 IPv4 주소 확인

현재 사용 중인 네트워크(Wi-Fi)의 **사설 IPv4 주소**를 확인합니다.

#### Windows

```bash
ipconfig
```

예시:

```text
무선 LAN 어댑터 Wi-Fi:
   IPv4 주소 . . . . . . . . . : 192.168.45.193
```

#### macOS

```bash
ipconfig getifaddr en0
```

#### Linux / WSL

```bash
ip addr show
```

---

### 2️⃣ 서버 실행 (app.py)

```bash
python labs/01_ip_port_http/app.py
```

실행 시 아래와 같은 로그가 출력됩니다.

```text
Running on all addresses (0.0.0.0)
Running on http://127.0.0.1:8000
Running on http://<사설IP>:8000
```

✅ 여기서 `<사설IP>`가  
앞에서 확인한 **내 네트워크 IPv4 주소와 같은지 비교**해보세요.

---

### 3️⃣ 접속 확인

브라우저에서 아래 주소로 접속합니다.

```text
http://localhost:8000
```

또는

```text
http://127.0.0.1:8000
```

✅ 정상적으로 접속되면 서버가 실행된 것입니다.

---

### 🔍 주소별 의미

#### 127.0.0.1 (localhost)

- 내 컴퓨터 자기 자신을 가리키는 주소
- 네트워크를 거치지 않는 내부 통신
- 항상 접근 가능

#### 사설 IP (예: 172.x.x.x)

- 내 컴퓨터가 네트워크(Wi-Fi)에서 사용하는 주소
- 같은 네트워크(LAN)에 있는 다른 기기에서 접근 가능

⚠️ 학교/공공 Wi-Fi에서는 보안 정책(Client Isolation)으로 차단될 수 있음

---

## 🧪 Lab 2. DNS

도메인 이름이 IP 주소로 변환되는 과정을 확인합니다.

### ▶️ 실행

```bash
python labs/02_dns/dns_lookup.py google.com
```

실행 시 아래와 같은 로그가 출력됩니다.

```text
[DNS] domain=google.com
 -> 142.250.x.x
```

### 🔎 출력 의미

- `domain=google.com`  
  → 사용자가 조회한 도메인 이름

- `142.250.x.x`  
  → 해당 도메인이 변환된 **IP 주소**  
  → DNS(Domain Name System)가 도메인 이름을 실제 서버의 IP로 변환한 결과

💡 이 IP 주소를 통해 컴퓨터는 도메인 이름이 아닌 **IP 주소**를 사용해 서버와 통신합니다.


```bash
python labs/02_dns/dns_lookup.py ys.learnus.org
```

실행 시 아래와 같은 로그가 출력됩니다.

```text
[DNS] domain=ys.learnus.org
 -> 115.85.xxx.xxx
 -> 27.96.xxx.xxx
```

---

### 🔎 확인 포인트

- DNS는 **하나의 IP** 또는 **여러 개의 IP 목록**을 반환할 수 있음
- 반환되는 IP는 실행할 때마다 달라질 수 있음
- 여러 IP를 사용하는 이유:
  - 트래픽 분산 (로드 밸런싱)
  - 장애 대비 (여러 서버 운영)

💡 실제 통신 시 클라이언트는 반환된 IP 중 하나를 선택해 서버와 연결합니다.

---

## 🧪 Lab 3. Client (DNS → TCP → HTTP)

`client.py`를 통해 요청 흐름 전체를 한 번에 확인합니다.

### 실행

```bash
# localhost로 요청
python labs/03_client/client.py http://localhost:8000
```

```bash
# 사설 IP로 요청
python labs/03_client/client.py http://<사설IP>:8000
```

💡 두 실행을 비교하여  
- DNS 결과(IP 개수)
- TCP 연결 시간
- 서버가 인식한 client IP  

가 어떻게 달라지는지 확인해보세요.

---

### 출력에서 확인할 것

#### 1) DNS (Name → IP)
- 입력한 URL의 호스트(`localhost` / 사설 IP)가 어떤 IP로 해석되는지 확인
- `localhost`는 IPv4(`127.0.0.1`)와 IPv6(`::1`)로 해석되어  
  **DNS 결과가 여러 개 출력될 수 있음**
- 사설 IP는 이미 주소가 정해져 있어 보통 하나의 IP만 출력됨

#### 2) TCP (IP:PORT 연결 성립)
- 선택된 IP와 포트(예: `127.0.0.1:8000`, `<사설IP>:8000`)로 연결을 시도
- 출력의 `ms`는 연결 성립까지 걸린 시간
- `localhost`는 내 컴퓨터 내부 연결이라 보통 더 짧게 측정됨

#### 3) HTTP (요청/응답)
- 연결된 TCP 위에서 HTTP 요청을 보내고 응답을 받음
- `status=200`은 정상 응답(OK)을 의미
- body는 서버가 실제로 응답했다는 것을 보여줌

---

### 예시 출력 (localhost)

```text
[INPUT] host=localhost, port=8000, path=/
[DNS] resolved IPs:
 - 127.0.0.1
 - ::1
[TCP] connect to 127.0.0.1:8000 = 0.5 ms
[HTTP] status=200
[HTTP] body preview:
OK! You reached the server.
client_ip=127.0.0.1
Try accessing via localhost and via your private IP.
```

💡 `localhost`는 내 컴퓨터 자신을 가리키는 주소이고,  
사설 IP는 네트워크에서 사용하는 주소이기 때문에  
**DNS 결과와 연결 방식이 다르게 나타날 수 있습니다.**

---

## 🔑 핵심 정리
- IP: 어디로 보낼지
- Port: 어떤 서비스로 보낼지
- DNS: 이름을 IP로 변환
- TCP: 연결이 성립되는지
- HTTP: 연결 위에서 데이터 교환
