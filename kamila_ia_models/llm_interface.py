# kamila_ia_models/llm_interface.py

import os
import google.generativeai as genai
from typing import List

class LLMInterface:
    """
    Interface unificada para interagir com os modelos de linguagem do Google (Gemini).
    Responsável por gerar respostas de texto e criar embeddings vetoriais.
    """
    def __init__(self, text_model_name: str = 'gemini-flash-latest', embedding_model_name: str = 'models/text-embedding-004'):
        """
        Inicializa a interface, configurando a API do Google.
        
        Args:
            text_model_name (str): Nome do modelo de geração de texto.
            embedding_model_name (str): Nome do modelo para criação de embeddings.
        """
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            raise ValueError("A chave GOOGLE_AI_API_KEY não foi encontrada no seu arquivo .env")
        
        genai.configure(api_key=api_key)
        self.text_model = genai.GenerativeModel(text_model_name)
        self.embedding_model_name = embedding_model_name
        print("Interface com LLM (Gemini) inicializada com sucesso.")

    def generate_response(self, prompt: str) -> str:
        """
        Gera uma resposta de texto a partir de um prompt.
        
        Args:
            prompt (str): O prompt completo a ser enviado para o modelo.
            
        Returns:
            str: A resposta gerada pelo modelo.
        """
        try:
            response = self.text_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erro ao gerar resposta do LLM: {e}")
            return "Desculpe, tive um problema para pensar na resposta."

    def create_embedding(self, text: str) -> List[float]:
        """
        Cria um embedding vetorial para um dado texto.
        
        Args:
            text (str): O texto a ser convertido em um vetor.
            
        Returns:
            List[float]: A representação vetorial (embedding) do texto.
        """
        try:
            result = genai.embed_content(model=self.embedding_model_name, content=text)
            return result['embedding']
        except Exception as e:
            print(f"Erro ao criar embedding para o texto '{text}': {e}")
            return []

    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Cria embeddings vetoriais para uma lista de textos (batch).

        Args:
            texts (List[str]): Lista de textos a serem convertidos em vetores.

        Returns:
            List[List[float]]: Lista de representações vetoriais (embeddings).
        """
        if not texts:
            return []

        try:
            result = genai.embed_content(model=self.embedding_model_name, content=texts)
            return result['embedding']
        except Exception as e:
            print(f"Erro ao criar embeddings em batch: {e}")
            return []