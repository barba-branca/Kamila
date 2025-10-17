import face_recognition
import cv2
import numpy as np
import os
import pyautogui
import time
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
jload_dotenv('.env')
        
# --- CONFIGURAÇÃO ---
KNOWN_USER_IMAGE = "kaue.jpg"

KNOWN_USER_NAME = "Kauê"

WINDOWS_PASSWORD = "SENHA" 

KAMILA_API_URL = "http://127.0.0.1:5000/trigger_greeting" 
# --------------------

print("Iniciando sistema de desbloqueio facial...")

# Carrega a sua foto e aprende a te reconhecer
try:
    user_image = face_recognition.load_image_file(os.path.join("auth", KNOWN_USER_IMAGE))
    user_face_encoding = face_recognition.face_encodings(user_image)[0]
    print(f"Rosto de '{KNOWN_USER_NAME}' carregado e codificado com sucesso.")
except Exception as e:
    print(f"ERRO: Não foi possível carregar a imagem de autenticação '{KNOWN_USER_IMAGE}'. {e}")
    exit()

known_face_encodings = [user_face_encoding]
known_face_names = [KNOWN_USER_NAME]

video_capture = cv2.VideoCapture(0)

print("Sistema ativo. Procurando por rosto conhecido na webcam...")

face_recognized = False

while not face_recognized:
    ret, frame = video_capture.read()
    if not ret:
        continue

    # Encontra todos os rostos no frame atual da webcam
    rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        # Vê se o rosto encontrado combina com o seu
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Desconhecido"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            
            if name == KNOWN_USER_NAME:
                print(f"BEM-VINDO, {KNOWN_USER_NAME}! Desbloqueando o sistema...")
                face_recognized = True
                
                # Simula o pressionar de uma tecla para ativar a tela de senha
                pyautogui.press('enter') 
                time.sleep(1) # Espera a tela de senha aparecer

                # Digita a senha
                pyautogui.typewrite(WINDOWS_PASSWORD)
                pyautogui.press('enter')
                
                print("Sistema desbloqueado.")
                
                # Espera o desktop carregar um pouco
                time.sleep(5) 
                
                # Tenta notificar a Kamila para fazer a saudação
                try:
                    print("Notificando a Kamila para fazer a saudação...")
                    requests.post(KAMILA_API_URL, json={'user': KNOWN_USER_NAME})
                except Exception as e:
                    print(f"Não foi possível notificar a Kamila. Ela está rodando? Erro: {e}")
                
                break
    if face_recognized:
        break

# Libera a câmera e fecha tudo
video_capture.release()
cv2.destroyAllWindows()
print("Sistema de desbloqueio facial encerrado.")