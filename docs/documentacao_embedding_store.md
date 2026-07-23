# Documentação Técnica: Banco Vetorial de Memória (`.kamila/core/embedding_store.py`)

Esta documentação detalha o funcionamento do módulo **`embedding_store.py`**, representado pela classe `EmbeddingStore`. Este componente é responsável por gerenciar a **memória de longo prazo** (*Long-Term Memory*) da assistente **Kamila**, utilizando vetores de embeddings e a base de dados vetorial **ChromaDB**.

---

## 1. Visão Geral da Arquitetura

O `EmbeddingStore` permite que a assistente grave fatos, preferências, episódios de diário e eventos de saúde de maneira permanente no disco, recuperando-os posteriormente através de busca semântica por similaridade vetorial.

```mermaid
flowchart TD
    SUBGRAPH Ingestão de Memórias
        TXT[Texto / Fato] --> EMB[LLMInterface - create_embedding]
        EMB --> META[Metadados + Timestamp + ID]
        META --> CDB[(ChromaDB - kamila_memories)]
    END

    SUBGRAPH Busca Semântica
        QUERY[Pergunta / Entrada do Usuário] --> QEMB[LLMInterface - create_embedding]
        QEMB --> SEARCH[ChromaDB - collection.query]
        SEARCH --> RESULT[Top N Memórias Relevantes]
    END
```

---

## 2. Tecnologias e Configuração da Base

| Componente | Descrição / Valor Padrão |
| :--- | :--- |
| **Banco Vetorial** | `chromadb.PersistentClient` |
| **Caminho de Armazenamento** | `.kamila/kamila_memory_db` (garante persistência entre sessões) |
| **Nome da Coleção** | `kamila_memories` |
| **Geração de Embeddings** | Delegada à classe `LLMInterface` (Modelo de Embedding Gemini) |

---

## 3. Detalhamento dos Métodos da Classe `EmbeddingStore`

### 3.1 Construtor (`__init__`)
```python
def __init__(self, llm_interface: LLMInterface, collection_name="kamila_memories"):
```
- **Fluxo de Inicialização**:
  1. Armazena a referência da interface da LLM (`self.llm`).
  2. Define o caminho do banco persistente em `.kamila/kamila_memory_db`.
  3. Cria ou carrega a coleção no ChromaDB (`self.client.get_or_create_collection`).
  4. Imprime no log o status de carregamento e a contagem de itens existentes na coleção.

---

### 3.2 Inserção de Memória Única (`add_memory`)
```python
def add_memory(self, text: str, metadata: Dict[str, Any]):
```
- **Fluxo**:
  1. Gera o embedding vetorial do texto via `self.llm.create_embedding(text)`.
  2. Se a geração do vetor for bem-sucedida, constrói um ID único no formato `mem_<timestamp>_<tamanho_do_texto>`.
  3. Injeta a marcação temporal `timestamp` em formato ISO nos metadados.
  4. Adiciona o vetor, o documento de texto, os metadados e o ID à coleção do ChromaDB.

---

### 3.3 Inserção de Memórias em Lote (`add_memories`)
```python
def add_memories(self, texts: List[str], metadatas: List[Dict[str, Any]]):
```
- **Fluxo Otimizado**:
  1. Envia a lista de textos para processamento em lote via `self.llm.create_embeddings_batch(texts)`.
  2. Itera sobre a lista gerando IDs únicos indexados (`mem_<timestamp>_<tamanho>_<índice_loop>`) para evitar colisões caso textos diferentes sejam processados no mesmo milissegundo.
  3. Insere todos os vetores e documentos na coleção em uma única operação de lote no ChromaDB.

---

### 3.4 Busca por Similaridade Semântica (`search_memories`)
```python
def search_memories(self, query_text: str, n_results: int = 3) -> List[str]:
```
- **Fluxo de Consulta**:
  1. Valida se a coleção contém documentos (`self.collection.count() > 0`). Se vazia, retorna lista vazia `[]`.
  2. Converte a frase de busca em um vetor de embedding via `self.llm.create_embedding(query_text)`.
  3. Executa a consulta vetorial `self.collection.query(query_embeddings=[query_embedding], n_results=n_results)`.
  4. Retorna os $N$ documentos de texto com maior proximidade semântica.

---

## 4. Exemplo de Estrutura Armazenada

```json
{
  "id": "mem_1721775400.123_25",
  "document": "O usuário gosta de café sem açúcar.",
  "metadata": {
    "type": "preference",
    "content": "café sem açúcar",
    "timestamp": "2026-07-23T19:37:00.123456"
  }
}
```
