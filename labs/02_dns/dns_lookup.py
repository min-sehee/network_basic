import socket
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python dns_lookup.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    print(f"[DNS] domain={domain}")

    infos = socket.getaddrinfo(domain, None)
    ips = sorted({info[4][0] for info in infos})

    for ip in ips:
        print(f" -> {ip}")

    print("\nTip: DNS resolves a name into one or more IPs.")

if __name__ == "__main__":
    main()
