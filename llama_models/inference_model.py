import os
import time
from dotenv import load_dotenv

from langchain_ollama import ChatOllama 
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

load_dotenv()

LLAMA_MODEL_INFERENCE = os.getenv('LLAMA_MODEL_INFERENCE')
LLAMA_URL = os.getenv('LLAMA_URL')

class LLAMAInferenceModel:
    """
    Classe para gerenciar a inferência de modelos
    LLAMA, incluindo o modelo de chat e o modelo de LLM.
    """
    def __init__(self):
        """
        Construtor da classe LLAMAInferenceModel.
        """
        self.LLAMA_MODEL = LLAMA_MODEL_INFERENCE
        self.LLAMA_URL = LLAMA_URL
        
    def invoke_chat_model(self, prompt):
        """
        Faz uma chamada ao modelo de chat LLAMA.
        
        Args:
            prompt (str): A entrada para o modelo de chat.
        Returns:
            response (str): A resposta do modelo de chat.
        """
        model = ChatOllama(model=self.LLAMA_MODEL, base_url=self.LLAMA_URL)
        response = model.invoke(prompt)

        return response
    
    def invoke_llm_model(self, prompt):
        """
        Faz uma chamada ao modelo de LLM LLAMA.
        
        Args:
            prompt (str): A entrada para o modelo de chat.
        Returns:
            response (str): A resposta do modelo de chat.
        """
        llm = OllamaLLM(model=self.LLAMA_MODEL)
        response = llm.invoke(prompt)
        
        return response



if __name__ == "__main__":
    model = LLAMAInferenceModel()
    
    # Calcular o tempo dessa operaçao
    start = time.time()
    end = time.time()
    print(f"Tempo de execução: {end - start} segundos")
    
    response = model.invoke_chat_model("Qual o sentido da vida?")