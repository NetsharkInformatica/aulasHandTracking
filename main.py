import cv2
import mediapipe as mp
import subprocess
import pyautogui

mp_maos= mp.solutions.hands
mp_desenhar= mp.solutions.drawing_utils
maos=mp_maos.Hands()

camera=cv2.VideoCapture(0)
resolucao_x=1024
resolucao_y=768
camera.set(cv2.CAP_PROP_FRAME_WIDTH,resolucao_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,resolucao_y)

#abre programas
processo_notepad=None
processo_mspaint=None
processo_calc=None
processo_vlc= None
caminho_vlc= r"C:\Program Files\VideoLAN\VLC\vlc.exe"
caminho_musica= "musicas/teste.mp3"
#"C:\Program Files\VideoLAN\VLC\vlc.exe"

def tecla_pressionada(tecla):
    pyautogui.press(tecla)
    

def inicia_programa(programa):
    return subprocess.Popen(programa, shell=True)

import os
#fecha Programas

def fecha_programa(nome_processo):
    return os.system(f"TASKKILL /IM {nome_processo} /F")
    


def encontre_coordenada_maos(imagem, lado_invertido=False):
    imagem_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    resultado= maos.process(imagem_rgb)
    todas_maos=[]
    if resultado.multi_hand_landmarks:
        for lado_mao, maos_landmarks in zip(resultado.multi_handedness, resultado.multi_hand_landmarks):
            info_maos={}
            coordenadas=[]
            for mark in maos_landmarks.landmark:
                coordenada_x=int(mark.x * resolucao_x)
                coordenada_y=int(mark.y * resolucao_y)
                coordenada_z= int(mark.z * resolucao_x)
                coordenadas.append((coordenada_x,coordenada_y,coordenada_z))
                info_maos['coordenadas']=coordenadas
            if lado_invertido:
                if lado_mao.classification[0].label == "Left":
                    info_maos["side"]= "Right"
                else:
                    info_maos["side"]="Left"
                    
            else:
                info_maos["side"]= lado_mao.classification[0].label
                
            #print(lado_mao.classification[0].label)
            todas_maos.append(info_maos)
                
            mp_desenhar.draw_landmarks(frame,maos_landmarks,mp_maos.HAND_CONNECTIONS)
            
    return imagem ,todas_maos
    
def dedos_levantados(mao):
    dedos=[]
    for tipodedo in [8,12,16,20]:
        if mao["coordenadas"][tipodedo][1]< mao["coordenadas"][tipodedo-2][1]:
            dedos.append(True)
        else:
            dedos.append(False)
            
    return dedos
    
            


while camera.isOpened():
    ret,frame = camera.read()
    frame=cv2.flip(frame,1)
    
   
    if not ret:
        print("Frame vazio da camera")
        continue
    imagem, todas_maos= encontre_coordenada_maos(frame,False)
    if len(todas_maos)==1:
        info_dedo_mao= dedos_levantados(todas_maos[0])
        #print(f"esse é o {info_dedo_mao}")
        if info_dedo_mao== [True, False,False,True]:
            break
        elif info_dedo_mao==[True,True,False,True]:
            processo_vlc==inicia_programa(f' "{caminho_vlc}" "{caminho_musica}"')
        elif info_dedo_mao == [True,False,False,False] and processo_notepad is None:
            processo_notepad=inicia_programa("notepad")
        elif info_dedo_mao == [True,True,False,False] and processo_calc is None:
            processo_calc=inicia_programa("calc")
        elif info_dedo_mao == [True,True,True,True] and processo_mspaint is None:
            processo_mspaint=inicia_programa("mspaint")
        #fecha programas
        elif info_dedo_mao == [False,False,False,False] :
            if processo_notepad is not None:
                fecha_programa("notepad.exe")
                processo_notepad= None
            elif processo_calc is not None:
                fecha_programa("CalculatorApp.exe")
                processo_calc=None
            elif processo_mspaint is not None:
                fecha_programa("mspaint.exe")
                processo_mspaint=None
                
               
                
            
            
    
    cv2.imshow("Camera",imagem)
    tecla=cv2.waitKey(1)
    if tecla ==27:
        break
    
        

