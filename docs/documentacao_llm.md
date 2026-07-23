# Documentação Técnica: Módulo de Modelos de Linguagem LLM (`.kamila/llm/`)

Esta documentação descreve em detalhes a estrutura, os motores e as integrações do pacote **`llm`**, localizado no diretório `.kamila/llm/`. Este pacote é o responsável por fornecer a **inteligência artificial generativa baseada em Large Language Models (LLM)** para a assistente **Kamila**, conectando-se ao **Google Gemini AI** e à API do **Google AI Studio**.

---

## 1. Visão Geral da Arquitetura do Pacote

O pacote `.kamila/llm` abstrai a comunicação com as APIs generativas da Google, oferecendo respostas em streaming, suporte a modo offline/simulado, parâmetros de segurança configuráveis e descoberta dinâmica de modelos na nuvem.

```mermaid
flowchart TD
    subgraph Entrada do Sistema (Kamila Core)
        PROMPT[Prompt da Conversa + Memória] --> INIT[__init__.py - Constantes & Suporte]
    end

    subgraph Clientes & Motores de IA (.kamila/llm)
        INIT --> GE[gemini_engine.py - GeminiEngine via SDK]
        INIT --> AI[ai_studio_integration.py - AIStudioIntegration via REST API]
        
        GE -->|SDK google.generativeai| STREAM[Geração em Streaming - gemini-flash-latest]
        AI -->|HTTP REST v1beta| DISCOV[Descoberta Dinâmica de Modelos & Text Gen]
    end

    subgraph Fallbacks
        GE -->|Sem Chave / API Offline| SIM1[Geração Simulada Local]
        AI -->|Sem Chave / API Offline| SIM2[Geração Simulada Local]
    end
```

---

## 2. Estrutura dos Arquivos do Módulo

| Arquivo | Descrição / Função |
| :--- | :--- |
| **`__init__.py`** | Define metadados do pacote (`v1.0.0`), hiperparâmetros padrão (`DEFAULT_MODEL = "gemini-pro"`, `temperature=0.7`, `max_tokens=2048`) e rotinas de validação de modelos. |
| **`gemini_engine.py`** | Implementa a classe `GeminiEngine` via SDK oficial `google.generativeai`. Oferece suporte a streaming em tempo real (`generate_response_stream`) e filtros de segurança. |
| **`ai_studio_integration.py`** | Implementa a classe `AIStudioIntegration` via chamadas HTTP REST nativas na API v1beta do Google. Realiza a descoberta em tempo real dos modelos ativos (`_discover_available_models`). |
| **`main_with_gemini.py`** | Ponto de entrada estendido de demonstração conectando o interpretador local com o motor Gemini. |
| **`test_gemini_modules.py`** | Suíte de testes unitários e de integração para validação dos endpoints da IA. |
| **`requirements_gemini.txt`** | Relação de dependências do módulo (`google-generativeai`, `requests`, `python-dotenv`). |
| **`README.md`** | Guia de instalação e referência de uso rápido para desenvolvedores. |

---

## 3. Detalhamento das Classes Principais

### 3.1 `GeminiEngine` (`.kamila/llm/gemini_engine.py`)

#### Construtor e Configuração de Segurança:
- Lê a chave de API `GOOGLE_AI_API_KEY` do arquivo `.env`.
- Inicializa o modelo `gemini-flash-latest` (ou modelo alternativo configurado).
- Aplica o objeto `genai.types.GenerationConfig`:
  - `temperature`: `0.7`
  - `top_k`: `40`
  - `top_p`: `0.95`
  - `max_output_tokens`: `2048`
- Aplica diretivas de segurança (`BLOCK_MEDIUM_AND_ABOVE`) para:
  - Assédio (`HARM_CATEGORY_HARASSMENT`).
  - Discurso de ódio (`HARM_CATEGORY_HATE_SPEECH`).
  - Conteúdo sexualmente explícito (`HARM_CATEGORY_SEXUALLY_EXPLICIT`).
  - Conteúdo perigoso (`HARM_CATEGORY_DANGEROUS_CONTENT`).

#### Método de Streaming (`generate_response_stream`):
```python
def generate_response_stream(self, prompt: str, context: Optional[Dict[str, Any]] = None):
```
- Invoca `model.generate_content(..., stream=True)` retornando um gerador (*generator*) que emite os pedaços de texto (*chunks*) à medida em que são sintetizados pela nuvem da Google.

---

### 3.2 `AIStudioIntegration` (`.kamila/llm/ai_studio_integration.py`)

#### Funcionalidades da API REST:
- **Descoberta de Modelos (`_discover_available_models`)**: Realiza requisição `GET` para `https://generativelanguage.googleapis.com/v1beta/models` e preenche a lista `models_available`.
- **Geração de Texto (`generate_text`)**: Executa requisição `POST` com payload JSON formatado enviando a estrutura `contents/parts`.

---

## 4. Modo Simulado / Fallback para Execução Offline

Tanto a classe `GeminiEngine` quanto a `AIStudioIntegration` contam com um mecanismo de **fallback gracioso**: caso a chave `GOOGLE_AI_API_KEY` não seja fornecida ou o ambiente esteja sem acesso à internet, o sistema ativa automaticamente métodos de simulação (`_generate_simulated_response` / `_generate_simulated_text`), evitando que a assistente sofra travamentos ou *crashes*.
