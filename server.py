import socket
import os

# Listen on all available networks
HOST = '0.0.0.0'
PORT = 5001
SAVE_DIR = "received_files" # Directory where received files will be saved

def start_server(): # Start the server, accept one client connection, and receive files until DONE

    # Create the save directory if it doesn't already exist
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Set up a TCP server socket and wait for a connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"[SERVER] Listening on {HOST}:{PORT}...")

    conn, addr = server.accept()
    print(f"[SERVER] Connected by {addr}")

    try:
        while True:
            # Read the header one byte at a time until we hit a newline
            # The header format is: "filename|filesize\n"
            header = b""
            while b"\n" not in header:
                chunk = conn.recv(1)
                if not chunk:
                    return # Client disconnected unexpectedly
                header += chunk
            
            # "DONE" signals that the client has finished sending all files
            header = header.decode().strip()

            if header == "DONE":
                break

            # Parse filename and expected byte count from the header
            filename, filesize = header.split("|")
            filesize = int(filesize)

            filepath = os.path.join(SAVE_DIR, filename)

            print(f"\n[SERVER] Receiving {filename} ({filesize} bytes)")

            received = 0

            # Write incoming data to disk in 1 KB chunks until the full file arrives
            with open(filepath, "wb") as f:
                while received < filesize:
                    data = conn.recv(1024)
                    if not data:
                        break # Connection dropped mid transfer
                    f.write(data)
                    received += len(data)

                    print(f"[SERVER] {filename}: {received}/{filesize}", end="\r")

            print(f"\n[SERVER] {filename} received.")

        print("[SERVER] All files received.")

    except Exception as e:
        print("[SERVER ERROR]", e)

    # Clean up both the connection and the server socket
    finally:
        conn.close()
        server.close()


if __name__ == "__main__":
    start_server()