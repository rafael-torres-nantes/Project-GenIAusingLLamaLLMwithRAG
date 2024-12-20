# 🦙 Extração e Processamento de PDFs com Modelos LLAMA

## 👨‍💻 Projeto desenvolvido por: 
[Rafael Torres Nantes](https://github.com/rafael-torres-nantes)

## Índice

* 📚 Contextualização do projeto
* 🛠️ Tecnologias/Ferramentas utilizadas
* 🖥️ Funcionamento do sistema
   * 🧩 Parte 1 - Backend
* 🔀 Arquitetura da aplicação
* 📁 Estrutura do projeto
* 📌 Como executar o projeto
* 🕵️ Dificuldades Encontradas

## 📚 Contextualização do projeto

O projeto tem como objetivo criar uma solução automatizada para extrair e processar informações de arquivos PDF utilizando modelos LLAMA. O sistema foi desenhado para processar grandes volumes de documentos, extraindo texto, imagens e metadados, e armazenando-os em um banco de dados vetorial para consultas rápidas e eficientes.

## 🛠️ Tecnologias/Ferramentas utilizadas

[<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">](https://www.python.org/)
[<img src="https://img.shields.io/badge/Visual_Studio_Code-007ACC?logo=visual-studio-code&logoColor=white">](https://code.visualstudio.com/)
[<img src="https://img.shields.io/badge/Fitz-BC1A3D?logo=python&logoColor=white">](https://pypi.org/project/fitz/)
[<img src="https://img.shields.io/badge/LangChain-005C84?logo=python&logoColor=white">](https://langchain.com/)
[<img src="https://img.shields.io/badge/ChromaDB-FF9900?logo=database&logoColor=white">](https://www.chromadb.com/)
[<img src="https://img.shields.io/badge/FAISS-0073BB?logo=database&logoColor=white">](https://github.com/facebookresearch/faiss)
[<img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white">](https://github.com/)

## 🖥️ Funcionamento do sistema

### 🧩 Parte 1 - Backend

O backend da aplicação foi desenvolvido utilizando **Python**, com diversas bibliotecas para extração e processamento de PDFs, integração com modelos LLAMA e armazenamento de dados em bancos de dados vetoriais.

* **Controller**: O arquivo controller_ingestion_data.py contém a lógica responsável por gerenciar a extração de dados de arquivos PDF e a fragmentação do conteúdo.
* **Modelos LLAMA**: A integração com os modelos LLAMA para inferência e embeddings está localizada em inference_model.py e embedding_model.py.
* **Banco de Dados Vetorial**: A integração com ChromaDB e FAISS para armazenamento e consulta de dados vetoriais está em chroma_database.py e faiss_database.py.
* **Utilitários**: A pasta utils contém funções auxiliares para manipulação de arquivos e listas.

## 🔀 Arquitetura da aplicação

O sistema é baseado em uma arquitetura modular, onde diferentes componentes são responsáveis por tarefas específicas, como extração de texto, processamento de dados, integração com modelos LLAMA e armazenamento em bancos de dados vetoriais.

## 📁 Estrutura do projeto

A estrutura do projeto é organizada da seguinte maneira:

```
.
├── controller/
│   ├── controller_ingestion_data.py
│   ├── controller_rag.py
├── data/
│   ├── images/
├── database/
│   ├── chroma_db/
├── knowledge_base/
│   ├── ingestion_data/
│   ├── vector_database/
├── llama_models/
│   ├── embedding_model.py
│   ├── inference_model.py
├── main.py
├── outputs/
│   ├── ocr_documents/
├── prompt_template/
│   ├── prompts_template.py
├── requirements.txt
├── scraping_data/
│   ├── scraping_pdf/
├── scripts/
│   ├── llama.sh
├── utils/
│   ├── convert_dict_to_object.py
│   ├── file_manipulation.py
│   ├── list_manipulation.py
│   ├── send_each_pdf_file.py
└── .gitignore
```

## 📌 Como executar o projeto

Para executar o projeto localmente, siga as instruções abaixo:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o script principal:**
   ```bash
   python main.py
   ```

## 🕵️ Dificuldades Encontradas

Durante o desenvolvimento do projeto, algumas dificuldades foram enfrentadas, como:

- **Extração de texto:** A implementação de diferentes métodos de OCR para extração de texto de PDFs exigiu testes e ajustes para lidar com diferentes formatos e qualidades de arquivos.
- **Integração com modelos LLAMA:** A configuração e integração dos modelos LLAMA para inferência e embeddings foi desafiadora, exigindo ajustes finos para obter resultados precisos.
- **Armazenamento vetorial:** A configuração e uso de bancos de dados vetoriais como ChromaDB e FAISS para armazenamento e consulta eficiente de dados vetoriais foi um desafio contínuo.
