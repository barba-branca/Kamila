# Documentação Técnica: Motor de Fala para Texto Principal (`.kamila/core/stt_engine.py`)

Esta documentação detalha o funcionamento do módulo **`stt_engine.py`**, representado pela classe `STTEngine`. Este é o **motor principal de Speech-to-Text (STT) de produção** da assistente **Kamila**, projetado para suportar escuta contínua assíncrona, tolerância a falhas na API de voz e gerenciamento multithreaded de entrada de áudio.

---

## 1. Visão Geral da Arquitetura

O `stt_engine.py` utiliza a biblioteca **PyAudio** para captura contínua em tempo real de frames PCM de 16kHz, avaliados pelo **Picovoice Porcupine**. Ao detectar a palavra de ativação (*Wake Word* *"Kamila"*), ele libera o dispositivo de áudio e transfere a captura para o **Google Speech Recognition** de forma não bloqueante (`ThreadPoolExecutor`).

```mermaid
flowchart TD
    subgraph Escuta Contínua em Background (Thread Daemon)
        PA[PyAudio - Stream PCM 16kHz] --> FRAME[Leitura de Frames PCM]
        FRAME --> PORC[Porcupine.process - Modelo .ppn]
        PORC -->|Wake Word Detectada| PAUSE[Pausa Stream PyAudio]
    end

    subgraph Captura de Comando & Redefinição
        PAUSE --> CB[Callback de Ativação - main_voice]
        CB --> MIC[SpeechRecognition.listen]
        MIC --> POOL[ThreadPoolExecutor - recognize_task]
    end

    subgraph Sistema de Fallback da API
        POOL --> API1{GOOGLE_API_KEY Ativa?}
        API1 -->|Sim| RECOG1[recognize_google com API Key]
        API1 -->|Erro / Não| RECOG2[recognize_google Padrão Gratuito]
        RECOG1 --> CMD[Comando Transcrito]
        RECOG2 --> CMD
    end
```

---

## 2. Parâmetros de Configuração Manual do Microfone

Para garantir alta estabilidade em ambientes ruidosos e evitar cortes prematuros de frases longas, a calibração de áudio é definida com parâmetros manuais estáticos:

```python
self.recognizer.dynamic_energy_threshold = False  # Desativa ajuste volátil
self.recognizer.energy_threshold = 400            # Limiar fixo de energia sonora
self.recognizer.pause_threshold = 1.5             # Aguarda 1.5s de silêncio para encerrar a frase
```

---

## 3. Detalhamento dos Métodos da Classe `STTEngine`

### 3.1 Construtor (`__init__`)
```python
def __init__(self, wake_word="kamila"):
```
- **Inicialização**:
  - Instancia o reconhecedor `sr.Recognizer()`.
  - Inicializa o `ThreadPoolExecutor(max_workers=1)` para I/O assíncrono de rede.
  - Invoca `_setup_microphone()` e `_setup_porcupine()`.

---

### 3.2 `_setup_microphone()`
- Filtra a lista de microfones disponíveis para evitar seletores virtuais ou mapeadores genéricos do Windows (`"mapeador"`, `"mapper"`).
- Define o microfone no dispositivo físico com taxa de amostragem de 16.000 Hz (`sample_rate=16000`).

---

### 3.3 `_setup_porcupine()`
- Carrega as chaves e modelos de ativação de voz dos diretórios locais:
  - **Parâmetros de Idioma**: `models/porcupine_models/porcupine_params_pt.pv`
  - **Modelo da Palavra-Chave**: `models/wake_words/camila_pt_windows_v3_0_0.ppn`
- Inicializa a instância `create_porcupine` usando a chave de acesso `PICOVOICE_ACCESS_KEY`.

---

### 3.4 Gerenciamento da Escuta em Background (`start_listening` & `_listen_loop`)

```python
def start_listening(self, callback):
```
- Inicia uma *thread* daemon dedicada (`_listen_loop`) que abre um stream PCM raw com PyAudio.
- O loop lê blocos de áudio (`frame_length`) e descompacta os inteiros curtos de 16 bits via `struct.unpack_from`.
- Quando `porcupine.process(pcm)` retorna a detecção (`keyword_index >= 0`):
  1. O stream de áudio do PyAudio é interrompido e fechado para liberar a placa de som.
  2. Executa a função `callback()` síncrona enviada como parâmetro.
  3. Reabre o stream do PyAudio após o término da interação de voz.

---

### 3.5 Processamento Assíncrono do Comando (`listen_for_command_async`)

```python
def listen_for_command_async(self, timeout=10):
```
- Captura até 15 segundos de frase do usuário com `self.recognizer.listen(source, timeout=10, phrase_time_limit=15)`.
- Submete a tarefa de requisição de rede ao `ThreadPoolExecutor`, retornando um objeto `concurrent.futures.Future`.
- **Estratégia Resiliente de Fallback**:
  1. **Nível 1**: Tenta efetuar a requisição usando a chave cadastrada em `GOOGLE_API_KEY`.
  2. **Nível 2 (Fallback)**: Caso ocorra erro de requisição (`sr.RequestError`), como chave inválida ou cota excedida, tenta automaticamente o endpoint público do Google STT (`key=None`).

---

### 3.6 Desalocação de Recursos (`cleanup`)

```python
def cleanup(self):
```
- Para o loop de escuta (`stop_listening()`).
- Deleta a instância do Porcupine em memória (`self.porcupine.delete()`).
- Desliga a piscina de threads (`self.executor.shutdown(wait=False)`).
