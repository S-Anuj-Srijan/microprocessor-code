import socket
import time

HOST = "host.docker.internal"   # Docker Desktop host alias
PORTS = [80, 81, 82]

MESSAGES = {
    80:  "from_container port80: hello arduino\n",
    81:  "from_container port81: status check\n",
    82:  "from_container port82: marco\n",
}

def send_one(port: int, message: str):
    with socket.create_connection((HOST, port), timeout=5) as s:
        s.sendall(message.encode("utf-8"))
        # Read ACK (your server sends an ACK line)
        ack = s.recv(1024)
        print(f"Sent -> {HOST}:{port} | msg={message.strip()!r} | ack={ack.decode('utf-8', errors='replace').strip()!r}")

def main():
    for p in PORTS:
        send_one(p, MESSAGES[p])
        time.sleep(0.2)

if __name__ == "__main__":
    main()
