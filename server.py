from socket import *
import threading

HOST = '0.0.0.0'
PORT = 8888

clients = []

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Сервер запущено на {HOST}:{PORT}")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Підключився клієнт: {address}")
        clients.append(client_socket)
        t = threading.Thread()
        t.start()

if __name__ == "main":
    main()
