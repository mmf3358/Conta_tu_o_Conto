import streamlit as st
import random
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def button_gerador():
    st.session_state["escolha"] = 'pergunta'

def contato() -> None:

    # st.subheader('GERADOR')
    # st.subheader('aqui conta conto')

    st.markdown(
    f"""
    <link rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap"
    >
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

    st.title("Gerador de Contos")

    nome = st.session_state["nome"]
    idade = st.session_state["idade"]
    tema = st.session_state["tema"]
    corpo = st.session_state["corpo"]

    if tema == "Tema 1":
        texto_tema = "estava procurando um dragão em forma de batata frita"

    elif tema == "Tema 2":
        texto_tema = "estava com medo de unicórnios voadores"

    elif tema == "Tema 3":
        texto_tema = "procurava uma vaga para estacionar o seu cavalo"

    elif tema == "Tema 4":
        texto_tema = "andava pelo jardim de sorvetes florais"

    elif tema == "Tema 5":
        texto_tema = "passeava com seu cachorro Fluffy"

    else:
        print("Definir tema")

    if corpo in ["Garoto", "Jovem", "Senhor"]:
        artigo = "um"
        sufixo = "o"
    else:
        artigo = "uma"
        sufixo = "a"

    if tema:
        contexto = f"Há muitos anos, em uma galáxia medieval distante, {artigo} {corpo.lower()} de {idade} anos, chamad{sufixo} {nome}, {texto_tema}..."

        formatted_md = f"#### **{contexto}**"

        st.subheader("Ideia inicial: ")
        st.markdown(formatted_md, unsafe_allow_html=True)

        # contexto entra no modelo de tradução
        # contexto traduzido vai para o modelo gerador de texto
        # output do modelo gerador de texto é resumido
        # resumo e output inteiros são traduzidos
        # resumo é mostrado em 3 opções
        # usuário escolhe uma das opções
        # output é mostrado em uma caixa de texto

        # opcoes de escolha
    #     selected_option = st.selectbox("Escolha uma opção", options)


    #     caixa de texto st.session_state[caixa de texto]

    #     select box -> alterar caixa de texto

    #     texto_caixa de texto -> alteracao no session state do input modelo

    #     input - > executar o request

    if 'initial_input' not in st.session_state:
        st.session_state['initial_input'] = ''

    def return_output(input_user) -> None:
        input_user = input_user

        output = input_user + "_batata_"

        return output

    options = ['',
               'comer',
               'fritar',
               'assar',
               'amar']

    selected_option = st.selectbox("Selecione um caminho",
                                   options,
                                   )


    def change_input_state():
        st.session_state["initial_input"] = selected_option


    def button_continuar(selected_option):
        st.session_state["initial_input"] = selected_option

    submit = st.button('Gerar Conto banana')

    if submit:

        st.subheader("Summary:")

        output = return_output(selected_option)

        text2 = output

        st.write(text2)

    continue_button = st.button('Continuar', on_click=button_continuar)

    st.write("---")

    confirm_button = st.button('Reconfigurar personagem', on_click=button_gerador)


    # confirm_button = st.button('Reconfigurar personagem', on_click=button_gerador)
