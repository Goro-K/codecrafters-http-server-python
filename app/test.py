import socket
import threading

def handle_request(conn):
    """Traite une requête HTTP reçue via la connexion établie."""
    data = conn.recv(4096).decode("utf-8")  # Taille ajustée pour une meilleure compatibilité
    if not data:  # Si aucune donnée n'est reçue, retourne
        return

    # Extraction des informations de la requête
    lines = data.split("\r\n")
    request_line = lines[0].split(" ")
    headers = {line.split(": ")[0]: line.split(": ")[1] for line in lines[1:] if ": " in line}
    print(headers)
    path = request_line[1]
    agent = headers.get("User-Agent", "Unknown")

    # Construction de la réponse en fonction du chemin
    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo/"):
        content = path[6:]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"
    elif path.startswith("/user-agent"):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(agent)}\r\n\r\n{agent}"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    conn.sendall(response.encode("utf-8"))

def main():
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen(5)  # Commence à écouter les connexions entrantes

    try:
        while True:  # Boucle principale du serveur
            conn, addr = server_socket.accept()  # Accepte une connexion entrante
            print(f"Connected to {addr}")
            with conn:
                handle_request(conn)
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
