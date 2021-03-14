"""
Сервер
"""
import cv2
import socket

# Прежде всего нам необходимо создать сокет:
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

server.bind(
    ("127.0.0.1", 1235)  # localhost
)

server.listen()  # может принимать некоторое количество сообщений
print("Server is listening", '\n')

client_socket, client_address = server.accept()
while True:
    try:

        data = client_socket.recv(2048)
        sizeOfImage = int(data.decode('utf-16'))
        print("Size of input image:", sizeOfImage)

        # Принимаю картинку
        file = open('image_server.png', mode="wb")  # открыть для записи принимаемой картинки файл

        while sizeOfImage > 0:
            data = client_socket.recv(2048)
            file.write(data)
            sizeOfImage = sizeOfImage - 2048

        file.close()

        # Применение медианного фильтра
        image = cv2.imread('image_server.png')

        # apply the 49×49 median filter on the image
        processed_image = cv2.medianBlur(image, 49)

        # save image to disk
        cv2.imwrite('image_server_filter.png', processed_image)
        print("Image was processed", '\n')
    except:
        print("An unexpected error occurred", '\n')
        break

server.close()
