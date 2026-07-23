# Documentação Técnica: Banco de Dados Vetorial Persistente (`.kamila/kamila_memory_db/`)

Esta documentação descreve a estrutura, o propósito e a política de segurança do diretório **`kamila_memory_db`**, localizado no caminho `.kamila/kamila_memory_db/`. Este componente atua como o **banco de dados vetorial de memória de longo prazo (Long-Term Memory)** da assistente **Kamila**.

---

## 1. Visão Geral da Arquitetura

O `kamila_memory_db` é um repositório binário gerenciado nativamente pelo **ChromaDB** através da classe `chromadb.PersistentClient`. Ele permite que a assistente mantenha uma memória contínua e permanente entre reinicializações do sistema.

```mermaid
flowchart TD
    subgraph Módulos da Kamila
        MM[MemoryManager] --> ES[EmbeddingStore]
        MU[MemoryUpdater] --> ES
        RET[Retriever] --> ES
    end

    subgraph Armazenamento Físico (.kamila/kamila_memory_db)
        ES -->|PersistentClient| SQLITE[(chroma.sqlite3 - Metadados, Textos e IDs)]
        ES -->|PersistentClient| HNSW[Índices Vetoriais HNSW - Embeddings]
    end
```

---

## 2. Estrutura de Arquivos Físicos

| Arquivo / Pasta | Tipo | Função |
| :--- | :--- | :--- |
| **`chroma.sqlite3`** | Banco SQLite | Armazena a coleção `kamila_memories`, o mapeamento de documentos brutos, tabelas de metadados e os IDs únicos de cada registro. |
| **Subpastas GUID** | Arquivos de Índice HNSW | Contêm as árvores de busca de vizinhos mais próximos (*Hierarchical Navigable Small World*) para consultas vetoriais ultra-rápidas. |

---

## 3. Estrutura dos Dados Armazenados

Cada registro dentro da coleção `kamila_memories` é composto por 4 colunas principais:

```json
{
  "id": "mem_1721775400.123_25",
  "embedding": [-0.0124, 0.0451, 0.0092, "... 768 a 1536 dimensões ..."],
  "document": "O usuário gosta de praticar caminhadas pela manhã.",
  "metadata": {
    "type": "preference",
    "content": "caminhadas pela manhã",
    "timestamp": "2026-07-23T19:37:00.123456"
  }
}
```

---

## 4. Integração com o Código do Projeto

- **Inicialização**: Instanciado em `.kamila/core/embedding_store.py`:
  ```python
  db_path = os.path.join(project_root, '.kamila', 'kamila_memory_db')
  self.client = chromadb.PersistentClient(path=db_path)
  self.collection = self.client.get_or_create_collection(name="kamila_memories")
  ```
- **Inserção**: Atualizado via `add_memory` e `add_memories`.
- **Busca Semântica**: Consultado via `search_memories` por k-vizinhos mais próximos ($k$-NN).

---

## 5. Política de Segurança e Privacidade

> [!IMPORTANT]
> **Proteção no Git**: Como este banco de dados armazena informações pessoais, preferências e registros clínicos/eventos de saúde do usuário, o diretório `.kamila/kamila_memory_db/` está **estritamente incluído no arquivo `.gitignore`**. 

**Nunca envie este diretório para o GitHub ou repositórios remotos.**
