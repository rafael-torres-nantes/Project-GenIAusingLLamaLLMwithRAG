# Importações de bibliotecas internas do projeto
from knowledge_base.vector_database.faiss_database import VectorDatabaseFAISS
from knowledge_base.vector_database.chroma_database import VectorDatabaseChroma
from knowledge_base.ingestion_data.chunking_langchain import ChunkSplitter

from scraping_data.scraping_pdf.ocr_text_llamaparser import PDFExtractorLLAMA 
from scraping_data.scraping_pdf.ocr_text_pdfplumber import PDFExtractorPlumber

from utils.send_each_pdf_file import list_all_pdf_in_folder
from utils.convert_dict_to_object import dict_to_namedtuple
from utils.list_manipulation import flatten_documents

class ControllerIngestionData:
    """
    Classe Controller:
    Responsável por gerenciar a extração de dados de arquivos PDF,
    a fragmentação do conteúdo e a integração com modelos de inferência e bancos de dados vetoriais.
    """
    def __init__(self):
        # Inicializa a extração de texto de PDFs usando diferentes métodos
        self.plumber_pdf_extractor = PDFExtractorPlumber()

        # Inicializa o banco de dados vetorial (Chroma)
        self.database_chroma = VectorDatabaseChroma()

        # Inicializa a ferramenta de fragmentação de texto
        self.chunk_splitter = ChunkSplitter()

    def ingestion_data(self, pdf_file_path="data\LOL-Rumo-ao-Challenger.pdf"):
        """
        Método de ingestão de dados:
        Permite a ingestão de um arquivo PDF e seu processamento futuro.
        
        Args:
            pdf_file_path (str): Caminho para o arquivo PDF a ser processado.
        
        """
        
        try: 
            # Extrai o conteúdo do PDF e o converte para Markdown
            markdown_data = self.plumber_pdf_extractor.convert_pdf_to_markdown(pdf_file_path)

            # Lista para armazenar os dados fragmentados
            chunked_data = []

            # Processa cada página do Markdown extraído
            for content in markdown_data:
                # Converte o dicionário para um objeto mais estruturado
                formated_content = dict_to_namedtuple(content)

                # Realiza a fragmentação do conteúdo em chunks
                chunk_split = self.chunk_splitter.recursive_split_documents([formated_content])
                
                # Adiciona os chunks processados à lista
                chunked_data.append(chunk_split)
            
            # Retorna os dados fragmentados
            formated_chunks = flatten_documents(chunked_data)
            
            # Retorna os dados fragmentados
            self.database_chroma.insert_into_chromadb(formated_chunks)
        
        except Exception as e:
            print(f"Erro ao fazer a Ingestão de Dados: {e}")

    def ingestion_data_folder(self, folder_path="./data"):
        """
        Método de ingestão de dados:
        Permite a ingestão de um arquivo PDF e seu processamento futuro.
        
        Args:
            folder_path (str): Caminho para o diretório dos arquivos PDF a ser processado.
        """
        
        list_path_pdf =list_all_pdf_in_folder(folder_path)
        
        for path_pdf in list_path_pdf:
            self.ingestion_data(pdf_file_path=path_pdf)