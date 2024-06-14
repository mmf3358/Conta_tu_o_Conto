from streamlit_option_menu import option_menu
from utils.aux import get_img_as_base64, load_lottiefile
from streamlit_lottie import st_lottie

from navigation import get_navigation
from gerador import gerador

import streamlit as st

def home():

    # img = get_img_as_base64("images/clouds.png")

    # page_bg_img = f"""
    # <style>
    # [data-testid="stAppViewContainer"] > .main {{
    # background-image: url("data:image/png;base64,{img}");
    # background-size: 100%;
    # background-position: center;
    # background-repeat: no-repeat;
    # background-attachment: fixed;
    # }}

    # [data-testid="stHeader"] {{
    # background: rgba(0,0,0,0);
    # }}

    # [data-testid="stToolbar"] {{
    # right: 2rem;
    # }}
    # </style>
    # """

    # st.markdown(page_bg_img, unsafe_allow_html=True)

    # lottie_coding = load_lottiefile("lottie_files/book.json")  # replace link to local lottie file

    # st_lottie(
    #     lottie_coding,
    #     speed=1,
    #     reverse=False,
    #     loop=True,
    #     quality="low", # medium ; high
    #     # renderer="svg", # canvas
    #     height=None,
    #     width=None,
    #     key=None,
    # )

    # st.title("Conta Tu o Conto")

    if "nome" not in st.session_state:
        st.session_state["nome"] = ""

    st.subheader("Nome do Personagem")
    nome = st.text_input(f"Nome do Personagem: ", value=st.session_state["nome"])

    # nome_button = st.button("Confirmar Nome")

    # if nome_button:
    #     st.session_state["nome"] = nome
    #     # st.write("Nome escolhido: ", nome)
    #     st.success(f"Nome escolhido: {nome}")


    if "corpo" not in st.session_state:
        st.session_state["corpo"] = ""

    st.subheader("Tipo de corpo (???????)")

    lista_tipo = [" ",
                   "Humano",
                   "Elfo",
                   "Unicórnio",
                   "Ogro",
                   "Fada",
                   "Anão"]
    corpo = st.selectbox("Tipo de personagem", lista_tipo)

    # if corpo == " ":
    #     st.error("Escolha o tipo")

    # corpo_button = st.button("Confirmar Corpo")

    # if corpo_button:
    #     st.session_state["corpo"] = corpo
    #     # st.write("Tipo de corpo escolhido: ", corpo)
    #     st.success(f"Tipo de corpo escolhido: {corpo}")

    if "idade" not in st.session_state:
        st.session_state["idade"] = 0

    st.subheader("Idade do Personagem")
    idade = st.slider("Idade do Personagem: ",
                      min_value=10,
                      max_value=80,
                      step=1,
                      value=st.session_state["idade"],
                    #   width=400,
                    #   height=200
                      )

    # idade_button = st.button("Confirmar Idade")

    # if idade_button:
    #     st.session_state["idade"] = int(idade)
    #     # st.write("Idade escolhida: ", idade, "anos")
    #     st.success(f"Idade escolhida: {idade} anos")

    if "tema" not in st.session_state:
        st.session_state["tema"] = []

    st.subheader("Tema do Conto")

    lista_tema = ["Tema do Conto", "Tema 1", "Tema 2", "Tema 3", "Tema 4", "Tema 5"]
    tema = st.selectbox("Tema do Conto", lista_tema)

    # tema_button = st.button("Confirmar Tema")

    # if tema_button:
    #     st.session_state["tema"] = tema
    #     # st.write("Tema escolhido: ", st.session_state["tema"])
    #     st.success(f"Tema escolhido: {tema}")

    confirm_button = st.button('Confirmar escolhas')
    if confirm_button:
        st.switch_page("pages/gerador.py")

    # pages = ["Confirmar"]

    # selected_page = option_menu(
    #     menu_title=None,
    #     options=pages,
    #     # icons=["house", "cloud-upload", "list-task", "gear"],
    #     menu_icon="cast",
    #     default_index=0,
    # )

    # if selected_page == "Confirmar":
        if nome == " ":
            nome = "Introduza o nome"
        elif nome != " ":
            st.session_state["nome"] = nome
        st.session_state["idade"] = int(idade)
        st.session_state["corpo"] = corpo
        st.session_state["tema"] = tema

        with open("gerador.py", "r", encoding="utf-8") as selected_page_file:
            code = selected_page_file.read()
        exec(code)





    # if confirm_button:
        if nome == " ":
            nome = "Introduza o nome"
        elif nome != " ":
            st.session_state["nome"] = nome
        st.session_state["idade"] = int(idade)
        st.session_state["corpo"] = corpo
        st.session_state["tema"] = tema

        # selected = change_page()
        # if selected == "Confirmar":
        #     gerador()

        # st.success(f"""
        #            Nome: {nome}\n
        #            Tipo: {corpo}\n
        #            Idade: {idade}\n
        #            Tema: {tema}
        #            """)
