import os
from scraping_data.scraping_pdf.ocr_text_pymupdf import PDFExtractor

pdf_extractor = PDFExtractor()

def each_pdf_in_folder(path):
    """
    Processa todos os arquivos PDF em um diretório ou um único arquivo PDF.

    Args:
        path (str): Caminho para o diretório ou arquivo PDF.

    Returns:
        dict: Um dicionário com o nome do PDF como chave e o texto extraído como valor.
    """
    pdf_texts = {}

    if os.path.isfile(path):  # Caso seja um arquivo único
        if path.lower().endswith('.pdf'):
            pdf_name = os.path.basename(path)
            pdf_texts[pdf_name] = pdf_extractor.extract_text_pdf(path)
    
    elif os.path.isdir(path):  # Caso seja um diretório
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    pdf_texts[file] = pdf_extractor.extract_text_pdf(pdf_path)
    else:
        print(f"O caminho {path} não é um arquivo ou diretório válido.")

    return pdf_texts