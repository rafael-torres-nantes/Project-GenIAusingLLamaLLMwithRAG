# Flatten the list of documents
def flatten_documents(documents):
    return [sentence for doc in documents for sentence in doc]

# Flatten the list of metadatas
def flatten_metadatas(metadatas):
    return [meta for meta_list in metadatas for meta in meta_list]