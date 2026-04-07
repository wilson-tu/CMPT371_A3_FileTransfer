import socket
import os

HOST = '0.0.0.0'
PORT = 5001
SAVE_DIR = "received_files"

def start_server():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"[SERVER] Listening on {HOST}:{PORT}...")

    conn, addr = server.accept()
    print(f"[SERVER] Connected by {addr}")

    try:
        while True:
            # Read header safely
            header = b""
            while b"\n" not in header:
                chunk = conn.recv(1)
                if not chunk:
                    return
                header += chunk

            header = header.decode().strip()

            if header == "DONE":
                break

            filename, filesize = header.split("|")
            filesize = int(filesize)

            filepath = os.path.join(SAVE_DIR, filename)

            print(f"\n[SERVER] Receiving {filename} ({filesize} bytes)")

            received = 0

            with open(filepath, "wb") as f:
                while received < filesize:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    received += len(data)

                    print(f"[SERVER] {filename}: {received}/{filesize}", end="\r")

            print(f"\n[SERVER] {filename} received.")

        print("[SERVER] All files received.")

    except Exception as e:
        print("[SERVER ERROR]", e)

    finally:
        conn.close()
        server.close()


if __name__ == "__main__":
    start_server()