from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def home():
    return (
        "OK! You reached the server.\n"
        f"client_ip={request.remote_addr}\n"
        "Try accessing via localhost and via your private IP.\n"
    )

if __name__ == "__main__":
    # host=0.0.0.0: 내 PC의 모든 인터페이스에서 받음 (사설IP로 접속 가능)
    app.run(host="0.0.0.0", port=8000, debug=True)

import datetime

@app.get("/")
def home():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return (
        f"[{now}] OK! You reached the server.\n"
        f"Your IP: {request.remote_addr}\n"
    )