import os
from dotenv import load_dotenv
from langchain_chroma import Chroma 
from llama_models.embedding_model import LLAMAEmbeddingModel

# Carregamento das variáveis de ambiente
load_dotenv()

# Caminho para o diretório de persistência do banco de vetores Chroma
CHROMA_PATH = os.getenv('CHROMA_PATH')

# Inicializa o modelo de embeddings LLAMA
llamaEmbeddingModel = LLAMAEmbeddingModel()
embedding_model = llamaEmbeddingModel.get_embedding_model()

class VectorDatabaseChroma:
    """
    Classe para gerenciar operações com o banco de vetores Chroma.
    Inclui métodos para criação, salvamento e carregamento de vetores.
    """

    def __init__(self):
        """
        Inicializa a instância da classe VectorDatabaseChroma.
        """
        self.chroma_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)

    def save_vectorstore(self, text_chunks):
        """
        Salva o armazenamento vetorial Chroma, evitando duplicatas.

        Args:
            text_chunks (list): Lista de chunks de texto com metadados.
        """
        try:
            chunks_with_ids = self.calculate_chunk_ids(text_chunks)
            existing_items = self.retrieve_vectorstore()
            existing_ids = set(existing_items["ids"])

            # Filtra os chunks novos
            new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

            if new_chunks:
                print(f"👉 Adicionando novos documentos: {len(new_chunks)}")
                new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
                self.chroma_db.add_documents(new_chunks, ids=new_chunk_ids)
                self.chroma_db.persist()
            else:
                print("✅ Nenhum novo documento para adicionar.")

        except Exception as e:
            print(f"Erro ao salvar o armazenamento vetorial: {e}")
            raise

    def retrieve_vectorstore(self):
        """
        Carrega o armazenamento vetorial Chroma do diretório especificado.

        Returns:
            dict: Dados do armazenamento vetorial carregado.
        """
        try:
            return self.chroma_db.get(include=[])
        except Exception as e:
            print(f"Erro ao carregar o armazenamento vetorial: {e}")
            raise

    @staticmethod
    def calculate_chunk_ids(text_chunks):
        """
        Adiciona IDs únicos a cada chunk com base na origem e página.

        Args:
            text_chunks (list): Lista de chunks a serem processados.

        Returns:
            list: Lista de chunks com IDs adicionados.
        """
        last_page_id = None
        current_chunk_index = 0

        for chunk in text_chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            chunk.metadata["id"] = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

        return text_chunks

if __name__ == '__main__':
    # Exemplo de uso da classe VectorDatabaseChroma
    vector_database = VectorDatabaseChroma()

    # Texto de exemplo para teste
    text_chunks = [
        'Este é um exemplo de texto para teste.',
        'Vamos dividir este texto em chunks menores.',
        'Cada chunk terá um tamanho máximo de 10 palavras.'
    ]

    # Criação e salvamento de vetores usando Chroma
    vectorstore = vector_database.get_vectorstore(text_chunks)
    vector_database.save_vectorstore(text_chunks)
