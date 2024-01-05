from cvzone.HandTrackingModule import HandDetector
import cv2
import socket

# Inicializar las variables para almacenar la posición previa
previous_wrist_position = [0, 0, 0]
previous_thumb_position = [0, 0, 0]
previous_index_position = [0, 0, 0]

width, height = 1280, 720

# Inicializar la captura de video y el detector de manos
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Configurar socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    # Obtener frame de imagen
    success, img = cap.read()

    # Encontrar la mano y sus landmarks
    hands, img = detector.findHands(img)  # with draw

    # Si se detecta una mano
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]  # Lista de 21 puntos de referencia

        # Coordenadas actuales de muñeca, pulgar e índice
        current_wrist_position = lmList[0]
        current_thumb_position = lmList[4]
        current_index_position = lmList[8]

        # Calcular los deltas de posición
        wrist_delta = [current - previous for current, previous in zip(current_wrist_position, previous_wrist_position)]
        thumb_delta = [current - previous for current, previous in zip(current_thumb_position, previous_thumb_position)]
        index_delta = [current - previous for current, previous in zip(current_index_position, previous_index_position)]

        # Preparar los datos para enviar
        data_wrist = f'wrist,{wrist_delta[0]},{wrist_delta[1]},{wrist_delta[2]}'
        data_thumb = f'thumb,{thumb_delta[0]},{thumb_delta[1]},{thumb_delta[2]}'
        data_index = f'index,{index_delta[0]},{index_delta[1]},{index_delta[2]}'

        # Enviar los datos de los deltas a través de UDP
        sock.sendto(str.encode(data_wrist), serverAddressPort)
        sock.sendto(str.encode(data_thumb), serverAddressPort)
        sock.sendto(str.encode(data_index), serverAddressPort)

        # Actualizar las posiciones previas para el próximo frame
        previous_wrist_position = current_wrist_position
        previous_thumb_position = current_thumb_position
        previous_index_position = current_index_position

    # Mostrar la imagen
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    cv2.imshow("Image", img)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y destruir todas las ventanas
cap.release()
cv2.destroyAllWindows()