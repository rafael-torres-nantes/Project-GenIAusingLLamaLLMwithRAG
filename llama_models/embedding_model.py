import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings 

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
        """
        
        embedding_model = OllamaEmbeddings(model=self.LLAMA_MODEL)

        return embedding_model

