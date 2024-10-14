import streamlit as st
import os
import pandas as pd 
import re
from openai import OpenAI

st.set_page_config(
    page_title="Material de Aula MAT020",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded")

 
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

# Widget de seleção de aula
aula_selecionada = st.sidebar.selectbox('Selecione uma aula:', aulas)
 
caminho_aula = os.path.join(diretorio_aulas, aula_selecionada)
conteudo_aula = ler_aula(caminho_aula)
st_markdown(conteudo_aula)
 

abas = ['Resumo AI', 'Lista de Insights AI', 'Exercícios AI']

aba1, aba2, aba3 = st.tabs(abas)

with aba1:
    st.header(abas[0]) 
with aba2:
    st.header(abas[1]) 
with aba3:
    st.header(abas[2])  


# Configurações de API 
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

 
# Configurações de modelo e carregamento de instruções do assistente
modelo = 'gpt-4o-mini'
 

# Mensagem inicial do assistente no chat
prompt = f"""
Você é um assistente de professor cuja tarefa é escrever exercicios baseado no <material de aula>.
O exercicio deve ser um teste, com 4 alternativas de resposta, da qual apenas uma seja correta. 
Você deve elaborar 5 exercícios e apresentá-los sequencialmente. Os exercícios devem abranger todo o conteúdo do <material de aula>
O teste deve ter um nivel de dificuldade médio para desafiador.
No seu output, deve contar apenas o exercício, nada a mais, nada a menos. 
Use formatação para destacar o que for importante e emojis quando pertinente (nao exagere).
Não apresente a resposta correta. 
Seja objetivo e preciso na escrita do exercício. Varie Bastante as ideias também. 
Use um parâmetro de temperatura alto.

<material de aula>
{conteudo_aula}
</material de aula>
 """ 

if st.button('Gerar Exercício AI'): 
    # Faz uma requisição à API OpenAI para gerar a resposta do assistente
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=modelo,
            messages= [{"role": "user", "content": prompt}],
            stream=True
        )

        # Exibe a resposta em tempo real
        response = st.write_stream(stream)
