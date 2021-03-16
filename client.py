"""
Реализация socket клиент-сервер, передача сообщения
Клиент
"""
import os
import time
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
file = open('image.png', mode="rb")  # считываем картинку

imageSize = os.path.getsize('image.png')
print("Size of image:", imageSize)
client.send(str(imageSize).encode())
time.sleep(0.1)

while imageSize > 0:
    data = file.read(2048)
    client.send(data)
    imageSize = imageSize - 2048

print("Image was sent")
file.close()
client.close()