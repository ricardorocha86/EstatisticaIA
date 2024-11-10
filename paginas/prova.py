import streamlit as st
from openai import OpenAI
import os

openai_api_key =  st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)



modelo = 'gpt-4o-mini'  
 

# Carregar as aulas a partir dos arquivos .txt
def carregar_aulas():
    aulas = {}
    pasta = 'aulas'
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith('.txt'):
            caminho = os.path.join(pasta, nome_arquivo)
            with open(caminho, 'r', encoding='utf-8') as file:
                # Extrair o nome da aula a partir do nome do arquivo
                nome_aula = os.path.splitext(nome_arquivo)[0].replace('_', ' ').title()
                aulas[nome_aula] = file.read()
    return aulas

# Função para gerar o teste usando a API da OpenAI
def gerar_teste(conteudo):
    prompt = f"""
    Você é um professor que cria provas para os alunos com base no conteúdo fornecido entre as tags abaixo.

    <conteudo>
    {conteudo}
    </conteudo>

    Por favor, crie uma prova com exatamente 5 questões dissertativas sobre o conteúdo acima. 
    Quando fizer um exemplo, certifique-se de colocar em contextos diferentes dos apresentados no conteudo. 
    **Estrutura da Prova**:
    
    1. Cada questão deve começar com o número da questão seguido de um ponto (ex: "1.").
    2. Todas as questões devem ser dissertativas, claras e de níveis variados.
    3. Cada questão deve abordar um aspecto específico do conteúdo: 
       - Questão 1: Introduza uma pergunta sobre a **compreensão básica** do conteúdo.
       - Questão 2: Proponha uma questão que exija esboçar gráficos de histograma e boxplots. Invente contexto interessante com amostra inventanda de tamanho em torno de 12- 15.
       - Questão 3: Crie uma questão que envolva **cálculos** baseados em exemplo inventado.
       - Questão 4 Crie uma questão que envolva **cálculos** baseados em exemplo inventado, mas em assunto diferente da questão 3.
       - Questão 5: Faça uma pergunta sobre **teoria** aprofundada.
       - Questão 6: Pergunte sobre **aplicações práticas** ou **implicações** do conteúdo. Simule uma situação hipotética.  
    
    **Formato da Prova**:
    - Título: '**Prova de Estatística Básica**'
    - Instrua o aluno a ler atentatamente cada questão e justificar todas as respostas.
    - Use a seguinte estrutura para cada questão:
      - "N. [Pergunta clara e concisa]"
      - Certifique-se de que todas as perguntas sigam este formato, e mantenha o padrão de formatação consistente entre as provas.
    - Exemplo de Formato:
      1. [Pergunta sobre compreensão]
      2. [Pergunta sobre visualização]
      3. [Pergunta envolvendo cálculos 1]
      4. [Pergunta envolvendo cálculos 2]
      5. [Pergunta sobre teoria]
      6. [Pergunta sobre aplicações práticas]

    - Uma mensagem motivadora de boa prova. 
    Lembre-se de incentivar o pensamento crítico em todas as questões e seguir exatamente o formato e sequência especificados.
"""

    stream = client.chat.completions.create(
        model = modelo, 
        messages = [{"role": "user", "content": prompt}],
        stream = True)

    return stream


 




st.title('Gerador de Provas')

aulas = carregar_aulas()
aulas_selecionadas = st.multiselect(
    'Selecione as aulas que deseja ser avaliado:',
    list(aulas.keys()),
    default=list(aulas.keys())  # Define todas as aulas como selecionadas por padrão
)

if st.button('✨ Gerar Prova AI'):
    if not aulas_selecionadas:
        st.warning('Por favor, selecione pelo menos uma aula.')
    else:
        conteudo_selecionado = '\n'.join([aulas[aula] for aula in aulas_selecionadas])
        with st.spinner('Gerando a prova...'):
            prova = gerar_teste(conteudo_selecionado) 
        st.write_stream(prova)







st.divider()








