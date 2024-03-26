import socket


def main():

    while True: # Pour que le serveur fonctionne sans arrêt même après une requête
        server_socket = socket.create_server(("localhost", 4221)) # le serveur fonctionne sur le port 4221
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected to {addr}")
            data = conn.recv(1239).decode("utf-8") # byte to use split method (conn is str)

            data = data.split("\r\n") 
            # ['GET /index.html HTTP/1.1', 'Host: localhost:4221', 'User-Agent: curl/7.81.0', 'Accept: */*', '', '']
            data = data[0].split(" ")
            # ['GET', '/index.html', 'HTTP/1.1']

            if data[1] == "/" :
                response = "HTTP/1.1 200 OK\r\n\r\n".encode("utf-8")
            else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode("utf-8")
            conn.send(response)
            
            server_socket.close()

if __name__ == "__main__":
    main()
