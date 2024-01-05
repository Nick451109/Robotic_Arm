import cv2
import mediapipe as mp
import numpy as np

# configuramos a Mediapipe para la detección de manos
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# detectamos colores en formato HSV (ajusta según tu color amarillo claro)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Inicializamos el objeto de la mano de Mediapipe
hands = mp_hands.Hands()

# Inicializamos la cámara
cap = cv2.VideoCapture(0)

# Configuraramos el kernel para los operadores morfológicos
kernel = np.ones((5, 5), np.uint8)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convertimos la imagen a formato HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definimos las máscaras para cada color
    mask_index = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_thumb = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_wrist = cv2.inRange(hsv, lower_red, upper_red)

    # Aplicamos operadores morfológicos para reducir falsos positivos
    mask_index = cv2.morphologyEx(mask_index, cv2.MORPH_OPEN, kernel)
    mask_thumb = cv2.morphologyEx(mask_thumb, cv2.MORPH_OPEN, kernel)
    mask_wrist = cv2.morphologyEx(mask_wrist, cv2.MORPH_OPEN, kernel)

    # Aplicamos las máscaras
    index_result = cv2.bitwise_and(frame, frame, mask=mask_index)
    thumb_result = cv2.bitwise_and(frame, frame, mask=mask_thumb)
    wrist_result = cv2.bitwise_and(frame, frame, mask=mask_wrist)

    # Encontramos contornos para obtener la posición del área de detección
    contours_index, _ = cv2.findContours(mask_index, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_thumb, _ = cv2.findContours(mask_thumb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_wrist, _ = cv2.findContours(mask_wrist, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Mostramos el nombre de cada dedo justo encima del área de detección
    if contours_index:
        index_area = cv2.boundingRect(contours_index[0])
        cv2.putText(frame, 'Indice', (index_area[0], index_area[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    if contours_thumb:
        thumb_area = cv2.boundingRect(contours_thumb[0])
        cv2.putText(frame, 'Pulgar', (thumb_area[0], thumb_area[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    if contours_wrist:
        wrist_area = cv2.boundingRect(contours_wrist[0])
        cv2.putText(frame, 'Muneca', (wrist_area[0], wrist_area[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Mostrar los resultados
    cv2.imshow('Indice', index_result)
    cv2.imshow('Pulgar', thumb_result)
    cv2.imshow('Muneca', wrist_result)

    # Mostrar la imagen original con las manos dibujadas
    cv2.imshow('Tiempo real', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
