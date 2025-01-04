import socket
import threading

# Створення серверу
new_socket = socket.socket()
new_socket.bind(("127.0.0.1", 20000))
new_socket.listen()

print("Сервер запущено!")

users = {"user1": "password1", "user2": "password2"}  # База користувачів
clients = []  # Список підключених клієнтів


# Функція для розсилки повідомлень усім клієнтам
def broadcast_message(message, sender_conn):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            clients.remove(client)
            client.close()


# Функція для обробки клієнта
def handle_client(conn, addr):
    print(f"{addr} підключився!")

    try:
        # Автентифікація клієнта
        conn.send("Введіть свій логін:".encode())
        login = conn.recv(1024).decode()

        conn.send("Введіть свій пароль:".encode())
        user_password = conn.recv(1024).decode()

        if login in users and users[login] == user_password:
            conn.send("Авторизація успішна! Ви у чаті.".encode())
            print(f"Користувач {login} підключився.")
            clients.append(conn)  # Додати клієнта до списку

            # Повідомлення для всіх про нового користувача
            broadcast_message(f"{login} приєднався до чату!", conn)

            # Основний цикл для прийому повідомлень
            while True:
                message = conn.recv(1024).decode()
                if message:
                    full_message = f"{login}: {message}"
                    print(f"Повідомлення від {login}: {message}")

                    # Розіслати повідомлення всім клієнтам
                    broadcast_message(full_message, conn)
                else:
                    break
        else:
            conn.send("Неправильний логін або пароль. Відключення.".encode())
            print(f"Неправильна авторизація для {addr}.")
    except:
        print(f"Помилка з'єднання з {addr}")
    finally:
        # Видалення клієнта зі списку і закриття з'єднання
        if conn in clients:
            clients.remove(conn)
        conn.close()
        print(f"{addr} відключився.")
        # Повідомлення про вихід користувача
        broadcast_message(f"{login} вийшов із чату.", conn)


# Цикл для прийому підключень
while True:
    conn, addr = new_socket.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
