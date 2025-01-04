import socket
import threading


# Функція для прийому повідомлень
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("З'єднання закрито.")
            client_socket.close()
            break


# Підключення до сервера
client_socket = socket.socket()
client_socket.connect(("127.0.0.1", 20000))

try:
    # Авторизація
    print(client_socket.recv(1024).decode())
    login = input()
    client_socket.send(login.encode())

    print(client_socket.recv(1024).decode())
    password = input()
    client_socket.send(password.encode())

    response = client_socket.recv(1024).decode()
    print(response)

    if "успішна" in response:
        # Запуск потоку для прийому повідомлень
        thread = threading.Thread(target=receive_messages, args=(client_socket,))
        thread.start()

        # Основний цикл для відправки повідомлень
        while True:
            message = input()
            client_socket.send(message.encode())
finally:
    client_socket.close()
