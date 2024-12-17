from collections import namedtuple

def dict_to_namedtuple(document_dict):
    """
    Converte um dicionário em um namedtuple, permitindo o acesso aos valores como atributos.
    
    Parâmetros:
        document_dict (dict): Dicionário contendo as chaves "page_content" e "metadata".
    
    Retorno:
        namedtuple: Um objeto namedtuple com os dados do dicionário.
    """
    # Define um namedtuple com campos para conteúdo da página e metadados
    Document = namedtuple("Document", ["page_content", "metadata"])
    
    # Cria o namedtuple a partir do dicionário fornecido
    document_namedtuple = Document(
        page_content=document_dict["page_content"],
        metadata=document_dict["metadata"]
    )
    
    return document_namedtuple
