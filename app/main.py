import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True: 
        try: 
            client, address = server_socket.accept()
            with client :
                print("Server connected to {}:{}".format(address[0], address[1])),
                req = client .recv(1024).decode("utf-8")
                client.send("HTTP/1.1 200 OK\r\n\r\n".encode("utg-8"))
        except:
            print("Server closed")
            server_socket.close()
            break
if __name__ == "__main__":
    main()
