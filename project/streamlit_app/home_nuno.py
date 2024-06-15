import streamlit as st
import warnings
import base64

# Suppress warnings
warnings.filterwarnings("ignore")


@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def button_pergunta():
    st.session_state["escolha"] = 'gerador'

def home():
    # st.subheader('HOME')
    # st.subheader('aqui faz perguntas')

    img = get_img_as_base64("project/streamlit_app/images/clouds.png")

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{img}");
    background-size: 100%;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: local;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """

    # st.markdown(page_bg_img, unsafe_allow_html=True)

    st.markdown(
    f"""
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap">
    """,
    unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <h2
        style="font-family: 'Pacifico', cursive;
        text-align: center;
        font-size: 72px;
        ">Conta Tu o Conto
        </h2>
        """,
        unsafe_allow_html=True,
    )

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

    st.subheader("Tipo de Personagem")

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

    # if selected_page == "Confirmar":
    if nome == " ":
        nome = "Introduza o nome"
    elif nome != " ":
        st.session_state["nome"] = nome
    st.session_state["idade"] = int(idade)
    st.session_state["corpo"] = corpo
    st.session_state["tema"] = tema

    # if qualquer nao existe:
    #     button
    #     st.error(DEFINA A MERDA DO NOME)

    # else:

    confirm_button = st.button('Confirmar escolhas', on_click=button_pergunta)
