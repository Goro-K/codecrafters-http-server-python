import socket, os
import argparse 
from threading import Thread
import pathlib

def main(directory):
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen(5)  # Commence à écouter les connexions entrantes
    print("Server is listening on localhost:4221")

    try:
        while True:  # Boucle principale du serveur
            conn, addr = server_socket.accept()  # Accepte une connexion entrante
            # Création d'un nouveau thread qui exécute la fonction handle_request pour chaque connexion
            # Démarre le Thread 
            Thread(target=handle_request, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        server_socket.close()

def check_dir(dir, file_name):
    filepath = os.path.join(dir, file_name)
    return os.path.isfile(filepath)

def handle_request(conn, addr):
    """Traite une requête HTTP reçue via la connexion établie."""
    try:
        print(f"Connected to {addr}")
        data = conn.recv(4096).decode("utf-8")  # Réception des données de la requête
        if not data:  # Si aucune donnée n'est reçue, ne fait rien
            return

        # Traitement simplifié de la requête HTTP
        request_line, _, headers_part = data.partition('\r\n')
        headers_lines = headers_part.split('\r\n')  # Divise les en-têtes en lignes
        headers = {line.split(": ")[0]: line.split(": ")[1] for line in headers_lines if ": " in line}  # Crée un dictionnaire d'en-têtes
        method, path, _ = request_line.split(' ', 2)  # Extractions de la méthode, du chemin et de la version HTTP
        agent = headers.get("User-Agent", "Unknown")

        # Réponse simple basée sur le chemin
        if path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"
        elif path.startswith("/echo/"):
            content = path[6:]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
        elif path.startswith("/user-agent"):
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(agent)}\r\n\r\n{agent}"
        elif path.startswith("/files"):
            file_name = path.split("/")[2].decode()
            print(file_name)
            if not check_dir(dir=args.directory, file_name=file_name):
                print("not found")
                conn.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                conn.sendall(b"")
            else:
                print("sending")
                d = open(f"{args.directory}/{file_name}", "rb").read()
                conn.sendall(
                    f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(d)}\r\n\r\n".encode()
                )
                conn.sendall(d)
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        conn.sendall(response.encode("utf-8"))  # Envoie la réponse au client
    finally:
        conn.close()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP server")
    parser.add_argument("--directory", required=True, help="Directory to serve files from")
    args = parser.parse_args()
    main(args.directory)