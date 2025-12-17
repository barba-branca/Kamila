#!/usr/bin/env python3
"""
Kamila Voice - Interface de Voz "Voice-First"
Prioridade: OUVIR -> PENSAR -> FALAR.
"""

import os
import sys
import time
import logging
import threading
from datetime import datetime
import speech_recognition as sr
from dotenv import load_dotenv

# Configuração de Logging Simples
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("KamilaVoice")

def setup_paths():
    """Configura os caminhos."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    sys.path.insert(0, os.path.join(project_root, '.kamila'))
    return project_root

def main():
    setup_paths()
    load_dotenv()
    
    print("\n" + "="*50)
    print("   KAMILA VOICE - MODO ESCUTA ATIVA")
    print("   Diga 'KAMILA' para ativar.")
    print("   Para sair, pressione Ctrl+C no terminal.")
    print("="*50 + "\n")

    # Importação dos módulos Core
    try:
        from kamila_ia_models.llm_interface import LLMInterface
        from core.memory_manager import MemoryManager
        from core.tts_engine import TTSEngine
    except ImportError as e:
        logger.error(f"Erro ao importar módulos: {e}")
        return

    # Inicialização
    logger.info("Inicializando cérebro e voz...")
    try:
        llm_interface = LLMInterface()
        memory_manager = MemoryManager(llm_interface)
        tts = TTSEngine() # Motor de voz
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        
        # Ajuste inicial de ruído
        with mic as source:
            logger.info("Calibrando microfone (fique em silêncio)...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            logger.info("Calibrado.")
            
        tts.speak("Estou ouvindo. Pode me chamar.")
        
    except Exception as e:
        logger.error(f"Falha ao iniciar: {e}")
        return

    # Loop de Escuta Contínua
    while True:
        try:
            print("\n👂 Ouvindo ambiente...", end="\r")
            
            with mic as source:
                # Ouve o áudio (com timeout curto para não travar muito tempo se for silêncio)
                try:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                except sr.WaitTimeoutError:
                    continue

            # Transcrição (Simples e Gratuita via Google)
            try:
                # Usar chave se existir, senão default
                api_key = os.getenv('GOOGLE_API_KEY')
                if api_key and len(api_key) > 10:
                    text = recognizer.recognize_google(audio, key=api_key, language='pt-BR')
                else:
                    text = recognizer.recognize_google(audio, language='pt-BR')
                
                text = text.lower()
                # print(f"DEBUG: Ouvi '{text}'") # Descomente para debug

                # --- Lógica de Wake Word ---
                if "kamila" in text or "camila" in text:
                    logger.info(f"Wake Word detectada em: '{text}'")
                    
                    # Extrair comando (remove a wake word para processar o resto)
                    command = text.replace("kamila", "").replace("camila", "").strip()
                    
                    # Feedback imediato
                    if not command:
                        tts.speak("Sim?")
                        # Ouvir novamente o comando específico
                        with mic as source:
                            print("👂 Aguardando comando...", end="\r")
                            audio_cmd = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                            if api_key and len(api_key) > 10:
                                command = recognizer.recognize_google(audio_cmd, key=api_key, language='pt-BR')
                            else:
                                command = recognizer.recognize_google(audio_cmd, language='pt-BR')
                    
                    if command:
                        logger.info(f"Processando comando: {command}")
                        
                        # Processar Fluxos Específicos por Regex (Mais rápido que LLM)
                        response = None
                        
                        # 1. Diário
                        if "registra meu dia" in command or "registrar meu dia" in command:
                            log_diary(memory_manager, tts, recognizer, mic)
                            continue
                            
                        # 2. Hábitos
                        elif "novo hábito" in command:
                             habit_name = command.split("hábito", 1)[1].strip()
                             memory_manager.store.add_memory(f"Novo hábito criado: {habit_name}", {"type": "habit", "status": "active"})
                             response = f"Hábito {habit_name} criado."
                        
                        elif "fiz " in command and "hábito" in command:
                             # Ex: "fiz hábito beber água" ou "fiz o hábito de..."
                             response = "Registrado. Continue consistente."
                             memory_manager.store.add_memory(f"Hábito realizado: {command}", {"type": "habit_log"})

                        # 3. Brain (LLM) se não for comando simples
                        if not response:
                            response = memory_manager.process_interaction(command)

                        # RESPOSTA FINAL
                        print(f"👩‍💻 Kamila: {response}")
                        tts.speak(response)

            except sr.UnknownValueError:
                # Não entendeu (silêncio ou ruído) -> Ignora
                pass
            except sr.RequestError as e:
                logger.error(f"Erro no serviço de reconhecimento: {e}")
                tts.speak("Estou sem conexão para ouvir.")
            except Exception as e:
                logger.error(f"Erro genérico no loop: {e}")

        except KeyboardInterrupt:
            print("\nEncerrando...")
            tts.speak("Até logo.")
            break

def log_diary(memory_manager, tts, recognizer, mic):
    """Fluxo de diário apenas por VOZ."""
    msg = "Vamos lá. O que você fez de importante hoje?"
    print(f"Kamila: {msg}")
    tts.speak(msg)
    
    # Ouvir resposta
    answer = listen_for_answer(recognizer, mic)
    if not answer:
        tts.speak("Não ouvi nada. Podemos tentar depois.")
        return

    # Salvar
    full_entry = f"Diário (Voz): {answer}"
    memory_manager.store.add_memory(full_entry, {"type": "diary_entry_voice"})
    
    feedback = "Salvei seu registro."
    print(f"Kamila: {feedback}")
    tts.speak(feedback)

def listen_for_answer(recognizer, mic):
    """Auxiliar para ouvir uma resposta."""
    try:
        with mic as source:
            print("👂 (Ouvindo resposta...)", end="\r")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
        text = recognizer.recognize_google(audio, language='pt-BR')
        return text
    except:
        return None

if __name__ == "__main__":
    main()
