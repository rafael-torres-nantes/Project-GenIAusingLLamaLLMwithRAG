from controller.controller import Controller
from scraping_data.scraping_pdf.ocr_text_pymupdf import PDFExtractor

controller = Controller()

if '__main__' == __name__:
    # Exemplo de criação e salvamento de vetores usando FAISS
    controller.run_process()
    
    
