# Importações de bibliotecas internas do projeto
from knowledge_base.vector_database.faiss_database import VectorDatabaseFAISS
from knowledge_base.vector_database.chroma_database import VectorDatabaseChroma
from knowledge_base.ingestion_data.chunking_langchain import ChunkSplitter

from llama_models.inference_model import LLAMAInferenceModel
from llama_models.embedding_model import LLAMAEmbeddingModel

from prompt_template.prompts_template import create_prompt_template

from scraping_data.scraping_pdf.ocr_text_llamaparser import PDFExtractorLLAMA 
from scraping_data.scraping_pdf.ocr_text_pdfplumber import PDFExtractorPlumber

from utils.send_each_pdf_file import each_pdf_in_folder
from utils.convert_dict_to_object import dict_to_namedtuple

class Controller:
    """
    Classe Controller:
    Responsável por gerenciar a extração de dados de arquivos PDF,
    a fragmentação do conteúdo e a integração com modelos de inferência e bancos de dados vetoriais.
    """
    def __init__(self):
        # Inicializa a extração de texto de PDFs usando diferentes métodos
        self.llama_pdf_extractor = PDFExtractorLLAMA()
        self.plumber_pdf_extractor = PDFExtractorPlumber()

        # Inicializa os modelos de embedding e inferência
        self.llama_embedding_model = LLAMAEmbeddingModel()
        self.llama_inference_model = LLAMAInferenceModel()

        # Inicializa o banco de dados vetorial (Chroma)
        self.vector_database_chroma = VectorDatabaseChroma()

        # Inicializa a ferramenta de fragmentação de texto
        self.chunk_splitter = ChunkSplitter()

    def ingestion_data(self, pdf_file):
        """
        Método de ingestão de dados:
        Permite a ingestão de um arquivo PDF e seu processamento futuro.
        """
        return None

    def run_process(self, pdf_file_path="data/DummyPDF.pdf"):
        """
        Método run_process:
        Realiza o processo de extração de texto de um arquivo PDF,
        segmentação em chunks e exibe os resultados formatados.
        """

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

        # Exibe os dados fragmentados no console
        print(chunked_data)

        # Indica a conclusão do processo
        return print("Processo completado!")
