# 🌐 Network Basics Lab

## ⚙️ 요구 사항

- Python 3.9+
- pip

```bash
pip install flask
```

---

## 🧪 Lab 1. IP & Port

### 1️⃣ 서버 실행

```bash
python labs/01_ip_port_http/app.py
```

실행 시 아래와 같은 로그가 출력됩니다.

```text
Running on all addresses (0.0.0.0)
Running on http://127.0.0.1:8000
Running on http://<사설IP>:8000
```

---

### 2️⃣ 접속 확인

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
- 서버와 클라이언트가 같은 컴퓨터에서 통신
- 항상 접근 가능

#### 사설 IP (예: 172.x.x.x)

- 같은 네트워크(LAN)에 있는 다른 기기에서 접근 가능한 주소
- 실제 서버 통신과 가장 유사한 형태

⚠️ 학교/공공 Wi-Fi에서는 보안 정책으로 차단될 수 있음

---

## 🧪 Lab 2. DNS

도메인 이름이 IP 주소로 변환되는 과정을 확인합니다.

```bash
python labs/02_dns/dns_lookup.py google.com
```