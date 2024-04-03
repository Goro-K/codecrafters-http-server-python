import os
import socket
import pathlib
import argparse

from concurrent.futures import ThreadPoolExecutor, wait
parser = argparse.ArgumentParser(
    prog="HTTP Server", description="Serves files over HTTP"
)
parser.add_argument("-d", "--directory", type=pathlib.Path)

args = parser.parse_args()
def check_path(data):
    return data.split(b"\r\n")[0].split(b" ")[1]

def check_method(data):
    return data.split(b"\r\n")[0].split(b" ")[0]

def get_user_agent(data):
    for d in data.split(b"\r\n"):
        if d.startswith(b"User-Agent:"):
            return d.split(b"User-Agent: ")[1]
        
def check_dir(dir, file_name):
    filepath = os.path.join(dir, file_name)

    return os.path.isfile(filepath)

def main(server_socket):
    while True:
        connection, _ = server_socket.accept()  # accept new connection

        data = connection.recv(1024)
        path = check_path(data)
        method = check_method(data)
        print(method)
        if path == b"/":
            connection.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        elif path.startswith(b"/user-agent"):
            user_agent = get_user_agent(data)
            connection.sendall(
                f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n".encode()
            )
            connection.sendall(user_agent)
        elif path.startswith(b"/files"):
            file_name = path.split(b"/")[2].decode()
            if not check_dir(dir=args.directory, file_name=file_name):
                print("not found")
                connection.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                connection.sendall(b"")
            else:
                print("sending")
                d = open(f"{args.directory}/{file_name}", "rb").read()
                connection.sendall(
                    f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(d)}\r\n\r\n".encode()
                )
                connection.sendall(d)
        elif method == b"POST" and path.startswith(b'/files'):
            print("POST")
            file_name = path.split(b"/")[2].decode()
            print(file_name)
            d = data.split(b"\r\n\r\n")[1]
            print(d)
            with open(f"{args.directory}/{file_name}", "wb") as f:
                f.write(d)
            connection.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())
            connection.sendall(b"")

        elif path.startswith(b"/echo"):
            d = path.split(b"/")[2:]
            connection.sendall(
                f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(b'/'.join(d))}\r\n\r\n".encode()
            )
            connection.sendall(b"/".join(d))
        else:
            connection.sendall("HTTP/1.1 404 NOT FOUND\r\n\r\n".encode())
        connection.close()

if __name__ == "__main__":
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # main(server_socket)
    with ThreadPoolExecutor(max_workers=10) as executor:
        fs = [executor.submit(main, server_socket) for _ in range(10)]
        wait(fs)
