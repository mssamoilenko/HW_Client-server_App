import socket
import threading

def handle_client(conn, addr):
    print(f"{addr} підключився!")
    try:
        # Запитуємо у клієнта, чи хоче він передати файл
        conn.send("Ви хочете здійснити передачу файлу? (так/ні): ".encode())
        user_response = conn.recv(1024).decode().strip().lower()

        if user_response == "так":
            conn.send("Запит підтверджено, чекаю назву файлу.".encode())

            # Отримуємо назву файлу
            file_name = conn.recv(1024).decode()
            print(f"Отримую файл: {file_name}")

            # Відкриваємо файл для запису
            with open(file_name, "wb") as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)

            print(f"Файл {file_name} успішно отримано від {addr}.")
            conn.send("Файл успішно отримано!".encode())
        else:
            conn.send("Передача файлу скасована.".encode())
            print(f"{addr} скасував передачу файлу.")
    except Exception as e:
        print(f"Помилка при обробці клієнта {addr}: {e}")
    finally:
        conn.close()
        print(f"З'єднання з {addr} закрито.")

def start_server(host="127.0.0.1", port=20000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Сервер запущено на {host}:{port}!")

    try:
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"Активні з'єднання: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\nСервер зупиняється...")
    finally:
        server_socket.close()

start_server()
