import random
import socket
import datetime
import time
from encryption import Encryption


class Keys:
    def __init__(self):
        self.b = random.randint(100, 100000)
        self.g = 0
        self.p = 0
        self.A = 0
        self.status = True

    def get_B(self):
        B = self.g ** self.b % self.p
        return B

    def get_K(self):
        K = self.A ** self.b % self.p
        return K


key = Keys()
enc = Encryption()

sock = socket.socket()

port = input('Enter port: ')  # вводим порт
sock.bind(('', int(port)))

while True:

    sock.listen(1)

    conn, addr = sock.accept()
    print()
    key.status = True

    while True:
        # ОТПРАВКА ОТКРЫТОГО КЛЮЧА
        if key.A != 0 and key.p != 0 and key.g != 0 and key.status:  # если получили все открытые ключи Клиента
            print(f'send: key-B = {key.get_B()}')
            print(f'key-K: {key.get_K()}')
            key.status = False
            time.sleep(0.25)
            conn.send(f'key-B: {key.get_B()}'.encode())  # отправляем открытый ключ В от Сервера

        # ПОЛУЧЕНИЕ СООБЩЕНИЯ ОТ КЛИЕНТА
        try:
            data = conn.recv(1024).decode("utf8")
        except ConnectionResetError as e:
            break

        # ПОЛУЧЕНИЕ КЛЮЧЕЙ ШИФРОВАНИЯ КЛИЕНТА
        if data[:5] == 'key-A':
            print(data)
            key.A = int(data.split(' ')[1])
        elif data[:5] == 'key-g':
            print(data)
            key.g = int(data.split(' ')[1])
        elif data[:5] == 'key-p':
            print(data)
            key.p = int(data.split(' ')[1])
        else:

            # СООБЩЕНИЯ
            old_data = data  # зашифрованное сообщение
            data = enc.Bytes_Msg(data, key.get_K())  # расшифрованное
            new_data = enc.Msg_Bytes(data + '_readed', key.get_K())  # новое
            print(f'Msg from client: {data}')

            # ВЫХОД КЛИЕНТА
            if data == "" or data == "exit":
                break
            elif data == "stop":
                break
            else:

                # ОБРАТНАЯ ОТПРАВКА СООБЩЕНИЯ
                conn.send(new_data.encode())


    if data == "stop":
        break

conn.close()
