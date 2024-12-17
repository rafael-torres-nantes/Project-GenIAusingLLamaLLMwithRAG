import os
import re

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)  # Cria o diretório, se necessário
        
def create_markdown_path(pdf_file, output_directory):
    pdf_filename = os.path.basename(pdf_file)
    markdown_filename = re.sub(r'\.pdf$', '', pdf_filename) + ".md"
    markdown_path = os.path.join(output_directory, markdown_filename)
    
    return markdown_path

def create_image_path(pdf_file, page_num, image_index, image_ext):
    # Define o nome do arquivo de imagem baseado no PDF e na página
    pdf_filename = os.path.basename(pdf_file)
    pdf_filename = re.sub(r'\.pdf$', '', pdf_filename)
    image_filename = f"{pdf_filename}_page{page_num+1}_img{image_index}.{image_ext}"
    
    return image_filename