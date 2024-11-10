import streamlit as st


st.set_page_config(
    page_title="Estatística - Aplicativo de Aula",
    page_icon="🐵",
    layout="centered",
    initial_sidebar_state="expanded")
 
paginas = {"Páginas": [
        st.Page("paginas/aulas.py", title="Aulas", icon='📚'), 
        st.Page("paginas/chatbot.py", title="Chatbot", icon='🐒'), 
        st.Page("paginas/prova.py", title="Prova", icon='⚡'), 
    ],
    "Outras Páginas": [
        st.Page("paginas/inicial.py", title="Início", default = True), 
    ], 
}

pg = st.navigation(paginas)
pg.run()


