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

        # Estado de detecção
        self.last_alert_time = 0
        self.fall_detected = False
        self.seizure_detected = False
        self.background_subtractor = None

        # Callback para alertas
        self.alert_callback = None

        # Modo de saúde intensivo
        self.health_mode = False

        logger.info("✅ Webcam Monitor inicializado!")

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

        try:
            while self.is_monitoring and self.cap:
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("⚠️ Falha ao capturar frame")
                    time.sleep(1)
                    continue

                # Processar frame
                processed_frame, motion_detected, fall_detected = self._process_frame(frame)

                # Contar frames consecutivos
                if motion_detected:
                    consecutive_motion += 1
                else:
                    consecutive_motion = 0

                if fall_detected:
                    consecutive_fall += 1
                else:
                    consecutive_fall = 0

                # Verificar detecções
                if consecutive_motion >= self.consecutive_frames:
                    self._handle_seizure_detection()
                    consecutive_motion = 0  # Reset após alerta

                if consecutive_fall >= self.consecutive_frames:
                    self._handle_fall_detection()
                    consecutive_fall = 0  # Reset após alerta

                # Pequena pausa
                time.sleep(0.1)

        except Exception as e:
            logger.error(f"❌ Erro no loop de monitoramento: {e}")
        finally:
            self.cleanup()

    def _process_frame(self, frame) -> Tuple[np.ndarray, bool, bool]:
        """
        Processa um frame para detecção de movimento e queda.

        Args:
            frame: Frame da webcam

        Returns:
            Tuple: (frame_processado, movimento_detectado, queda_detectada)
        """
        try:
            # Redimensionar frame
            frame = cv2.resize(frame, (640, 480))

            # Converter para grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # Background subtraction
            if self.background_subtractor:
                fg_mask = self.background_subtractor.apply(gray)
                fg_mask = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY)[1]
                # Criar kernel para dilatação
                kernel = np.ones((5, 5), np.uint8)
                fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)
            else:
                fg_mask = np.zeros_like(gray)

            # Detectar movimento
            motion_detected = self._detect_motion(fg_mask)

            # Detectar queda
            fall_detected = self._detect_fall(frame, fg_mask)

            # Desenhar informações no frame
            self._draw_detection_info(frame, motion_detected, fall_detected)

            return frame, motion_detected, fall_detected

        except Exception as e:
            logger.error(f"❌ Erro ao processar frame: {e}")
            return frame, False, False

    def _detect_motion(self, fg_mask) -> bool:
        """
        Detecta movimento baseado na máscara de foreground.

        Args:
            fg_mask: Máscara de foreground

        Returns:
            bool: True se movimento significativo detectado
        """
        try:
            # Calcular área de movimento
            motion_area = np.sum(fg_mask > 0)

            # Verificar se excede threshold
            return motion_area > self.motion_threshold

        except Exception as e:
            logger.error(f"❌ Erro na detecção de movimento: {e}")
            return False

    def _detect_fall(self, frame, fg_mask) -> bool:
        """
        Detecta possível queda baseada na posição e movimento.

        Args:
            frame: Frame original
            fg_mask: Máscara de foreground

        Returns:
            bool: True se queda detectada
        """
        try:
            # Encontrar contornos
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if not contours:
                return False

            # Pegar o maior contorno (provavelmente a pessoa)
            largest_contour = max(contours, key=cv2.contourArea)

            # Calcular bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Calcular altura relativa (queda se pessoa está baixa na tela)
            frame_height = frame.shape[0]
            relative_height = (y + h) / frame_height

            # Considerar queda se a pessoa está na parte inferior da tela
            # e há movimento significativo
            motion_area = np.sum(fg_mask > 0)
            is_fallen = (relative_height > (1 - self.fall_threshold)) and (motion_area > 500)

            return is_fallen

        except Exception as e:
            logger.error(f"❌ Erro na detecção de queda: {e}")
            return False

    def _draw_detection_info(self, frame, motion_detected, fall_detected):
        """
        Desenha informações de detecção no frame.

        Args:
            frame: Frame para desenhar
            motion_detected: Se movimento foi detectado
            fall_detected: Se queda foi detectada
        """
        try:
            # Status de monitoramento
            status = "MONITORANDO" if self.is_monitoring else "PARADO"
            cv2.putText(frame, f"Status: {status}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Indicadores de detecção
            if motion_detected:
                cv2.putText(frame, "MOVIMENTO DETECTADO!", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            if fall_detected:
                cv2.putText(frame, "QUEDA DETECTADA!", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")
            cv2.putText(frame, f"Time: {timestamp}", (10, frame.shape[0] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        except Exception as e:
            logger.error(f"❌ Erro ao desenhar informações: {e}")

    def _handle_seizure_detection(self):
        """Manipula detecção de convulsão."""
        try:
            current_time = time.time()

            # Verificar cooldown
            if (current_time - self.last_alert_time) < self.alert_cooldown:
                return

            self.last_alert_time = current_time
            self.seizure_detected = True

            logger.warning("🚨 CONVULSÃO DETECTADA!")

            # Alerta de voz
            if self.tts_engine:
                self.tts_engine.speak("Atenção! Detectei uma possível convulsão! Pedindo ajuda!")

            # Callback personalizado
            if self.alert_callback:
                self.alert_callback("seizure", "Detectei uma possível convulsão!")

        except Exception as e:
            logger.error(f"❌ Erro ao manipular detecção de convulsão: {e}")

    def _handle_fall_detection(self):
        """Manipula detecção de queda."""
        try:
            current_time = time.time()

            # Verificar cooldown
            if (current_time - self.last_alert_time) < self.alert_cooldown:
                return

            self.last_alert_time = current_time
            self.fall_detected = True

            logger.warning("🚨 QUEDA DETECTADA!")

            # Alerta de voz
            if self.tts_engine:
                self.tts_engine.speak("Atenção! Detectei uma possível queda! Pedindo ajuda!")

            # Callback personalizado
            if self.alert_callback:
                self.alert_callback("fall", "Detectei uma possível queda!")

        except Exception as e:
            logger.error(f"❌ Erro ao manipular detecção de queda: {e}")

    def set_motion_threshold(self, threshold: int):
        """
        Define o threshold para detecção de movimento.

        Args:
            threshold (int): Novo threshold
        """
        self.motion_threshold = max(100, min(10000, threshold))
        logger.info(f"🔧 Motion threshold alterado para: {self.motion_threshold}")

    def set_fall_threshold(self, threshold: float):
        """
        Define o threshold para detecção de queda.

        Args:
            threshold (float): Novo threshold (0.0 a 1.0)
        """
        self.fall_threshold = max(0.1, min(0.8, threshold))
        logger.info(f"🔧 Fall threshold alterado para: {self.fall_threshold}")

    def set_alert_cooldown(self, cooldown: int):
        """
        Define o cooldown entre alertas.

        Args:
            cooldown (int): Cooldown em segundos
        """
        self.alert_cooldown = max(10, cooldown)
        logger.info(f"🔧 Alert cooldown alterado para: {self.alert_cooldown}s")

    def get_status(self) -> dict:
        """Retorna status atual do monitor."""
        return {
            "is_monitoring": self.is_monitoring,
            "motion_threshold": self.motion_threshold,
            "fall_threshold": self.fall_threshold,
            "alert_cooldown": self.alert_cooldown,
            "last_alert_time": self.last_alert_time,
            "seizure_detected": self.seizure_detected,
            "fall_detected": self.fall_detected,
            "health_mode": self.health_mode
        }

    def set_health_mode(self, enabled: bool):
        """
        Ativa ou desativa o modo de saúde intensivo.

        Args:
            enabled (bool): True para ativar, False para desativar
        """
        self.health_mode = enabled

        if enabled:
            # Configurações mais sensíveis para modo de saúde
            self.motion_threshold = 500  # Threshold mais baixo
            self.fall_threshold = 0.2    # Threshold mais sensível para quedas
            self.alert_cooldown = 15     # Cooldown menor para alertas mais rápidos
            logger.info("🏥 Modo de saúde intensivo ativado!")
        else:
            # Configurações padrão
            self.motion_threshold = 1000
            self.fall_threshold = 0.3
            self.alert_cooldown = 30
            logger.info("🏥 Modo de saúde intensivo desativado!")

    def cleanup(self):
        """Limpa recursos do monitor."""
        logger.info("🧹 Limpando Webcam Monitor...")

        self.is_monitoring = False

        if self.cap and self.cap.isOpened():
            self.cap.release()

        if self.background_subtractor:
            self.background_subtractor = None

        logger.info("✅ Webcam Monitor limpo!")
