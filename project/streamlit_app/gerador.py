from utils.aux import get_img_as_base64

import streamlit as st

def gerador() -> None:

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

    st.title("Gerador de Contos")

    nome = st.session_state["nome"]
    idade = st.session_state["idade"]
    tema = st.session_state["tema"]
    corpo = st.session_state["corpo"]

    # formatted_md = f"#### **{nome}**"
    # st.subheader("Nome da Personagem Principal: ")
    # st.markdown(formatted_md, unsafe_allow_html=True)

    # formatted_md = f"#### **{corpo}**"
    # st.subheader("Tipo de corpo da Personagem Principal: ")
    # st.markdown(formatted_md, unsafe_allow_html=True)

    # formatted_md = f"#### **{idade}**"
    # st.subheader("Idade da Personagem Principal: ")
    # st.markdown(formatted_md, unsafe_allow_html=True)

    # formatted_md = f"#### **{tema}**"
    # st.subheader("Tema Escolhido: ")
    # st.markdown(formatted_md, unsafe_allow_html=True)

    if tema == "Tema 1":
        texto_tema = "estava procurando um dragão em forma de batata frita"

    if tema == "Tema 2":
        texto_tema = "estava com medo de unicórnios voadores"

    if tema == "Tema 3":
        texto_tema = "procurava uma vaga para estacionar o seu cavalo"

    if tema == "Tema 4":
        texto_tema = "andava pelo jardim de sorvetes florais"

    if tema == "Tema 5":
        texto_tema = "passeava com seu cachorro Fluffy"

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

        # PLACEHOLDEEEEER

        if contexto:

            initial_input = contexto

            contador = 0

            while contador < 3:

                # Create a text box
                initial_input = contexto

                # # Chamada na API
                # completo, resumo = api_call(initial_input)

                # completo_1 = completo[0]
                # completo_2 = completo[1]
                # completo_3 = completo[2]

                # resumo_1 = resumo[0]
                # resumo_2 = resumo[1]
                # resumo_3 = resumo[2]

                resumo_1 = "Abacaxi aqui abacaxi lá longe"
                resumo_2 = "Abacaxi aqui abacaxi lá perto"
                resumo_3 = "Abacaxi aqui abacaxi lá no meio"

                completo = ["abacaxi em algum lugar da terra",
                            "abacaxi longe do morango",
                            "abacaxi sem hortelã"]

                completo_1 = completo[0]
                completo_2 = completo[1]
                completo_3 = completo[2]


                options = [resumo_1, resumo_2, resumo_3]
                selected_option = st.selectbox("Escolha uma opção", options)

                # Update the text box with the new value
                if selected_option == options[0]:
                    text_box = completo_1
                elif selected_option == options[1]:
                    text_box = completo_2
                elif selected_option == options[2]:
                    text_box = completo_3

                # Display the text box
                st.write(text_box)

                # Create two columns
                col1, col2 = st.columns(2)

                with col1:
                    continue_button = st.button("Continuar", label="Continue com o conto")

                with col2:
                    reset_button = st.button("Reset", label="Voltar ao início")

                if continue_button:
                    initial_input = text_box
                    contador += 1

                if reset_button:
                    initial_input = ""
                    break
