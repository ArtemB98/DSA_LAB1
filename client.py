"""
Реализация socket клиент-сервер, передача сообщения
Клиент
"""

import socket

# Создание клиента:
client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

client.connect(
    ("127.0.0.1", 1234)
)

# считывает и отправляет картинку
file = open('image.png', mode="rb") #считываем картинку

data = file.read(2048)

while data:
    client.send(data)
    data = file.read(2048)

file.close()
client.close()
