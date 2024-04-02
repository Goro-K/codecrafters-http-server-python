import socket
import threading
import sys
import os

# Parse command line arguments
directory = None
for i, arg in enumerate(sys.argv):
    if arg == "--directory" and i + 1 < len(sys.argv):
        directory = sys.argv[i + 1]
        break

if directory is None:
    print("Usage: python your_server.py --directory <directory>")
    sys.exit(1)

def handle_request(conn, addr):
    """Traite une requête HTTP reçue via la connexion établie."""
    try:
        print(f"Connected to {addr}")
        data = conn.recv(4096).decode("utf-8")
        if not data:
            return

        request_line = data.split("\r\n")[0]
        method, path, _ = request_line.split(' ', 2)
        
        # Serve files under the specified directory
        if path.startswith("/files/") and method == "GET":
            filepath = os.path.join(directory, path[len("/files/"):])
            print(f"Attempting to open: {filepath}")  # Affiche le chemin complet du fichier
            
            if os.path.exists(filepath) and os.path.isfile(filepath):
                with open(filepath, "rb") as file:
                    content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n"
                conn.sendall(response.encode("utf-8") + content)
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
                conn.sendall(response.encode("utf-8"))
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            conn.sendall(response.encode("utf-8"))
    finally:
        conn.close()

def main():
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen(5)
    print("Server is listening on localhost:4221")

    try:
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_request, args=(conn, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
