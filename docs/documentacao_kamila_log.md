# Documentação Técnica: Arquivo de Log Principal (`.kamila/logs/kamila.log`)

Esta documentação descreve o funcionamento, a estrutura e a utilidade do arquivo **`kamila.log`**, localizado no caminho `.kamila/logs/kamila.log`. Este arquivo armazena a **telemetria contínua, auditoria de execução e histórico de diagnósticos** de todos os módulos da assistente **Kamila**.

---

## 1. Visão Geral e Propósito

O `kamila.log` é mantido dinamicamente pela biblioteca nativa `logging` do Python através de um `FileHandler` configurado nas interfaces de entrada do sistema (`main_voice.py`, `main_cli.py`, `main_with_gemini.py`).

```mermaid
flowchart TD
    SUBGRAPH Módulos Emissores
        STT[core.stt_engine]
        TTS[core.tts_engine]
        NLU[core.interpreter]
        MEM[core.memory_manager]
        ACT[core.actions]
        LLM[llm.gemini_engine]
    END

    SUBGRAPH Logger Central
        STT --> LOG[logging.FileHandler]
        TTS --> LOG
        NLU --> LOG
        MEM --> LOG
        ACT --> LOG
        LLM --> LOG
    END

    LOG --> FILE[.kamila/logs/kamila.log]
```

---

## 2. Padrão de Formatação e Estrutura

Os registros são armazenados sequencialmente em codificação UTF-8, seguindo a estrutura:

```text
YYYY-MM-DD HH:MM:SS,mmm - nome_do_modulo - NÍVEL_DE_LOG - Mensagem do Evento
```

### Exemplo Real de Sequência de Log:

```text
2026-07-23 19:40:01,102 - core.stt_engine - INFO - 🎤 Inicializando STT Engine...
2026-07-23 19:40:02,345 - core.stt_engine - INFO - Microfone configurado: Realtek High Definition Audio
2026-07-23 19:40:02,890 - core.tts_engine - INFO - Volume: 0.9, Velocidade: 180 WPM
2026-07-23 19:40:05,432 - core.stt_engine - INFO - Palavra de ativação detectada!
2026-07-23 19:40:08,765 - core.interpreter - INFO - Intenção identificada: time (Confiança: 1.0)
2026-07-23 19:40:09,123 - core.tts_engine - INFO - Fala concluída com sucesso.
```

---

## 3. Classificação dos Níveis de Log

- **`INFO`**: Eventos operacionais normais (inicializações, conexões com APIs, transcrições concluídas).
- **`DEBUG`**: Rastreamento interno detalhado (ex: requisições em background do Gemini, estado do buffer).
- **`WARNING`**: Alertas que não interrompem o sistema (ex: ausência de chaves de API com alternância para modo simulado).
- **`ERROR`**: Exceções capturadas e falhas de rede (ex: erros na API do Google Speech ou timeout).
- **`CRITICAL`**: Falhas graves que impedem o funcionamento da assistente (ex: microfone não encontrado).

---

## 4. Manutenção e Segurança

> [!NOTE]
> **Privacidade & Git Hygiene**: O arquivo `kamila.log` registra interações e mensagens em tempo real da assistente. Por essa razão, ele é protegido pelo arquivo `.gitignore` (`*.log`) e **não é sincronizado com o repositório remoto Git**.
