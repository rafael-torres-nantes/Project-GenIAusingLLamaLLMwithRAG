import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from llama_models.embedding_model import LLAMAEmbeddingModel

# Carregamento das variáveis de ambiente
load_dotenv()

# Caminho para o diretório de persistência do banco de vetores Chroma
FAISS_PATH = os.getenv('FAISS_PATH')

# Inicializa o modelo de embeddings LLAMA
llamaEmbeddingModel = LLAMAEmbeddingModel()
embedding_model = llamaEmbeddingModel.get_embedding_model()

class VectorDatabaseFAISS:
    """
    Classe para gerenciar o banco de dados vetorial FAISS, 
    com métodos para criar, salvar e carregar vetores.
    """
    
    def __init__(self):
        """
        Inicializa a instância do VectorDatabaseFAISS.
        """
        pass
    
    def get_vectorstore(self, text_chunks):
        """
        Cria e retorna um banco de dados vetorial FAISS a partir de fragmentos de texto.
        
        Args:
            text_chunks (list of str): Lista de textos para criar os vetores.
        
        Returns:
            vectorstore (FAISS): O banco de dados vetorial FAISS gerado.
        """        
        # Cria o banco de dados vetorial FAISS a partir dos textos
        self.faiss_db = FAISS.from_texts(texts=text_chunks, embedding=embedding_model)
        
        return self.faiss_db
    
    def save_vectorstore(self):
        """
        Salva o banco de dados vetorial FAISS em um diretório local.
        
        Args:
            vectorstore (FAISS): O banco de dados vetorial a ser salvo.
            output_path (str): O caminho onde o banco de dados vetorial será salvo.
        
        Raises:
            Exception: Se ocorrer algum erro ao salvar o banco de dados.
        """
        try:            
            # Salva o banco de dados vetorial localmente
            self.faiss_db.save_local(FAISS_PATH)
        
        except Exception as e:
            # Caso ocorra algum erro, imprime e relança a exceção
            print(f'Error saving vectorstore: {e}')
            raise e
    
    def retrieve_vectorstore(self):
        """
        Carrega um banco de dados vetorial FAISS a partir de um diretório local.
        
        Args:
            input_path (str): O caminho onde o banco de dados vetorial está localizado.
        
        Returns:
            vectorstore (FAISS): O banco de dados vetorial carregado.
        
        Raises:
            Exception: Se ocorrer algum erro ao carregar o banco de dados.
        """
        try:
            # Carrega o banco de dados vetorial a partir do diretório
            self.faiss_db = FAISS.load_local(FAISS_PATH)
            return self.faiss_db
        
        except Exception as e:
            # Caso ocorra algum erro, imprime e relança a exceção
            print(f'Error loading vectorstore: {e}')
            raise e

# Exemplo de uso com o FAISS e o Chroma
if __name__ == '__main__':
    # Exemplo de criação e salvamento de vetores usando FAISS
    text_chunks = [
        'Este é um exemplo de texto para teste.',
        'Vamos dividir este texto em chunks menores.',
        'Cada chunk terá um tamanho máximo de 10 palavras.'
    ]
    
    
    # Instância da classe FAISS para criar e salvar vetores
    faiss_db = VectorDatabaseFAISS()
    vectorstore_faiss = faiss_db.get_vectorstore(text_chunks)
    faiss_db.save_vectorstore(vectorstore_faiss)