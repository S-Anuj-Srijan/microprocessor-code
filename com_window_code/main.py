import asyncio
from datetime import datetime

import comencment_marco_polo_code
from init import ComWindow# uses the ComWindow class you created earlier

PORTS = [80, 81, 82]


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    listen_port: int,
    com: ComWindow
):
    peer = writer.get_extra_info("peername")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Connected on port {listen_port} from {peer}")

    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break

            text = data.decode("utf-8", errors="replace")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] Port {listen_port} RX from {peer}: {text!r}")

            # Forward to Arduino over serial.
            # If you want raw forwarding with no prefix, set payload = text.
            payload = text.rstrip("\r\n")
            if payload:
                com.write(payload)  # ComWindow adds '\n' for Arduino line-based parsing

            # ACK back to sender
            writer.write(f"ACK port={listen_port} bytes={len(data)}\n".encode("utf-8"))
            await writer.drain()

    except asyncio.CancelledError:
        raise
    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Port {listen_port} ERROR from {peer}: {e}")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Disconnected on port {listen_port} from {peer}")


async def start_server_on_port(port: int, com: ComWindow):
    async def handler(reader, writer):
        return await handle_client(reader, writer, port, com)

    server = await asyncio.start_server(handler, host="0.0.0.0", port=port)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
    print(f"Listening on {addrs}")
    return server


async def main(com: ComWindow):
    servers = []
    for p in PORTS:
        servers.append(await start_server_on_port(p, com))

    await asyncio.gather(*(s.serve_forever() for s in servers))


if __name__ == "__main__":
    # 1) Run Marco–Polo discovery (CALL THE FUNCTION)
    result = comencment_marco_polo_code.find_first_polo_port()

    if result:
        comencment_marco_polo_code.write_dict_to_file(result, "detected_port.txt")
        print("First responding port saved to detected_port.txt")
        print(f"Detected port: {result.get('port')}")
    else:
        print("No device responded with 'polo'")
        raise SystemExit(1)

    # 2) Open serial connection to detected Arduino port
    port_name = result["port"]
    com = ComWindow(port=port_name, baudrate=9600, timeout=1)

    try:
        com.open()
        com.flush()

        # 3) Start TCP servers and forward to serial
        asyncio.run(main(com))

    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        com.close()
