import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from utils.file_manipulation import create_directory, create_markdown_path

# Carregamento das variáveis de ambiente 
load_dotenv()
LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')  # Chave da API LLAMA carregada do arquivo .env

class PDFExtractorLLAMA:
    """
    Classe para extração de tabelas e texto de arquivos PDF, com suporte para conversão para Markdown.
    """

    def __init__(self):
        """
        Inicializa a classe LlamaPDFExtractor.
        """
        self.LLAMA_API_KEY = LLAMA_API_KEY

    def set_pdf_metadata(self, page_text, page_num, pdf_file):
        """
        Define os metadados de uma página extraída de um arquivo PDF.
        
        Args:
            page_text (str): Texto extraído da página.
            pdf_file (str): Caminho do arquivo PDF.
            page_num (int): Número da página.
            page (Page): Objeto de página de um arquivo PDF.
        
        Returns:
            dict: Dicionário contendo os metadados da página
        """
        page_metadata = {
            "page_content": page_text,  # Texto extraído da página
            "metadata" : {
                "page_number": f"{page_num + 1}",   # Número da página
                "source": pdf_file,     # Caminho do arquivo PDF
            }
        }
        
        return page_metadata
    
    def extract_text_with_metadata(self, pdf_file):
        """
        Extrai o conteúdo de um PDF em formato texto bruto (TXT).

        Args:
            pdf_file (str): Caminho para o arquivo PDF.

        Returns:
            list[dict]: Lista de informações extraídas com texto bruto, número da página e fonte.
        """
        try:
            # Inicializa o parser LLAMA com resultado em texto bruto
            parser = LlamaParse(api_key=self.LLAMA_API_KEY, result_type="txt", verbose=True)
            
            # Carrega os dados do PDF usando o LLAMA
            documents = parser.load_data(pdf_file)
            
            # Estrutura para armazenar informações extraídas
            extract_metadata = []
            
            # Itera por cada página do PDF e armazena as informações
            for i in range(len(documents)):
                extract_metadata.append(self.set_pdf_metadata(documents[i].text, i, pdf_file))
            
            return extract_metadata  # Retorna as informações extraídas
        
        # Tratamento de erros durante o processo
        except Exception as e:
            print(f"Erro ao processar o arquivo {pdf_file}: {e}")
            raise e

    def convert_pdf_to_markdown(self, pdf_file, output_markdown_path='./outputs/ocr_documents/markdown/'):
        """
        Converte um PDF para um arquivo em formato Markdown (MD).

        Args:
            pdf_file (str): Caminho para o arquivo PDF.
            directory (str): Diretório para salvar os arquivos Markdown.

        Returns:
            list[dict]: Lista de informações extraídas com texto em Markdown, número da página e fonte.
        """
        
        # Verifica se o diretório de saída existe; caso contrário, cria 
        create_directory(output_markdown_path)
        
        try:
            # Inicializa o parser LLAMA com resultado em Markdown 
            parser = LlamaParse(api_key=self.LLAMA_API_KEY, result_type="markdown", verbose=True)
            
            # Carrega os dados do PDF usando o LLAMA 
            documents = parser.load_data(pdf_file)

            # Define o nome do arquivo Markdown baseado no nome do PDF 
            markdown_path = create_markdown_path(pdf_file, output_markdown_path)
            
            # Opcional: Nome fixo para o arquivo gerado
            markdown_path = 'document_llamaparser.md'

            # Caminho completo do arquivo Markdown 
            path_markdown = os.path.join(output_markdown_path, markdown_path)
            
            # Estrutura para armazenar informações extraídas 
            extract_metadata = []
            
            # Salva cada página como texto Markdown no arquivo de saída 
            with open(path_markdown, "w", encoding="utf-8") as file:
                for i in range(len(documents)):
                    file.write(documents[i].text)  # Escreve o texto no arquivo
                    extract_metadata.append(self.set_pdf_metadata(documents[i].text, i, pdf_file))
            
            return extract_metadata  # Retorna as informações extraídas
        
        except Exception as e:
            # Tratamento de erros 
            print(f"Erro ao processar o arquivo {pdf_file}: {e}")
            raise e

        
if __name__ == '__main__':
    # Caminho para o arquivo PDF a ser processado 
    pdf_file_path = './data/DummyPDF.pdf'
    
    # Inicializa a classe PDFExtractorLLAMA
    pdf_extractor = PDFExtractorLLAMA()
    
    # Converte o PDF para Markdown
    print("\nConvertendo PDF para Markdown...")
    markdown_file_info = pdf_extractor.convert_pdf_to_markdown(pdf_file_path)
    print(f"Arquivo Markdown criado em: {markdown_file_info['markdown_path']}")

    # Extrai texto com metadados do PDF
    print("Extraindo texto com metadados do PDF...")
    pdf_text_info = pdf_extractor.extract_text_with_metadata(pdf_file_path)
    print(f"Texto extraído: {pdf_text_info['pdf_text']}")
