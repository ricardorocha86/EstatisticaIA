import streamlit as st
import os
import pandas as pd 
import re
from openai import OpenAI

st.set_page_config(page_title = "Estatística IA",
                   page_icon = "🐵",
                   layout = "wide",
                   initial_sidebar_state = "expanded")
    

 
def st_markdown(markdown_string):
    parts = re.split(r"!\[(.*?)\]\((.*?)\)", markdown_string)
    for i, part in enumerate(parts):
        if i % 3 == 0:
            st.markdown(part)
        elif i % 3 == 1:
            title = part
        else:
            st.image(part)  # Add caption if you want -> , caption=title)


# Função para buscar arquivos markdown no diretório de aulas
def buscar_aulas(diretorio):
    return [f for f in os.listdir(diretorio) if f.endswith('.txt')]

# Função para ler o conteúdo de uma aula em markdown
def ler_aula(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        return f.read()

# Diretório onde as aulas estão armazenadas
diretorio_aulas = 'aulas' 

# Busca as aulas no diretório
aulas = buscar_aulas(diretorio_aulas)

def aux(x):
    return x[:-4]
# Widget de seleção de aula
aula_selecionada = st.sidebar.selectbox('Selecione uma aula:', sorted(aulas), index = len(aulas)-1, format_func = aux)
 
caminho_aula = os.path.join(diretorio_aulas, aula_selecionada)
conteudo_aula = ler_aula(caminho_aula)
st_markdown(conteudo_aula)
 
st.divider()
abas = ['Exercícios AI', 'Lista de Insights AI', 'Quiz AI']

aba1, aba2, aba3 = st.tabs(abas)

with aba1:

    st.header(abas[0]) 
    if st.button('Gerar Lista de Exercícios dessa Lição', type = 'primary'): 

        # Configurações de API 
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        client = OpenAI(api_key=openai_api_key)
        modelo = 'gpt-4o-mini'
         
        # Mensagem inicial do assistente no chat
        prompt = f"""
        Você é um assistente de professor cuja tarefa é escrever uma lista de exercicios baseado no <material de aula> abaixo.
        Você deve fazer 3 exercícios abertos e 3 exercícios de teste. Nos abertos, deve ser feita uma pergunta aberta. 
        Nos exercicios do tipo teste, deve ter uma pergunta e 4 alternativas de resposta, da qual apenas uma seja correta.
        Cada alternativa deve estar em uma linha. 
        Não diga qual resposta é a correta. 
        O output deve conter os 3 exercicios abertos seguidos dos 3 exercicios de teste, seguido de uma breve resolução dos exercícios abertos e o gabarito dos exercicios de teste, separados por sessão. 
        No seu output, deve contar apenas o exercício, nada a mais, nada a menos. 
        Use formatação quando necessário, use negrito e italico para destacar o que for importante e emojis quando pertinente. 

        <material de aula>
        {conteudo_aula}
        </material de aula>
         """ 

        # Faz uma requisição à API OpenAI para gerar a resposta do assistente
        with st.chat_message("assistant", avatar = '🐵'):
            stream = client.chat.completions.create(
                model=modelo,
                messages= [{"role": "user", "content": prompt}],
                stream=True
            )

            # Exibe a resposta em tempo real
            response = st.write_stream(stream)


with aba2:
    st.header(abas[1]) 

    if st.button('Gerar Lista de Insights dessa Lição', type = 'primary'): 

        # Configurações de API 
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        client = OpenAI(api_key=openai_api_key)
        modelo = 'gpt-4o-mini'
         
        # Mensagem inicial do assistente no chat
        prompt = f"""Você é um assistente que tem a função de utilizar um <material de aula> e processar seguindo as seguintes instruções:
        - Leia e compreenda integralmente o material de aula para captar o contexto, os tópicos abordados e a progressão dos conceitos.
        - Escreva um output que seja uma coleção de 10 insights sobre a aula.
        - Use bullet points para cada insight. 
        - use texto normal nos titulos das sessões. 
        - cada insight deve ter no máximo 140 caracteres.
        - seu output deve ser apenas, e somente apenas, a lista de insights.
        - use negrito e italico para destacar o que for importante.

        O material da aula é o seguinte:

        <material de aula>
        {conteudo_aula}
        </material de aula>
        """

        # Faz uma requisição à API OpenAI para gerar a resposta do assistente
        with st.chat_message("assistant", avatar = '🐵'):
            stream = client.chat.completions.create(
                model=modelo,
                messages= [{"role": "user", "content": prompt}],
                stream=True
            )

            # Exibe a resposta em tempo real
            response = st.write_stream(stream)



with aba3:
    st.header(abas[2])  
    st.write('Em breve 🚧')

    

