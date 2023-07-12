# socket'in aynı anda kaç client'tan gelecek request'leri handle edeceği test edildi, request'leri sıraya aldığı görüldü

import socket
import multiprocessing
import email
from io import StringIO
import time

def start_socket(pipe):
    host = socket.gethostname()
    port = 65433
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        data = conn.recv(1024).decode()
        if not data:
            break
        received_body = 0
        _, headers = data.split('\r\n', 1)
        message = email.message_from_file(StringIO(headers.lower()))
        headers = dict(message.items())
        received_body += len(data.split('\r\n\r\n')[1])
        while received_body < int(headers["content-length"]):
            data += conn.recv(1024).decode()
            received_body += 1024

        # with open('requests.txt', 'a') as f:
        #     f.write(data + '\r\n\r\n')

        pipe.send(data.split('\r\n\r\n')[1])
        msg = pipe.recv()
        
        resp = r"""HTTP/1.1 200 OK
Content-Type: text/plain

""" + msg
        conn.send(resp.encode())
        conn.close()

def start_scene(pipe):
    while True:
        data = pipe.recv()
        time.sleep(10)
        pipe.send(data)

def main():
    conn_endp1, conn_endp2 = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=start_socket, args=(conn_endp1,))
    p2 = multiprocessing.Process(target=start_scene, args=(conn_endp2,))
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    

if __name__ == '__main__':
    main()