# Documentação Técnica: Suíte de Integração Completa (`.kamila/test_full_integration.py`)

Esta documentação descreve em detalhes o funcionamento da suíte de testes **`test_full_integration.py`**, localizada em `.kamila/test_full_integration.py`. Este script executa a **auditoria ponta a ponta (*End-to-End*) do pipeline da Kamila**, testando desde o reconhecimento de voz inicial até o registro histórico em memória.

---

## 1. Visão Geral da Arquitetura do Teste

O `test_full_integration.py` testa isoladamente cada motor e, em seguida, executa o fluxo encadeado completo em `test_full_pipeline()`:

```mermaid
flowchart TD
    SUBGRAPH 1. Testes de Motores Isolados
        T_STT[test_stt_only - Escuta de Voz]
        T_TTS[test_tts_only - Síntese Vocal]
        T_INT[test_interpreter_only - NLU / Intenções]
        T_ACT[test_actions_only - Execução de Ações]
        T_GEM[test_gemini_only - Inferência Gemini LLM]
    END

    SUBGRAPH 2. Pipeline Integrado Completo
        T_STT --> T_PIPE[test_full_pipeline]
        T_TTS --> T_PIPE
        T_INT --> T_PIPE
        T_ACT --> T_PIPE
        T_GEM --> T_PIPE
        
        T_PIPE -->|1. NLU| INT_STEP[CommandInterpreter.interpret_command]
        INT_STEP -->|2. Ação| ACT_STEP[ActionManager.execute_action]
        ACT_STEP -->|3. Fallback LLM| GEM_STEP[GeminiEngine.chat]
        GEM_STEP -->|4. Áudio| TTS_STEP[TTSEngine.speak]
        TTS_STEP -->|5. Memória| MEM_STEP[MemoryManager.add_interaction]
    END

    T_PIPE --> SUMMARY[Relatório de Resultados no Terminal]
```

---

## 2. Como Executar o Teste de Integração

No terminal, com o ambiente virtual ativado:

```bash
python .kamila/test_full_integration.py
```

---

## 3. Detalhamento dos Módulos de Teste

| Nome da Função | Módulo Avaliado | Validação Realizada |
| :--- | :--- | :--- |
| **`test_stt_only()`** | `core.stt_engine` | Tenta capturar 3 segundos de áudio do microfone físico. |
| **`test_tts_only()`** | `core.tts_engine` | Sintetiza a frase de validação *"Olá! Teste de voz funcionando!"*. |
| **`test_interpreter_only()`** | `core.interpreter` | Avalia 5 comandos de exemplo e imprime as intenções detectadas. |
| **`test_actions_only()`** | `core.actions` | Instancia `ActionManager(tts)` e executa as ações de tempo e status. |
| **`test_gemini_only()`** | `llm.gemini_engine` | Envia um prompt em nuvem e valida se a resposta do Gemini não está vazia. |
| **`test_full_pipeline()`** | Pipeline Completo | Encadeia NLU → Ação → Fallback LLM → TTS → Memória para o comando *"que horas são"*. |

---

## 4. Estrutura do Relatório Final (`main`)

Após tentar executar todas as suítes, o script emite a contagem consolidada:

```text
==================================================
📊 RESULTADOS FINAIS:
✅ STT Only
✅ TTS Only
✅ Interpreter Only
✅ Actions Only
✅ Gemini Only
✅ Full Pipeline

🎯 Total: 6/6 testes passaram
🎉 Todos os testes passaram! Integração completa funcionando.
```
