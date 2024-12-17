from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Texto de exemplo usado para testar a funcionalidade de divisão em chunks
large_test_text = """

# O Primeiro Dia de Programação de João

João sempre foi um menino curioso. Desde pequeno, ele adorava desmontar brinquedos para ver como funcionavam. Quando completou 10 anos, seus pais lhe deram um presente especial: um computador. João ficou encantado e passou horas explorando todas as suas funcionalidades.

## Descobrindo a Programação

Um dia, na escola, o professor de informática mencionou algo chamado "programação". João ficou intrigado e decidiu pesquisar mais sobre o assunto. Ele descobriu que poderia criar seus próprios jogos e aplicativos, e isso o deixou muito animado.

## O Primeiro Programa

No seu primeiro dia programando, João decidiu começar com algo simples. Ele abriu um editor de texto e escreveu seu primeiro programa em Python:

    print("Olá, mundo!")

    João ficou maravilhado ao ver as palavras "Olá, mundo!" aparecerem na tela do computador. Ele não conseguia acreditar que tinha conseguido fazer o computador seguir suas instruções. A partir daquele momento, ele sabia que queria aprender mais sobre programação.

    ## Explorando Novas Possibilidades

    Com o passar do tempo, João começou a explorar outras linguagens de programação e a criar projetos mais complexos. Ele aprendeu sobre variáveis, loops, e funções, e como essas ferramentas poderiam ser usadas para resolver problemas do mundo real.

    ## Compartilhando o Conhecimento

    João também começou a compartilhar seu conhecimento com seus amigos. Ele criou um clube de programação na escola, onde ensinava outros alunos a programar. Ele adorava ver a mesma expressão de maravilha no rosto de seus amigos quando eles conseguiam fazer seus programas funcionarem.

    ## O Futuro de João

    Agora, com 15 anos, João já sabe que quer seguir carreira na área de tecnologia. Ele sonha em criar aplicativos que possam ajudar as pessoas e tornar o mundo um lugar melhor. E tudo começou com aquele simples programa que exibia "Olá, mundo!" na tela.
    # Adicionando mais conteúdo ao texto

    ## A Jornada de João Continua

    João não parou por aí. Ele começou a participar de competições de programação e hackathons. Em uma dessas competições, ele e seu time desenvolveram um aplicativo que ajudava pessoas a encontrar abrigos para animais de rua. O projeto foi um sucesso e ganhou o primeiro lugar na competição.

    ## Aprendendo com os Erros

    Como qualquer programador, João também enfrentou muitos desafios e cometeu erros ao longo do caminho. Houve momentos em que ele se sentiu frustrado e pensou em desistir. Mas ele aprendeu que os erros fazem parte do processo de aprendizado e que cada falha é uma oportunidade para melhorar.

    ## Inspirando Outros

    João começou a dar palestras em eventos de tecnologia, compartilhando sua jornada e inspirando outros jovens a seguir seus passos. Ele acreditava que a tecnologia tinha o poder de transformar vidas e queria motivar mais pessoas a aprenderem a programar.

    ## O Impacto da Programação

    Aos 18 anos, João já tinha desenvolvido vários aplicativos que estavam sendo usados por milhares de pessoas. Ele percebeu que a programação não era apenas uma habilidade técnica, mas uma ferramenta poderosa para causar um impacto positivo na sociedade.

    ## O Sonho de João

    João sonhava em criar uma startup de tecnologia que pudesse resolver problemas globais. Ele começou a estudar empreendedorismo e a buscar investidores para transformar suas ideias em realidade. Ele sabia que o caminho seria difícil, mas estava determinado a seguir em frente.

    ## A Importância da Comunidade

    João também valorizava a importância da comunidade de programadores. Ele participava de fóruns online, contribuía para projetos de código aberto e ajudava outros programadores a resolverem problemas. Ele acreditava que juntos, os programadores poderiam alcançar grandes feitos.

    ## O Legado de João

    Hoje, João é um programador renomado e um empreendedor de sucesso. Ele continua a trabalhar em projetos inovadores e a inspirar a próxima geração de programadores. Seu legado é um testemunho do poder da curiosidade, da perseverança e da paixão pela tecnologia.

    ## Conclusão

    A história de João é um lembrete de que todos nós temos o potencial de criar algo incrível. Com determinação e vontade de aprender, podemos superar qualquer desafio e transformar nossos sonhos em realidade. E tudo começa com um simples "Olá, mundo!".
"""

class TextChunkTool:
    """
    Classe para dividir textos longos em chunks menores utilizando dois métodos:
    1. `CharacterTextSplitter` - Divide com base em caracteres e separadores.
    2. `RecursiveCharacterTextSplitter` - Divide de forma recursiva, utilizando backup caso os limites sejam excedidos.
    """

    def __init__(self):
        # Configuração padrão para separador, tamanho de chunk e sobreposição
        self.separator = "\n"  # Define o separador entre os chunks
        self.chunk_size = 1000  # Tamanho máximo de cada chunk
        self.chunk_overlap = 200  # Sobreposição entre chunks
        self.length_function = len  # Função de cálculo do tamanho do texto

    def character_split_documents(self, text):
        """
        Divide o texto em chunks usando `CharacterTextSplitter`.

        Args:
            text (str): Texto a ser dividido.

        Returns:
            list: Lista de chunks resultantes da divisão.
        """
        text_splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=self.length_function
        )

        # Executa a divisão do texto em chunks
        text_chunks = text_splitter.split_text(text)
        return text_chunks

    def recursive_split_documents(self, text):
        """
        Divide o texto em chunks usando `RecursiveCharacterTextSplitter`.

        Args:
            text (str): Texto a ser dividido.

        Returns:
            list: Lista de chunks resultantes da divisão recursiva.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=self.length_function,
            is_separator_regex=False,  # Define que o separador não é um regex
        )

        # Executa a divisão recursiva do texto em chunks
        text_chunks = text_splitter.split_documents(text)
        return text_chunks
    
    
# Testando a funcionalidade com o texto exemplo
if __name__ == '__main__':
    chunks = TextChunkTool()

    # Dividindo o texto em chunks usando `split_text_into_chunks`
    text_chunks = chunks.split_text_into_chunks(large_test_text)
    
    # Imprimindo os primeiros 100 caracteres de cada chunk (limite para visualização)
    print(text_chunks[:100])
    
    # Exibindo os primeiros 100 caracteres de cada chunk (limite para visualização)
    print([chunk[:100] for chunk in text_chunks])
