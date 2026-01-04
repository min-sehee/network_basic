from __future__ import annotations

import json
import socket
import sys
import time
from urllib.parse import urlparse


def resolve_host(host: str) -> list[str]:
    infos = socket.getaddrinfo(host, None)
    return sorted({info[4][0] for info in infos})


def tcp_connect_time(ip: str, port: int, timeout_s: float = 3.0) -> float:
    start = time.perf_counter()
    with socket.create_connection((ip, port), timeout=timeout_s):
        end = time.perf_counter()
    return (end - start) * 1000.0  # ms


def http_get(host: str, ip: str, port: int, path: str, timeout_s: float = 3.0) -> tuple[int, str]:
    """
    매우 단순한 HTTP/1.1 GET (교육용)
    - Host 헤더는 도메인/호스트로 넣음
    - 연결은 ip:port로 수행
    """
    req = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"User-Agent: network-basics-client/1.0\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    ).encode("utf-8")

    with socket.create_connection((ip, port), timeout=timeout_s) as s:
        s.sendall(req)
        chunks = []
        while True:
            data = s.recv(4096)
            if not data:
                break
            chunks.append(data)

    raw = b"".join(chunks).decode("utf-8", errors="replace")
    status_line = raw.split("\r\n", 1)[0] if raw else ""
    # e.g. "HTTP/1.1 200 OK"
    try:
        status_code = int(status_line.split()[1])
    except Exception:
        status_code = -1

    return status_code, raw


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python client.py <url>")
        print("Example: python client.py http://localhost:8000")
        return 1

    url = sys.argv[1]
    u = urlparse(url)
    if not u.scheme or not u.netloc:
        print("Invalid URL. Include scheme like http://")
        return 1

    host = u.hostname or ""
    port = u.port or 80
    path = u.path or "/"
    if u.query:
        path += "?" + u.query

    print(f"[INPUT] host={host}, port={port}, path={path}")

    # 1) DNS
    ips = resolve_host(host)
    print("[DNS] resolved IPs:")
    for ip in ips:
        print(f" - {ip}")

    # 2) TCP connect timing (첫 IP로 측정)
    target_ip = ips[0]
    try:
        ms = tcp_connect_time(target_ip, port)
        print(f"[TCP] connect to {target_ip}:{port} = {ms:.1f} ms")
    except Exception as e:
        print(f"[TCP] connect failed to {target_ip}:{port} ({type(e).__name__}: {e})")
        return 2

    # 3) HTTP
    status, raw = http_get(host, target_ip, port, path)
    print(f"[HTTP] status={status}")

    # body만 간단히 출력 (너무 길면 자름)
    parts = raw.split("\r\n\r\n", 1)
    body = parts[1] if len(parts) == 2 else ""
    body_preview = body[:500] + ("..." if len(body) > 500 else "")
    print("[HTTP] body preview:")
    print(body_preview)

    # JSON이면 pretty print
    try:
        obj = json.loads(body)
        print("\n[HTTP] json parsed:")
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
