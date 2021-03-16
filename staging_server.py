"""
Промежуточный Сервер
"""

import socket
import time
import cv2
import numpy as np
import os

# Создание промежуточного сервера:
staging_server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

staging_server.bind(
    ("127.0.0.1", 1234)  # localhost
)

staging_server.listen()  # может принимать некоторое количество сообщений
print("Server is listening", '\n')

staging_server2 = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

staging_server2.connect(
    ("127.0.0.1", 1235)
)

while True:
    try:
        client_socket, client_address = staging_server.accept()

        data1 = client_socket.recv(2048)
        sizeOfImage1 = int(data1.decode())
        print("Size of input image:", sizeOfImage1)

        # Принимаю картинку
        file = open('image_staging_server.png', mode="wb")  # открыть для записи принимаемой картинки файл

        while sizeOfImage1 > 0:
            data = client_socket.recv(2048)
            file.write(data)
            sizeOfImage1 = sizeOfImage1 - 2048

        file.close()

        # Внесение шума
        image = cv2.imread('image_staging_server.png')

        row, col, ch = image.shape
        mean = 0
        var = 100
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy = image + gauss

        # save the denoised image
        cv2.imwrite('image_staging_server_output.png', noisy)

        # считывает, отправляет размер и саму картинку
        file = open('image_staging_server_output.png', mode="rb")  # считываем картинку

        imageSize = os.path.getsize('image_staging_server_output.png')
        print("Size of output image:", imageSize)
        staging_server2.send(str(imageSize).encode())
        time.sleep(0.1)

        while imageSize > 0:
            data = file.read(2048)
            staging_server2.send(data)
            imageSize = imageSize - 2048

        file.close()
        print("Image was sent", '\n')
    except:
        print("An unexpected error occurred", '\n')
        break

staging_server.close()
