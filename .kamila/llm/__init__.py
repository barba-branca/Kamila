# Kamila LLM Package - Large Language Models
"""
Pacote de modelos de linguagem para a assistente Kamila.
Contém integração com Google Gemini AI e outros LLMs.
"""

__version__ = "1.0.0"
__author__ = "Kauê Martins"
__description__ = "Módulos de IA generativa para Kamila"

# Configurações padrão dos LLMs
DEFAULT_MODEL = "gemini-pro"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TIMEOUT = 30

# Modelos suportados
SUPPORTED_MODELS = {
    "gemini-pro": "Google Gemini Pro",
    "gemini-pro-vision": "Google Gemini Pro Vision",
    "ai-studio-palm": "Google AI Studio PaLM",
    "ai-studio-gemini": "Google AI Studio Gemini"
}

def get_available_models():
    """Retorna lista de modelos disponíveis."""
    return list(SUPPORTED_MODELS.keys())

def get_model_info(model_name):
    """Retorna informações de um modelo específico."""
    return SUPPORTED_MODELS.get(model_name, "Modelo não encontrado")

def is_model_available(model_name):
    """Verifica se um modelo está disponível."""
    return model_name in SUPPORTED_MODELS
