# Importações de bibliotecas internas do projeto
from knowledge_base.vector_database.faiss_database import VectorDatabaseFAISS
from knowledge_base.vector_database.chroma_database import VectorDatabaseChroma

from llama_models.inference_model import LLAMAInferenceModel
from llama_models.embedding_model import LLAMAEmbeddingModel

from prompt_template.prompts_template import create_prompt_template

class ControllerRAG:
    """
    Gerencia a extração de dados de arquivos PDF, fragmentação de conteúdo, 
    e integração com modelos de inferência e bancos de dados vetoriais.
    """

    def __init__(self):
        """
        Inicializa a classe ControllerRAG com os modelos de embedding, inferência 
        e banco de dados vetorial.
        """
        # Inicializa os modelos de embedding e inferência
        self.llama_embedding_model = LLAMAEmbeddingModel()
        self.llama_inference_model = LLAMAInferenceModel()

        # Inicializa o banco de dados vetorial (Chroma)
        self.database_chroma = VectorDatabaseChroma()

    def retrieve_data(self, query_text, n_results=5):
        """
        Recupera dados do banco vetorial com base em uma consulta textual.

        Args:
            query_text (str): Texto da consulta.
            n_results (int): Número de resultados desejados.

        Returns:
            dict: Dados recuperados do banco vetorial.
        """
        # Gera um vetor de embedding para a consulta textual
        embedding_query = self.llama_embedding_model.generate_embedding(query_text)
        
        # Recupera dados do banco vetorial
        retrieve_data = self.database_chroma.query_chromadb(embedding_query, n_results)
        
        # Retorna o primeiro documento recuperado
        filter_data = retrieve_data['documents'][0]
        return filter_data

    def generate_response(self, user_query, contexts):
        """
        Constrói um prompt para o modelo de inferência com base no contexto e na pergunta do usuário.

        Args:
            user_query (str): Pergunta do usuário.
            contexts (str): Contextos recuperados dos documentos relevantes.

        Returns:
            response_llm: Resposta gerada pelo modelo de inferência.
        """
        # Cria um prompt para o modelo de inferência
        prompt = create_prompt_template(user_query, contexts)
        
        # Gera uma resposta com base no prompt
        response_llm = self.llama_inference_model.invoke_llm_model(prompt)
        
        return response_llm
    
    def execute_RAG(self, user_query):
        """
        Executa o processo de recuperação de dados e geração de resposta.

        Args:
            pdf_file_path (str): Caminho para o arquivo PDF (atualmente não utilizado).

        Returns:
            None: Indica a conclusão do processo.
        """
        
        # Recupera dados relevantes do banco vetorial
        print("[system] Recuperando dados do banco vetorial...")
        context = self.retrieve_data(user_query, n_results=5)

        # Gera resposta com base nos dados recuperados
        print("[system] Gerando resposta...")
        response = self.generate_response(user_query, context)
        
        return response
    
if __name__ == "__main__":
    # Exemplo de uso da classe ControllerRAG
    controller = ControllerRAG()

    # Query de exemplo
    query = "Oque são minions?"

    # Recupera dados relevantes do banco vetorial
    retrieve_data = controller.execute_RAG(query)
    
    print(retrieve_data)