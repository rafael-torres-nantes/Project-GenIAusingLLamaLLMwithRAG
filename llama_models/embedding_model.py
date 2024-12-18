import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
import ollama

load_dotenv()

LLAMA_MODEL_EMBEDDING = os.getenv('LLAMA_MODEL_EMBEDDING')
LLAMA_URL = os.getenv('LLAMA_URL')

class LLAMAEmbeddingModel:
    def __init__(self):
        self.LLAMA_MODEL = LLAMA_MODEL_EMBEDDING
        self.LLAMA_URL = LLAMA_URL
        
    def get_embedding_model(self):
        """
        Obtém o modelo de embeddings LLAMA.

        Returns:
            embedding_model: Modelo de embeddings LLAMA
        """
        
        embedding_model = OllamaEmbeddings(model=self.LLAMA_MODEL)

        return embedding_model

    def generate_embedding(self, text):
        """
        Gera embedding para um texto fornecido. 
        
        Args:
            text (str): Texto para o qual o embedding será gerado.
        Returns:
            embedding: Embedding gerado para o texto.
        """
        response = ollama.embeddings(model=LLAMA_MODEL_EMBEDDING, prompt=text)
        embedding = response["embedding"]
        return embedding
    
if __name__ == "__main__":
    llama_embedding_model = LLAMAEmbeddingModel()
    embedding = llama_embedding_model.generate_embedding("Hello, world!")
    print(embedding)