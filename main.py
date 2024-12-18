from controller.controller_ingestion_data import ControllerIngestionData
from controller.controller_rag import ControllerRAG

controller_ingestion = ControllerIngestionData()
controller_rag = ControllerRAG()

if '__main__' == __name__:
    # Exemplo de criação e salvamento de vetores usando Chroma
    controller_ingestion.ingestion_data_folder()

    query = "Quais lanes tem no LOL?"

    # Recupera dados relevantes do banco vetorial
    retrieve_data = controller_rag.execute_RAG(query)

    print(retrieve_data)