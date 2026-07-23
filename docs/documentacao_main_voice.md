# Documentação Técnica: Interface de Voz Continuada ("Voice-First") (`main_voice.py`)

Esta documentação descreve o funcionamento e a arquitetura do script **`main_voice.py`**, localizado em `main_voice.py`. Este módulo fornece a **interface de escuta viva-voz continuada (*Voice-First Hands-Free*)**, escutando o microfone em tempo real, detectando a chamada da assistente (*"Kamila"*), processando intenções via NLU/LLM e respondendo audivelmente.

---

## 1. Visão Geral da Arquitetura

O `main_voice.py` implementa um loop de áudio sem interrupção (pipeline: **Ouvir $\rightarrow$ Processar $\rightarrow$ Falar**).

```mermaid
flowchart TD
    START[Início: python main_voice.py] --> CALIB[Calibração de Ruído Ambiente - 2 segundos]
    CALIB --> TTS_READY[tts.speak 'Estou ouvindo. Pode me chamar.']
    
    TTS_READY --> LOOP[Loop Continuo: recognizer.listen phrase_time_limit=5s]
    LOOP --> STT[recognize_google pt-BR]
    
    STT --> WAKE{Contém 'kamila' ou 'camila'?}
    WAKE -->|Não| LOOP
    WAKE -->|Sim| EXTRACT[Remove wake word do texto]
    
    EXTRACT --> CMD_CHECK{Tem comando restaste?}
    CMD_CHECK -->|Não| SAY_YES[tts.speak 'Sim?' + Escuta por 10s]
    CMD_CHECK -->|Sim| ROUTER[Roteamento de Comandos]
    SAY_YES --> ROUTER
    
    ROUTER -->|registra meu dia| DIARY_VOICE[log_diary - Pergunta e grava diário falado]
    ROUTER -->|novo hábito / fiz hábito| HABIT[Registra hábito na memória]
    ROUTER -->|Geral| LLM[memory_manager.process_interaction]
    
    DIARY_VOICE & HABIT & LLM --> SPEAK_RESP[tts.speak resposta]
    SPEAK_RESP --> LOOP
```

---

## 2. Componentes e Funcionalidades

### 2.1 Calibração de Ruído e Inicialização
- **`recognizer.adjust_for_ambient_noise(source, duration=2)`**: Ajusta os limiares de sensibilidade para evitar acionamentos acidentais em salas ruidosas.
- Emite o aviso audível *"Estou ouvindo. Pode me chamar."*.

---

### 2.2 Tratamento de Interação Simples ("Kamila" $\rightarrow$ "Sim?")
Se o usuário pronunciar apenas o nome *"Kamila"*, a assistente responde imediatamente *"Sim?"* por voz e entra em modo de escuta estendido (tempo limite de 10 segundos) para aguardar o comando.

---

### 2.3 Registro de Diário 100% por Voz (`log_diary`)
Sem necessitar de teclado:
1. Kamila pergunta: *"Vamos lá. O que você fez de importante hoje?"*.
2. Escuta a resposta falada via `listen_for_answer()`.
3. Armazena no banco vetorial de memória com os metadados `{"type": "diary_entry_voice"}`.
4. Responde: *"Salvei seu registro."*.

---

## 3. Como Executar

No terminal com microfone conectado e ambiente virtual ativo:

```bash
python main_voice.py
```
