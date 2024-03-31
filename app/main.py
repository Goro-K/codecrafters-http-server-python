import socket
import threading

def handle_request(conn, addr):
    """Traite une requête HTTP reçue via la connexion établie."""
    try:
        print(f"Connected to {addr}")
        data = conn.recv(4096).decode("utf-8")  # Réception des données de la requête
        if not data:  # Si aucune donnée n'est reçue, ne fait rien
            return

        # Traitement simplifié de la requête HTTP
        request_line, _, headers_part = data.partition('\r\n')
        method, path, _ = request_line.split()
        # Vous pouvez ajouter plus de logique ici pour traiter différents types de requêtes

        # Réponse simple basée sur le chemin
        if path == "/":
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Hello, World!</h1></body></html>"
        else:
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>"

        conn.sendall(response.encode("utf-8"))
    finally:
        conn.close()

def main():
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen(5)  # Commence à écouter les connexions entrantes
    print("Server is listening on localhost:4221")

    try:
        while True:  # Boucle principale du serveur
            conn, addr = server_socket.accept()  # Accepte une connexion entrante
            # Création d'un nouveau thread qui exécute la fonction handle_request pour chaque connexion
            client_thread = threading.Thread(target=handle_request, args=(conn, addr))
            client_thread.start()  # Démarre le thread
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
