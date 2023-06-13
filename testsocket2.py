import socket


def server_program():
    host = socket.gethostname()
    port = 65432
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(2)
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        data = conn.recv(1024).decode()
        if not data:
            break
        print(str(data))
        data = r"""HTTP/1.1 200 OK
Content-Type: text/plain

OK"""
        conn.send(data.encode())
        conn.close()


if __name__ == '__main__':
    server_program()
