import os
import re
import fitz  # PyMuPDF
import pymupdf4llm
import pathlib
from utils.file_manipulation import create_directory, create_markdown_path, create_image_path

class PDFExtractor:
    
    def __init__(self):
        # Inicializa a classe PDFExtractor, sem atributos definidos no momento.
        pass
    
    def set_pdf_metadata(self, page_text, page_num, pdf_file):
        """
        Define os metadados de uma página extraída de um arquivo PDF.
        
        Args:
            page_text (str): Texto extraído da página.
            pdf_file (str): Caminho do arquivo PDF.
            i (int): Número da página.
            page (Page): Objeto de página de um arquivo PDF.
        
        Returns:
            dict: Dicionário contendo os metadados da página
        """
        # Define os metadados da página
        page_metadata = {
            "page_content": page_text,          # Texto extraído da página
            "metadata" : 
            {
                "page_number": page_num + 1,    # Número da página
                "source": pdf_file,             # Caminho do arquivo PDF
            }
        }
        
        return page_metadata
    
    def extract_text_with_metadata(self, pdf_file):
        """
        Extrai texto de um arquivo PDF usando a biblioteca PyMuPDF.

        Args:
            pdf_file (str): Caminho do arquivo PDF.

        Returns:
            str: Texto extraído do PDF ou mensagem de erro em caso de falha.
        """
        try:
            # Abre o arquivo PDF usando PyMuPDF
            doc = fitz.open(pdf_file)
            extract_metadata = []  # Lista para armazenar as informações extraídas
            all_text = ""

            # Itera sobre cada página do PDF e extrai o texto
            for page_num in range(doc.page_count):
                page = doc[page_num]
                all_text += page.get_text()
                extract_metadata.append(self.set_pdf_metadata(page.get_text(), page_num, pdf_file))

            # Fecha o arquivo PDF
            doc.close()
            return {"pdf_text" : all_text, "extract_metadata": extract_metadata}
        
        except fitz.EmptyFileError as e:
            # Trata erro caso o arquivo esteja vazio ou corrompido
            print(f"Erro: O arquivo {pdf_file} está vazio ou corrompido.")
            raise e
        
        except Exception as e:
            # Trata outros erros inesperados
            print(f"Erro ao processar o arquivo {pdf_file}: {e}")
            raise e

    def extract_images_pdf(self, pdf_file, output_image_path='./outputs/ocr_documents/images'):
        """
        Extrai imagens de um arquivo PDF usando a biblioteca PyMuPDF.

        Args:
            pdf_file (str): Caminho do arquivo PDF.

        Returns:
            list: Lista de nomes dos arquivos de imagens extraídos.
        """

        # Garante que o diretório de saída existe
        create_directory(output_image_path)

        try:
            # Abre o arquivo PDF
            doc = fitz.open(pdf_file)
            images = []  # Lista para armazenar os nomes das imagens extraídas

            # Itera sobre cada página do PDF
            for page_num in range(doc.page_count):
                page = doc[page_num]
                image_list = page.get_images(full=True)  # Obtém as imagens da página

                # Itera sobre cada imagem encontrada na página
                for image_index, img in enumerate(image_list):
                    xref = img[0]  # Referência à imagem no PDF
                    base_image = doc.extract_image(xref)  # Extrai a imagem
                    image_bytes = base_image["image"]  # Conteúdo binário da imagem
                    image_ext = base_image["ext"]  # Extensão do arquivo de imagem

                    # Define o nome do arquivo de imagem baseado no PDF e na página
                    image_filename = create_image_path(pdf_file, page_num, image_index, image_ext)

                    # Define o caminho do arquivo de imagem
                    path_image = os.path.join(output_image_path, image_filename)

                    # Salva a imagem em um arquivo
                    with open(path_image, "wb") as image_file:
                        image_file.write(image_bytes)

                    # Adiciona o nome da imagem à lista
                    images.append(path_image)

            # Fecha o arquivo PDF
            doc.close()
            return images
        
        except fitz.EmptyFileError as e:
            # Trata erro caso o arquivo esteja vazio ou corrompido
            print(f"Erro: O arquivo {pdf_file} está vazio ou corrompido.")
            raise e
        except Exception as e:
            # Trata outros erros inesperados
            print(f"Erro ao processar o arquivo {pdf_file}: {e}")
            raise e 
    
    def extract_links_pdf(self, pdf_file):
        """
        Extrai links de um arquivo PDF usando a biblioteca PyMuPDF.

        Args:
            pdf_file (str): Caminho do arquivo PDF.

        Returns:
            list: Lista de links extraídos.
        """
        try:
            # Abre o arquivo PDF
            doc = fitz.open(pdf_file)
            links = []  # Lista para armazenar os links extraídos

            # Itera sobre cada página do PDF
            for page_num in range(doc.page_count):
                page = doc[page_num]
                link_list = page.get_links()  # Obtém os links da página

                # Itera sobre cada link encontrado na página
                for link in link_list:
                    link_url = link["uri"]  # URL do link
                    link_rect = link["rect"]  # Coordenadas do link
                    link_page = page_num + 1  # Página do link

                    # Adiciona o link à lista
                    links.append({"url": link_url, "page": link_page, "rect": link_rect})

            # Fecha o arquivo PDF
            doc.close()
            return links
        
        except fitz.EmptyFileError as e:
            # Trata erro caso o arquivo esteja vazio ou corrompido
            print(f"Erro: O arquivo {pdf_file} está vazio ou corrompido.")
            raise e
        
        except Exception as e:
            # Trata outros erros inesperados
            print(f"Erro ao processar o arquivo {pdf_file}: {e}")

    def extract_tables_pdf(self, pdf_file):
        """
        Extrai tabelas de um arquivo PDF usando a biblioteca PyMuPDF.

        Args:
            pdf_file (str): Caminho do arquivo PDF.
        """
        try:
            # Abre o arquivo PDF
            doc = fitz.open(pdf_file)
            tables = []  # Lista para armazenar as tabelas extraídas

            # Itera sobre cada página do PDF
            for page_num in range(doc.page_count):
                page = doc[page_num]
                table_list = page.find_tables()  # Obtém as tabelas da página

                # Itera sobre cada tabela encontrada na página
                for table in table_list:
                    tables.append(table)

            # Fecha o arquivo PDF
            doc.close()
            return tables
        
        except fitz.EmptyFileError:
            # Trata erro caso o arquivo esteja vazio ou corrompido
            print(f"Erro: O arquivo {pdf_file} está vazio ou corrompido.")
            raise
        
        except Exception as e:
            # Trata outros erros inesperados
            print(f"Erro ao processar o arquivo {pdf_file}: {e}")
            raise

    def convert_pdf_to_markdown(self, pdf_file, output_markdown_path='./outputs/ocr_documents/markdown'):
        """
        Converte um arquivo PDF em um arquivo Markdown.

        Args:
            pdf_file (str): Caminho do arquivo PDF.
            directory (str): Diretório onde o arquivo Markdown será salvo.

        Returns:
            str: Texto em Markdown extraído do PDF.
        """
        # Garante que o diretório de saída existe
        create_directory(output_markdown_path)

        try:
            # Converte o PDF para Markdown usando pymupdf4llm
            md_text = pymupdf4llm.to_markdown(pdf_file)

            # Define o caminho do arquivo Markdown de saída
            markdown_path = pathlib.Path(output_markdown_path) / "document_pymupdf.md"

            # Salva o conteúdo Markdown no arquivo
            markdown_path.write_bytes(md_text.encode('utf-8'))

            return md_text
        
        except Exception as e:
            # Trata erros durante a conversão
            print(f"Erro ao processar o arquivo {pdf_file}: {e}")
            raise e

    def convert_pdf_to_image(self, pdf_file, directory='./data/images/'):
        """
        Converte um arquivo PDF em imagens PNG por página.

        Args:
            pdf_file (str): Caminho do arquivo PDF.
            directory (str): Diretório onde as imagens serão salvas.

        Returns:
            list: Lista de nomes dos arquivos de imagens gerados.
        """
        
        # Garante que o diretório de saída existe
        create_directory(directory)

        try:
            # Abre o arquivo PDF
            doc = fitz.open(pdf_file)
            image_filenames = []  # Lista para armazenar os nomes das imagens geradas

            # Itera sobre cada página do PDF
            for page_num in range(doc.page_count):
                page = doc[page_num]

                # Gera uma imagem da página
                image = page.get_pixmap()

                # Define o nome do arquivo de imagem baseado no PDF e na página
                image_filename = create_image_path(pdf_file, page_num, None, 'png')
                image_path = os.path.join(directory, image_filename)

                # Salva a imagem em um arquivo
                image.save(image_path)

                # Adiciona o nome da imagem à lista
                image_filenames.append(image_path)

            # Fecha o arquivo PDF
            doc.close()
            return image_filenames
        
        except fitz.EmptyFileError as e:
            # Trata erro caso o arquivo esteja vazio ou corrompido
            print(f"Erro: O arquivo {pdf_file} está vazio ou corrompido.")
            raise e 
        
        except Exception as e:
            # Trata outros erros inesperados
            print(f"Erro ao processar o arquivo {pdf_file}: {e}")
            raise e

    def extract_all(self, pdf_file):
        """
        Executa todas as funções de extração de um arquivo PDF e retorna um dicionário com os resultados.

        Args:
            pdf_file (str): Caminho do arquivo PDF.

        Returns:
            dict: Dicionário com os resultados da extração.
        """
        
        try:
            # Extrai o texto do PDF
            text = self.extract_text_with_metadata(pdf_file)

            # Extrai imagens do PDF
            images = self.extract_images_pdf(pdf_file)

            # Extrai links do PDF
            links = self.extract_links_pdf(pdf_file)

            # Extrai tabelas do PDF
            tables = self.extract_tables_pdf(pdf_file)

            # Converte o PDF para Markdown
            markdown_text = self.convert_pdf_to_markdown(pdf_file)
            
            # Converte o PDF para imagens
            images = self.convert_pdf_to_image(pdf_file)

            # Retorna um dicionário com os resultados
            return {
                'page_content': text["pdf_text"],
                'metadata' : {
                    "path_images": images,
                    "tables": tables,
                    "links": links,
                    "markdown_text": markdown_text
                } 
            }
        except Exception as e:
            # Trata erros durante a extração
            print(f"Erro ao processar o arquivo {pdf_file}: {e}")
            raise

if __name__ == "__main__":
    # Instancia a classe PDFExtractor
    pdf_extractor = PDFExtractor()

    # Caminho do arquivo PDF
    pdf_file = "./data/DummyPDF.pdf"

    # Extrai todas as informações do PDF
    extracted_data = pdf_extractor.extract_all(pdf_file)

    # Exibe os resultados
    print("Texto extraído (primeiros 500 caracteres):")
    print(extracted_data['page_content'][:500])

    print("\nCaminhos das imagens extraídas:")
    for image_path in extracted_data['metadata']['path_images']:
        print(image_path)

    print("\nTabelas extraídas:")
    for table in extracted_data['metadata']['tables']:
        print(table)

    print("\nLinks extraídos:")
    for link in extracted_data['metadata']['links']:
        print(link)

    print("\nTexto em Markdown (primeiros 2000 caracteres):")
    print(extracted_data['metadata']['markdown_text'][:2000])