# Kamila Assistant - Package Principal
"""
Pacote principal da assistente virtual Kamila.
Contém todos os módulos core e funcionalidades avançadas.
"""

__version__ = "2.0.0"
__author__ = "Kauê Martins"
__description__ = "Assistente Virtual com IA e Voz"

# Configurações globais
DEFAULT_WAKE_WORD = "kamila"
DEFAULT_LANGUAGE = "pt-BR"
DEFAULT_TIMEOUT = 30

# Status do sistema
SYSTEM_STATUS = {
    "initialized": False,
    "wake_word_detected": False,
    "processing_command": False,
    "last_interaction": None
}

def get_system_info():
    """Retorna informações do sistema."""
    return {
        "name": "Kamila Assistant",
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "wake_word": DEFAULT_WAKE_WORD,
        "language": DEFAULT_LANGUAGE
    }

def initialize_system():
    """Inicializa o sistema Kamila."""
    global SYSTEM_STATUS
    SYSTEM_STATUS["initialized"] = True
    SYSTEM_STATUS["last_interaction"] = None
    return True
