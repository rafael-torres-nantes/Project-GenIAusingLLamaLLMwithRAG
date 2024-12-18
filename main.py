from controller.controller_ingestion_data import Controller
from knowledge_base.vector_database.chroma_database import VectorDatabaseChroma

controller = Controller()

if '__main__' == __name__:
    # Exemplo de criação e salvamento de vetores usando FAISS
    controller.run_process()
    
    # # Exemplo de uso da classe VectorDatabaseChroma
    # vector_database = VectorDatabaseChroma()

    # # Texto de exemplo para teste
    # text_chunks = [
    #     "Este é um exemplo de texto para teste.",
    #     "Vamos dividir este texto em chunks menores.",
    #     "Cada chunk terá um tamanho máximo de 10 palavras."
    # ]

    # # Metadados correspondentes aos chunks
    # metadata = [
    #     {"source": "exemplo_1", "page": 1},
    #     {"source": "exemplo_2", "page": 2},
    #     {"source": "exemplo_3", "page": 3}
    # ]

    # # Inserir os chunks no banco vetorial
    # print("Adicionando chunks ao banco vetorial...")
    # vector_database.insert_into_chromadb(text_chunks, metadata)

    # # Consulta no banco vetorial
    # print("\nConsultando no banco vetorial...")
    # query = "texto para teste"
    # results = vector_database.query_chromadb(query_text=query, n_results=2)

    # # Exibição dos resultados da consulta
    # print("\nResultados da consulta:")
    # for doc, meta in zip(results['documents'], results['metadatas']):
    #     print(f"- Documento: {doc}")
    #     print(f"  Metadados: {meta}")