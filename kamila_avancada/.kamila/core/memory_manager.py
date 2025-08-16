import json
import os
import logging

# Define o nome do arquivo da memória. Ele será criado na mesma pasta do main.py
MEMORY_FILE = 'memory.json'
memory_data = {}

def load_memory():
    """
    Carrega os dados da memória do arquivo JSON ao iniciar.
    Se o arquivo não existir, cria uma memória inicial.
    """
    global memory_data
    # Garante que o caminho seja relativo à pasta principal do projeto
    # (Este ajuste pode ser necessário dependendo de como você executa o script)
    # Por enquanto, vamos assumir que está na mesma pasta do .exe ou script principal.
    
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            logging.info(f"Memória carregada de '{MEMORY_FILE}'.")
        except json.JSONDecodeError:
            logging.error(f"Erro ao decodificar '{MEMORY_FILE}'. Iniciando com memória padrão.")
            _initialize_default_memory()
    else:
        logging.info(f"Arquivo '{MEMORY_FILE}' não encontrado. Criando nova memória.")
        _initialize_default_memory()
        save_memory() # Salva a memória inicial no disco

def _initialize_default_memory():
    """Define os valores iniciais para uma nova memória."""
    global memory_data
    memory_data = {
        'user_name': 'Kauê',
        'interactions': 0,
        'mood': 'neutra', # Estados possíveis: neutra, feliz, prestativa
        'last_interaction_time': None
    }

def save_memory():
    """Salva o estado atual da memória no arquivo JSON."""
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=4, ensure_ascii=False)
        # logging.info("Memória salva.") # Desativado para não poluir o log a cada salvamento
    except Exception as e:
        logging.error(f"Falha ao salvar a memória: {e}")


def update_memory(key, value):
    """
    Atualiza um valor na memória e imediatamente salva no disco.
    Ex: update_memory('interactions', 10)
    """
    global memory_data
    memory_data[key] = value
    save_memory()

def get_from_memory(key, default=None):
    """
    Recupera um valor da memória. Retorna um valor padrão se a chave não existir.
    Ex: user = get_from_memory('user_name', 'amigo')
    """
    return memory_data.get(key, default)

# --- Ação Inicial ---
# Carrega a memória assim que este módulo for importado pela primeira vez.
load_memory()