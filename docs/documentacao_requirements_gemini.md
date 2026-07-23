# Documentação Técnica: Dependências de IA Generativa (`.kamila/llm/requirements_gemini.txt`)

Esta documentação descreve em detalhes as bibliotecas e dependências Python especificadas no arquivo **`requirements_gemini.txt`**, localizado em `.kamila/llm/requirements_gemini.txt`. Este arquivo lista todos os pacotes necessários para suportar os módulos de IA generativa, processamento de linguagem natural (NLP/NLU) e comunicação com as APIs do **Google Gemini** e **Google AI Studio**.

---

## 1. Comando de Instalação

Para instalar todas as dependências do módulo de IA no ambiente virtual, execute:

```bash
pip install -r .kamila/llm/requirements_gemini.txt
```

---

## 2. Relação de Pacotes por Categoria

| Categoria | Biblioteca | Versão Mínima | Função no Sistema Kamila |
| :--- | :--- | :--- | :--- |
| **Google AI** | `google-generativeai` | `>= 0.7.0` | SDK oficial da Google para inferência nos modelos Gemini (`GeminiEngine`). |
| **Google AI** | `google-ai-generativelanguage` | `>= 0.6.0` | Protobufs e definições de serviços de linguagem de baixo nível. |
| **HTTP REST** | `requests` | `>= 2.31.0` | Cliente HTTP utilizado pela classe `AIStudioIntegration` para chamadas diretas. |
| **Assíncrono** | `asyncio-mqtt` | `>= 0.13.0` | Suporte a mensageria e eventos assíncronos via protocolo MQTT. |
| **IA / ML** | `transformers` | `>= 4.21.0` | Modelos de linguagem locais e suporte a tokenizadores da Hugging Face. |
| **IA / ML** | `torch` | `>= 2.0.0` | Framework PyTorch para operações de inferência em tensores. |
| **Vetorização** | `numpy` | `>= 1.24.0` | Manipulação matemática de vetores de embedding e matrizes. |
| **NLU / NLP** | `nltk` | `>= 3.8` | Tokenização, stemming e remoção de *stop words*. |
| **NLU / NLP** | `spacy` | `>= 3.6` | Análise sintática avançada e reconhecimento de entidades nomeadas (NER). |
| **Fallback (Opcional)**| `openai` | `>= 0.28.0` | SDK da OpenAI para redundância e comparação de modelos. |
| **Fallback (Opcional)**| `anthropic` | `>= 0.3.0` | SDK da Anthropic (Claude) para redundância e comparação de modelos. |

---

## 3. Integração no Ecossistema

- **Essenciais**: `google-generativeai` e `requests` são vitais para o funcionamento dos módulos `gemini_engine.py` e `ai_studio_integration.py`.
- **NLU & Vetores**: `numpy`, `nltk` e `spacy` fornecem suporte ao pré-processamento de texto e manipulação de embeddings gravados no banco vetorial **ChromaDB**.
