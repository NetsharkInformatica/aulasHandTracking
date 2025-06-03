import cv2
import mediapipe as mp

mp_maos= mp.solutions.hands
mp_desenhar= mp.solutions.drawing_utils
maos=mp_maos.Hands()

camera=cv2.VideoCapture(0)
resolucao_x=1280
resolucao_y=720
camera.set(cv2.CAP_PROP_FRAME_WIDTH,resolucao_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,resolucao_y)

while camera.isOpened():
    ret,frame = camera.read()
    imagem_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    resultado= maos.process(imagem_rgb)
    if resultado.multi_hand_landmarks:
        for maos_landmarks in resultado.multi_hand_landmarks:
            mp_desenhar.draw_landmarks(frame,maos_landmarks,mp_maos.HAND_CONNECTIONS)
    if not ret:
        print("Frame vazio da camera")
        continue
    cv2.imshow("Camera",frame)
    tecla=cv2.waitKey(1)
    if tecla ==27:
        break
    
        

