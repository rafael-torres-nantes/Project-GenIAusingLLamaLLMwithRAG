import pdfplumber
import pandas as pd
from utils.file_manipulation import create_directory, create_markdown_path

class PDFExtractorPlumber:
    """
    Classe para extração de tabelas e texto de arquivos PDF, com suporte para conversão para Markdown.
    """

    def __init__(self):
        """
        Inicializa a classe PDFExtractor.
        """
        pass
    
    def set_pdf_metadata(self, page_text, pdf_file, page_num, page):
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
        # Define os metadados da página
        page_metadata = {
            "page_content": page_text,      # Texto extraído da página
            "metadata" : {
                "page_number": f"{page_num + 1}",   # Número da página
                "source": pdf_file,                 # Caminho do arquivo PDF
                "bounding_box": f"{page.bbox}",     # Caixa delimitadora da página
            }
        }
        
        return page_metadata
                            
    def extract_text_with_metadata(self, pdf_file, output_directory='./outputs/ocr_documents/text_metadata'):
        """
        Extrai o texto de um arquivo PDF, incluindo metadados de cada página, e salva em um arquivo.

        Args:
            pdf_file (str): Caminho do arquivo PDF.
            output_directory (str): Diretório onde o arquivo com metadados será salvo.

        Returns:
            dict: Dicionário contendo o texto e os metadados extraídos.
        """
        pdf_text = ""
        pdf_metadata = []

        try:
            # Abre o arquivo PDF usando pdfplumber
            with pdfplumber.open(pdf_file) as pdf_document:
                
                # Itera por cada página do PDF
                for i, page in enumerate(pdf_document.pages):
                    # Extrai o texto da página
                    page_text = page.extract_text()
                    pdf_metadata.append(self.set_pdf_metadata(page_text, pdf_file, i, page))

                pdf_text = "\n\n".join(page['page_content'] for page in pdf_metadata)

            return {"pdf_text": pdf_text, "pdf_metadata": pdf_metadata}

        except Exception as error:
            # Trata erros durante a extração
            print(f"Erro ao processar o arquivo {pdf_file}: {error}")
            raise error

    def convert_pdf_to_markdown(self, pdf_file, output_markdown_path='./outputs/ocr_documents/markdown'):
        """
        Converte o conteúdo de um arquivo PDF para um arquivo Markdown.

        Args:
            pdf_file (str): Caminho do arquivo PDF.
            output_markdown_path (str): Diretório onde o arquivo Markdown será salvo.

        Returns:
            dict: Dicionário contendo o caminho do arquivo Markdown e informações extraídas.
        """
        # Garante que o diretório de saída existe
        create_directory(output_markdown_path)

        try:
            # Cria o caminho do arquivo Markdown
            markdown_path = create_markdown_path(pdf_file, output_markdown_path)

            # Abre o arquivo PDF usando pdfplumber
            with pdfplumber.open(pdf_file) as pdf_document:
                markdown_content = []
                extract_metadata = []

                # Itera por cada página do PDF
                for i, page in enumerate(pdf_document.pages):
                    page_text = page.extract_text()
                    extract_metadata.append(self.set_pdf_metadata(page_text, pdf_file, i, page))
                    markdown_content.append(page_text if page_text else "")

                # Salva o conteúdo extraído em um arquivo Markdown
                with open(markdown_path, "w", encoding="utf-8") as markdown_file:
                    markdown_file.write("\n\n".join(markdown_content))

            # Define o caminho do arquivo Markdown e as informações extraídas
            print(f"Markdown gerado em: {markdown_path}")
            
            return extract_metadata

        except Exception as error:
            print(f"Erro ao processar o arquivo {pdf_file}: {error}")
            raise error
        
    def extract_table_data(self, pdf_file):
        """
        Extrai tabelas de um arquivo PDF e organiza as informações.

        Args:
            pdf_file (str): Caminho do arquivo PDF.

        Returns:
            list: Lista de dicionários contendo informações detalhadas sobre as tabelas extraídas.
        """
        try:
            # Abre o arquivo PDF usando pdfplumber
            with pdfplumber.open(pdf_file) as pdf_document:

                # Lista para armazenar as tabelas extraídas
                extracted_tables = []
                
                # Itera por cada página do PDF
                for page in pdf_document.pages:
                    # Extrai a tabela da página atual
                    raw_table = page.extract_table()

                    # Limpa os dados da tabela extraída
                    cleaned_table = self.clean_table(raw_table)

                    # Extrai informações adicionais sobre a tabela
                    table_metadata = self.extract_table_metadata(page)

                    if table_metadata:
                        table_metadata['cleaned_table'] = cleaned_table
                        extracted_tables.append(table_metadata)

            return extracted_tables

        except Exception as error:
            # Trata erros inesperados
            print(f"Erro ao processar o arquivo {pdf_file}: {error}")
            raise error

    def extract_table_metadata(self, pdf_page):
        """
        Obtém metadados de tabelas em uma página do PDF.

        Args:
            pdf_page (Page): Objeto de página de um arquivo PDF.

        Returns:
            dict or None: Dicionário com informações sobre as tabelas, ou None se não houver tabelas.
        """
        tables  = pdf_page.find_tables()

        if tables:
            metadata = {
                'page_number': pdf_page.page_number,
                'bounding_box': tables[0].bbox,
                'table_cells': tables[0].cells,
                'table_rows': tables[0].rows
            }
            return metadata

        return None

    def clean_table(self, raw_table):
        """
        Limpa os dados de uma tabela extraída de um arquivo PDF.

        Args:
            raw_table (list): Tabela bruta extraída do PDF.

        Returns:
            pd.DataFrame: Dados da tabela organizados em um DataFrame do Pandas.
        """
        if raw_table:
            return pd.DataFrame(raw_table[1:], columns=raw_table[0])
        return pd.DataFrame()

if __name__ == '__main__':
    # Exemplo de uso da classe PDFExtractorPlumber
    pdf_file_path = './data/DummyPDF.pdf'

    # Inicializa a classe PDFExtractorPlumber
    pdf_extractor = PDFExtractorPlumber()

    #  Extrai tabelas do PDF 
    print("Extraindo tabelas do PDF...")
    tables = pdf_extractor.extract_table_data(pdf_file_path)
    print(f"Tabelas extraídas: {len(tables)}")

    # Converte o PDF para Markdown
    print("\nConvertendo PDF para Markdown...")
    markdown_file_info = pdf_extractor.convert_pdf_to_markdown(pdf_file_path)
    print(f"Arquivo Markdown criado em: {markdown_file_info['markdown_path']}")

    # Extrai texto com metadados do PDF
    print("Extraindo texto com metadados do PDF...")
    pdf_text_info = pdf_extractor.extract_text_with_metadata(pdf_file_path)
    print(f"Texto extraído: {pdf_text_info['pdf_text']}")