import streamlit as st
from streamlit_option_menu import option_menu

def home():
    st.title("Conta Tu o Conto")

    if "nome" not in st.session_state:
        st.session_state["nome"] = ""

    st.subheader("Nome da Personagem Principal")
    nome = st.text_input("Defina o nome: ", value=st.session_state["nome"])

    nome_button = st.button("Confirmar Nome")

    if nome_button:
        st.session_state["nome"] = nome
        st.write("Nome escolhido: ", nome)

    if "corpo" not in st.session_state:
        st.session_state["corpo"] = ""

    st.subheader("Tipo de corpo (???????)")

    lista_corpo = ["Selecione um tipo de corpo", "Garoto", "Garota", "Jovem", "Senhor", "Senhora"]
    corpo = st.selectbox("Selecione um tipo de corpo", lista_corpo)

    corpo_button = st.button("Confirmar Corpo")

    if corpo_button:
        st.session_state["corpo"] = corpo
        st.write("Tipo de corpo escolhido: ", st.session_state["corpo"])

    if "idade" not in st.session_state:
        st.session_state["idade"] = 0

    st.subheader("Idade da Personagem Principal")
    idade = st.slider("Escolha a idade: ", min_value=10, max_value=80, step=1, value=st.session_state["idade"])

    idade_button = st.button("Confirmar Idade")

    if idade_button:
        st.session_state["idade"] = int(idade)
        st.write("Idade escolhida: ", idade, "anos")

    if "tema" not in st.session_state:
        st.session_state["tema"] = []

    st.subheader("Tema da História")

    lista_tema = ["Selecione um tema", "Tema 1", "Tema 2", "Tema 3", "Tema 4", "Tema 5"]
    tema = st.selectbox("Selecione um tema", lista_tema)

    tema_button = st.button("Confirmar Tema")

    if tema_button:
        st.session_state["tema"] = tema
        st.write("Tema escolhido: ", st.session_state["tema"])
