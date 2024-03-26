import socket


def main():

    server_socket = socket.create_server(("localhost", 4221))
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected to {addr}")
        data = conn.recv(1239)
        conn.send("HTTP/1.1 200 OK\r\n\r\n".encode("utf-8"))
        
    server_socket.close()
    
if __name__ == "__main__":
    main()
