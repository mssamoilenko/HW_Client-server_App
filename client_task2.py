import socket

def send_file():
    host = "127.0.0.1"
    port = 20000

    # Створюємо з'єднання з сервером
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Підключено до сервера {host}:{port}")

        # Отримуємо запит на підтвердження передачі файлу
        response = client_socket.recv(1024).decode()
        print(response)

        # Користувач підтверджує, чи хоче передати файл
        user_response = input("Ваш вибір (так/ні): ").strip().lower()
        client_socket.send(user_response.encode())

        # Якщо користувач погодився, починаємо передачу файлу
        if user_response == "так":
            file_path = input("Введіть шлях до файлу для передачі: ")
            try:
                with open(file_path, "rb") as f:
                    file_name = file_path.split("/")[-1]  # Отримуємо ім'я файлу
                    client_socket.send(file_name.encode())  # Надсилаємо назву файлу

                    # Отримуємо підтвердження від сервера
                    server_response = client_socket.recv(1024).decode()
                    print(server_response)

                    # Відправляємо вміст файлу
                    while chunk := f.read(1024):
                        client_socket.send(chunk)

                    print("Файл успішно надіслано!")
            except FileNotFoundError:
                print("Файл не знайдено! Перевірте шлях.")
        else:
            print("Передача файлу скасована.")
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        client_socket.close()

send_file()
