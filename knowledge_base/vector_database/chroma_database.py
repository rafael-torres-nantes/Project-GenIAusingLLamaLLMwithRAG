import os
import chromadb
import uuid
from dotenv import load_dotenv
from llama_models.embedding_model import LLAMAEmbeddingModel
from utils.file_manipulation import create_directory

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

    def __init__(self, database_name="my_database"):
        """
        Inicializa a instância da classe VectorDatabaseChroma.
        """
        # Cria o diretório de persistência se não existir
        create_directory(CHROMA_PATH)
        
        # Inicializa o cliente persistente do ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        
        # Cria ou recupera uma coleção
        self.collection = self.chroma_client.get_or_create_collection(name=database_name)
                     
    def query_chromadb(self, query_text, n_results=5):
        """
        Realiza uma consulta no banco vetorial Chroma usando texto de entrada.

        Args:
            query_text (str): Texto da consulta.
            n_results (int): Número de resultados desejados.

        Returns:
            dict: Resultados contendo documentos e metadados correspondentes.
        """
        # Gera embeddings para a consulta e encontra os chunks mais similares
        results = self.collection.query(
            query_texts=[query_text],  # Chroma gerará embeddings para isso
            n_results=n_results,
            include=["documents", "metadatas"]  # Inclui documentos e metadados nos resultados
        )
        return results
    
    def insert_into_chromadb(self, chunks):
        """
        Insere apenas chunks únicos no banco de dados vetorial Chroma.

        Args:
            chunks (list): Lista de chunks de texto com metadados.
        """
        # Recupera IDs existentes no banco de dados
        existing_ids = set(self.collection.get().get("ids", []))

        # Filtra chunks que ainda não estão no banco de dados
        new_chunks = [
            chunk for chunk in chunks 
            if str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.page_content)) not in existing_ids
        ]
        if new_chunks:
            print(f"👉 Adicionando novos documentos: {len(new_chunks)}")
            self.add_chunks_to_collection(new_chunks)
            return print("✅ Documentos adicionados com sucesso.")
        
        return print("✅ Nenhum novo documento para adicionar.")
    
    def add_chunks_to_collection(self, chunks):
        """
        Adiciona chunks de texto e metadados à coleção.

        Args:
            chunks (list): Lista de chunks de texto com metadados.
        """
        # Extrai conteúdos e metadados dos chunks
        chunk_content = [chunk.page_content for chunk in chunks]
        chunk_metadata = [chunk.metadata for chunk in chunks]
        
        # Adiciona os documentos e metadados ao banco vetorial
        self.collection.add(
            documents=chunk_content,
            metadatas=chunk_metadata,
            ids=[str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.page_content)) for chunk in chunks]
        )

if __name__ == '__main__':
    # Inicializa a classe VectorDatabaseChroma
    vector_database = VectorDatabaseChroma()

    # Exemplo de texto dividido em chunks
    text_chunks = [
        "Este é um exemplo de texto para teste.",
        "Vamos dividir este texto em chunks menores.",
        "Cada chunk terá um tamanho máximo de 10 palavras."
    ]

    # Metadados correspondentes aos chunks
    metadata = [
        {"source": "exemplo_1", "page": 1},
        {"source": "exemplo_2", "page": 2},
        {"source": "exemplo_3", "page": 3}
    ]

    # Insere os chunks no banco vetorial
    print("Adicionando chunks ao banco vetorial...")
    vector_database.insert_into_chromadb(text_chunks)

    # Realiza uma consulta no banco vetorial
    print("\nConsultando no banco vetorial...")
    query = "texto para teste"
    results = vector_database.query_chromadb(query_text=query, n_results=2)

    # Exibe os resultados da consulta
    print("\nResultados da consulta:")
    for doc, meta in zip(results['documents'], results['metadatas']):
        print(f"- Documento: {doc}")
        print(f"  Metadados: {meta}")
