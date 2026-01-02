import face_recognition
import cv2
import numpy as np
import os
import pyautogui
import time
import requests
import pyperclip
from dotenv import load_dotenv

pyautogui.FAILSAFE = False

# Carregar variáveis de ambiente
load_dotenv('KAMILA/.env')
        
# --- CONFIGURAÇÃO ---
KNOWN_USER_IMAGE = "kaue.jpg"

KNOWN_USER_NAME = "kaue martins"

WINDOWS_PASSWORD = "2020" 

KAMILA_API_URL = "http://127.0.0.1:5000/trigger_greeting" 
# --------------------

print("Iniciando sistema de desbloqueio facial...")

# Carrega a sua foto e aprende a te reconhecer
try:
    print(f"Carregando a imagem de '{os.path.join('auth', KNOWN_USER_IMAGE)}'...")
    user_image = face_recognition.load_image_file(os.path.join("auth", KNOWN_USER_IMAGE))
    
    print("Codificando o rosto. Isso pode levar um momento...")
    face_encodings_list = face_recognition.face_encodings(user_image)
    
    # --- VERIFICAÇÃO PRINCIPAL ---
    if not face_encodings_list:
        print("\n!!! ERRO CRÍTICO !!!")
        print(f"Nenhum rosto foi detectado na imagem '{KNOWN_USER_IMAGE}'.")
        print("Dicas:")
        print(" - Use uma foto clara e de frente (como uma selfie ou foto 3x4).")
        print(" - Garanta que o rosto não esteja de lado ou coberto.")
        print(" - A imagem deve ter uma boa iluminação.")
        exit()

    user_face_encoding = face_encodings_list[0]
    print(f"Rosto de '{KNOWN_USER_NAME}' carregado e codificado com sucesso.")
    
except FileNotFoundError:
    print(f"\nERRO: A foto '{KNOWN_USER_IMAGE}' não foi encontrada na pasta 'auth'.")
    exit()
except Exception as e:
    print(f"ERRO inesperado ao processar a imagem: {e}")
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
                
                print("Aguarde 2 segundos antes da automação...")
                time.sleep(2)

                # --- LÓGICA DE DESBLOQUEIO FINAL (VIA COPY & PASTE) ---

                # 1. Copia a senha para a área de transferência.
                #    Esta é uma abordagem mais robusta contra bloqueios da UI.
                print("Copiando a senha para a área de transferência...")
                pyperclip.copy(WINDOWS_PASSWORD)

                # 2. Ativa a tela de senha.
                print("Ativando a tela de senha e aguardando...")
                pyautogui.press('enter')
                time.sleep(1.5) # Damos tempo para a tela de senha carregar

                # 3. Clica no meio da tela para garantir foco no campo da senha
                screenWidth, screenHeight = pyautogui.size()
                pyautogui.click(screenWidth / 2, screenHeight / 2)
                time.sleep(0.5)

                # 4. Usa o atalho 'ctrl + v' para colar a senha
                print("Colando a senha...")
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                
                # 5. Limpa a área de transferência por segurança
                pyperclip.copy('') 

                # 6. Pressiona Enter para logar
                print("Pressionando Enter para logar...")
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