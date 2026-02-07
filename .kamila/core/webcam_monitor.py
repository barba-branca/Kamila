#!/usr/bin/env python3
"""
Webcam Monitor - Sistema de Monitoramento por Webcam para Kamila
Detecta convulsões e quedas através de análise de movimento e posição.
"""

import cv2
import numpy as np
import threading
import time
import logging
from datetime import datetime
from typing import Optional, Callable, Tuple
import os

logger = logging.getLogger(__name__)

# Tentar importar MediaPipe para detecção facial avançada
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logger.warning("MediaPipe não disponível. Detecção de piscadas desativada.")

class WebcamMonitor:
    """Sistema de monitoramento por webcam para detecção de emergências."""

    def __init__(self, tts_engine=None):
        """
        Inicializa o monitor de webcam.

        Args:
            tts_engine: Instância do motor TTS para alertas de voz
        """
        logger.info("🚨 Inicializando Webcam Monitor...")

        self.tts_engine = tts_engine
        self.is_monitoring = False
        self.monitor_thread = None
        self.cap = None

        # Configurações de detecção
        self.motion_threshold = 1000  # Threshold para movimento
        self.fall_threshold = 0.3     # Threshold para altura (proporção da tela)
        self.consecutive_frames = 5   # Frames consecutivos para confirmar detecção
        self.alert_cooldown = 30      # Segundos entre alertas

        # Configurações de Face Mesh (Blink Detection)
        self.blink_threshold = 0.5  # EAR (Eye Aspect Ratio) threshold
        self.blink_limit = 3 # Blinks por segundo para considerar anormal
        self.eye_closed = False

        # Estado de detecção
        self.last_alert_time = 0
        self.fall_detected = False
        self.seizure_detected = False
        self.background_subtractor = None

        # Inicializar MediaPipe Face Mesh se disponível
        if MEDIAPIPE_AVAILABLE:
            self.mp_face_mesh = mp.solutions.face_mesh
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            # Índices dos landmarks dos olhos
            self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
            self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]

        # Callback para alertas
        self.alert_callback = None

        # Modo de saúde intensivo
        self.health_mode = False

        logger.info("✅ Webcam Monitor inicializado!")

    def _speak_async(self, text):
        """Executa a fala em uma thread separada para não bloquear o monitoramento."""
        if self.tts_engine:
            threading.Thread(target=self.tts_engine.speak, args=(text,), daemon=True).start()

    def start_monitoring(self, alert_callback: Optional[Callable] = None):
        """
        Inicia o monitoramento contínuo da webcam.

        Args:
            alert_callback: Função a ser chamada quando uma emergência for detectada
        """
        if self.is_monitoring:
            logger.warning("⚠️ Monitoramento já está ativo")
            return False

        try:
            # Inicializar câmera
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                logger.error("❌ Não foi possível acessar a webcam")
                return False

            # Configurar resolução
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            # Inicializar background subtractor
            self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
                history=100, varThreshold=50, detectShadows=True
            )

            self.alert_callback = alert_callback
            self.is_monitoring = True

            # Iniciar thread de monitoramento
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()

            logger.info("🎥 Monitoramento iniciado com sucesso!")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao iniciar monitoramento: {e}")
            self.cleanup()
            return False

    def stop_monitoring(self):
        """Para o monitoramento da webcam."""
        if not self.is_monitoring:
            return

        logger.info("🛑 Parando monitoramento...")
        self.is_monitoring = False

        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)

        self.cleanup()

    def _monitor_loop(self):
        """Loop principal de monitoramento."""
        logger.info("🔄 Iniciando loop de monitoramento...")

        consecutive_motion = 0
        consecutive_fall = 0

        # Blink detection state
        blink_counter = 0
        blink_start_time = time.time()
        self.eye_closed = False

        try:
            while self.is_monitoring and self.cap:
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("⚠️ Falha ao capturar frame")
                    time.sleep(1)
                    continue

                # Processar frame
                processed_frame, motion_detected, fall_detected, eye_is_closed_now = self._process_frame(frame)

                # --- Análise de Movimento (Convulsão Generalizada) ---
                if motion_detected:
                    consecutive_motion += 1
                else:
                    consecutive_motion = 0

                # --- Análise de Queda ---
                if fall_detected:
                    consecutive_fall += 1
                else:
                    consecutive_fall = 0

                # --- Análise de Piscadas (Sintoma de Crise Focal) ---
                # Detecta a transição de aberto para fechado (início da piscada)
                if eye_is_closed_now and not self.eye_closed:
                    self.eye_closed = True
                elif not eye_is_closed_now and self.eye_closed:
                    self.eye_closed = False
                    blink_counter += 1 # Conta piscada completa (fechou e abriu)

                # Verificar taxa de piscadas por segundo (janela deslizante simples)
                if time.time() - blink_start_time >= 1.0:
                    if blink_counter > self.blink_limit:
                        logger.warning(f"⚠️ Piscadas excessivas detectadas: {blink_counter}/s")
                        self._handle_blink_alert(blink_counter)

                    # Resetar contador e timer para o próximo segundo
                    blink_counter = 0
                    blink_start_time = time.time()


                # Verificar detecções e disparar alertas
                if consecutive_motion >= self.consecutive_frames * 2: # Mais sensível a movimento contínuo
                     # Só dispara se o movimento for muito intenso (convulsão)
                     # Aqui seria ideal uma lógica mais complexa de tremor, mas movimento contínuo é um proxy
                    self._handle_seizure_detection()
                    consecutive_motion = 0

                if consecutive_fall >= self.consecutive_frames:
                    self._handle_fall_detection()
                    consecutive_fall = 0

                # Pequena pausa
                time.sleep(0.05)

        except Exception as e:
            logger.error(f"❌ Erro no loop de monitoramento: {e}")
        finally:
            self.cleanup()

    def _process_frame(self, frame) -> Tuple[np.ndarray, bool, bool, bool]:
        """
        Processa um frame para detecção de movimento, queda e estado do olho.
        Returns:
            frame, motion_detected, fall_detected, eye_is_closed
        """
        try:
            # Redimensionar frame
            frame = cv2.resize(frame, (640, 480))

            # --- Detecção Facial e de Piscadas (MediaPipe) ---
            eye_is_closed = False
            if MEDIAPIPE_AVAILABLE:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_mesh.process(frame_rgb)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        # Calcular EAR (Eye Aspect Ratio)
                        left_ear = self._calculate_ear(face_landmarks.landmark, self.LEFT_EYE)
                        right_ear = self._calculate_ear(face_landmarks.landmark, self.RIGHT_EYE)

                        avg_ear = (left_ear + right_ear) / 2.0

                        # Se EAR < threshold, olho está fechado
                        if avg_ear < 0.2: # Threshold empírico
                             eye_is_closed = True

            # --- Detecção de Movimento e Queda (CV2 Clássico) ---
            # Converter para grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # Background subtraction
            if self.background_subtractor:
                fg_mask = self.background_subtractor.apply(gray)
                fg_mask = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY)[1]
                kernel = np.ones((5, 5), np.uint8)
                fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)
            else:
                fg_mask = np.zeros_like(gray)

            motion_detected = self._detect_motion(fg_mask)
            fall_detected = self._detect_fall(frame, fg_mask)

            self._draw_detection_info(frame, motion_detected, fall_detected, eye_is_closed)

            return frame, motion_detected, fall_detected, eye_is_closed

        except Exception as e:
            logger.error(f"❌ Erro ao processar frame: {e}")
            return frame, False, False, False

    def _calculate_ear(self, landmarks, eye_indices):
        """Calcula o Eye Aspect Ratio."""
        # Pontos verticais
        A = np.linalg.norm(np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y]) -
                           np.array([landmarks[eye_indices[5]].x, landmarks[eye_indices[5]].y]))
        B = np.linalg.norm(np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y]) -
                           np.array([landmarks[eye_indices[4]].x, landmarks[eye_indices[4]].y]))

        # Pontos horizontais
        C = np.linalg.norm(np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y]) -
                           np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y]))

        ear = (A + B) / (2.0 * C)
        return ear

    def _detect_motion(self, fg_mask) -> bool:
        """Detecta movimento significativo."""
        try:
            motion_area = np.sum(fg_mask > 0)
            return motion_area > self.motion_threshold
        except Exception:
            return False

    def _detect_fall(self, frame, fg_mask) -> bool:
        """Detecta possível queda."""
        try:
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours: return False

            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            frame_height = frame.shape[0]
            relative_height = (y + h) / frame_height

            motion_area = np.sum(fg_mask > 0)
            # Queda se está baixo e há movimento
            return (relative_height > (1 - self.fall_threshold)) and (motion_area > 500)
        except Exception:
            return False

    def _draw_detection_info(self, frame, motion_detected, fall_detected, eye_is_closed):
        """Desenha informações no frame."""
        try:
            status = "MONITORANDO" if self.is_monitoring else "PARADO"
            cv2.putText(frame, f"Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if motion_detected:
                cv2.putText(frame, "MOVIMENTO!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if fall_detected:
                cv2.putText(frame, "QUEDA!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if eye_is_closed:
                cv2.putText(frame, "OLHO FECHADO", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            timestamp = datetime.now().strftime("%H:%M:%S")
            cv2.putText(frame, f"Time: {timestamp}", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        except Exception:
            pass

    def _handle_seizure_detection(self):
        """Manipula detecção de convulsão."""
        current_time = time.time()
        if (current_time - self.last_alert_time) < self.alert_cooldown:
            return

        self.last_alert_time = current_time
        self.seizure_detected = True
        logger.warning("🚨 CONVULSÃO DETECTADA!")
        self._speak_async("Atenção! Detectei uma possível convulsão! Pedindo ajuda!")
        if self.alert_callback:
            self.alert_callback("seizure", "Detectei uma possível convulsão!")

    def _handle_fall_detection(self):
        """Manipula detecção de queda."""
        current_time = time.time()
        if (current_time - self.last_alert_time) < self.alert_cooldown:
            return

        self.last_alert_time = current_time
        self.fall_detected = True
        logger.warning("🚨 QUEDA DETECTADA!")
        self._speak_async("Atenção! Detectei uma possível queda! Pedindo ajuda!")
        if self.alert_callback:
            self.alert_callback("fall", "Detectei uma possível queda!")

    def _handle_blink_alert(self, count):
        """Manipula alerta de piscadas excessivas."""
        current_time = time.time()
        # Cooldown menor para piscadas
        if (current_time - self.last_alert_time) < 10:
             return

        self.last_alert_time = current_time
        logger.warning(f"🚨 PISCADAS EXCESSIVAS: {count}/s")
        self._speak_async(f"Estou detectando muitas piscadas. Você está bem?")
        if self.alert_callback:
            self.alert_callback("blink_rate", f"Taxa de piscadas elevada: {count}/s")

    def set_motion_threshold(self, threshold: int):
        self.motion_threshold = max(100, min(10000, threshold))

    def set_fall_threshold(self, threshold: float):
        self.fall_threshold = max(0.1, min(0.8, threshold))

    def set_alert_cooldown(self, cooldown: int):
        self.alert_cooldown = max(10, cooldown)

    def get_status(self) -> dict:
        return {
            "is_monitoring": self.is_monitoring,
            "motion_threshold": self.motion_threshold,
            "fall_threshold": self.fall_threshold,
            "seizure_detected": self.seizure_detected,
            "fall_detected": self.fall_detected,
            "health_mode": self.health_mode
        }

    def set_health_mode(self, enabled: bool):
        self.health_mode = enabled
        if enabled:
            self.motion_threshold = 500
            self.fall_threshold = 0.2
            self.alert_cooldown = 15
            logger.info("🏥 Modo de saúde intensivo ativado!")
        else:
            self.motion_threshold = 1000
            self.fall_threshold = 0.3
            self.alert_cooldown = 30
            logger.info("🏥 Modo de saúde intensivo desativado!")

    def cleanup(self):
        logger.info("🧹 Limpando Webcam Monitor...")
        self.is_monitoring = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.background_subtractor:
            self.background_subtractor = None
        if MEDIAPIPE_AVAILABLE:
            self.face_mesh.close()
        logger.info("✅ Webcam Monitor limpo!")
