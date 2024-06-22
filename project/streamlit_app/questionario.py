import streamlit as st
import os
import random
from streamlit_utils import *



def Titulo_do_conto():
    ### Definir titulo
    subtitulo = "Titulo do Conto"
    st.markdown(f'<p class="subtitulo_01">{subtitulo}</p>', unsafe_allow_html=True)
    
    st.session_state["titulo"] = st.text_input("Titulo", value=None)



def Dados_personagem():
    ### Definir os dados do personagem
    subtitulo = "Dados do Personagem"
    st.markdown(f'<p class="subtitulo_01">{subtitulo}</p>', unsafe_allow_html=True)

    nome = st.text_input("Nome", value=None)
    idade = st.text_input("Idade", value=None)
    ocupacao = st.text_input("Ocupação", value=None)

    st.session_state["dados"] = [nome, idade, ocupacao]



def Selecionar_tema():
    ### Definir o tema do contexto
    col1, col2 = st.columns([6, 8])

    subtitulo = "Tema do Conto"
    st.markdown(f'<p class="subtitulo_01">{subtitulo}</p>', unsafe_allow_html=True)

    button_escolha_01 = st.session_state["tema_botao"][0]
    button_escolha_02 = st.session_state["tema_botao"][1]
    button_escolha_03 = st.session_state["tema_botao"][2]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<span id={button_escolha_01}></span>', unsafe_allow_html=True)
        st.button(
            "Tema Castelo",
            key = random.randint(0,42424242),
            on_click=Definir_tema,
            args=(0,),
            use_container_width=True)
    with col2:
        st.markdown(f'<span id={button_escolha_02}></span>', unsafe_allow_html=True)
        st.button(
            "Tema Floresta",
            key = random.randint(0,42424242),
            on_click=Definir_tema,
            args=(1,),
            use_container_width=True)
    with col3:
        st.markdown(f'<span id={button_escolha_03}></span>', unsafe_allow_html=True)
        st.button(
            "Tema Fadas",
            key = random.randint(0,42424242),
            on_click=Definir_tema,
            args=(2,),
            use_container_width=True
            )



def Definir_tema(opcao):
    ### Definir estilo do botao do tema
    st.session_state["tema_botao"] = ['"button-escolha"','"button-escolha"','"button-escolha"']
    st.session_state["tema_botao"][opcao] = '"button-escolhido"'
    st.session_state["tema"] = opcao



def alterar_estado():
    ### Mudar estado da pagina
    st.session_state["tentativa_alt_estado"] = True
    
    if st.session_state["titulo"] == None:
        st.session_state["erro"] = 3
        return 0
    if Verifica_dados() == True:
        st.session_state["erro"] = 2
        return 0
    if st.session_state["tema"] == None:
        st.session_state["erro"] = 1
        return 0
            
    st.session_state["contexto"] = Gerar_Contexto()
    st.session_state["estado_inicial"] = 'gerador'



def Gerar_Contexto():
    ### Gerar contexto a partir dos dados
    nome = st.session_state["dados"][0]
    idade = st.session_state["dados"][1]
    ocupacao = st.session_state["dados"][2]
    tema = st.session_state["tema"]

    temas = [f"Era uma vez, um {ocupacao} chamado {nome}. Tinha {idade} anos e gostava muito de aventuras em lugares misteriosos. Um dia encontrou um castelo que nunca havia visto na vida.",
             f"Numa floresta mágica, um elfo {ocupacao} chamado {nome}, de idade {idade} anos, descobriu um portal secreto que a levaria a um mundo feito de doces, onde os animais falavam a língua dos elfos.",
             f"Nos campos do Reino de Chocolate, a pequena fada {nome} era perseguida pela Rainha Malévola, que a ameaçava de aprisioná-la em um sono eterno se não revelasse os segredos da floresta mágica."]

    return temas[tema]



def Verifica_dados():
    ### Verifica a introdução dos dados
    for i in range(3):
        if st.session_state["dados"][i] == None or st.session_state["tema"] == "":
            return True
        else:
            return False



def questionario():
    ### Cria variavel de corrente
    cwd = os.getcwd()
    
    ### Importa estilos CSS
    style_css_file = f"{cwd}/project/streamlit_app/style.css"
    
    with open(style_css_file) as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    ### Define Estados iniciais
    Estados_iniciais()

    ### Imprime imagem de fundo e titulo
    bg_image_file = f"{cwd}/project/streamlit_app/images//fundo_questionario.png"
    Define_imagem_de_fundo(bg_image_file)
    titulo = "Conta Tu o Conto"
    st.markdown(f'<p class="titulo">{titulo}</p>', unsafe_allow_html=True)
    
    ### Define o titulo do conto
    Titulo_do_conto()
    
    st.subheader("")
    st.subheader("")
    
    ### Pega dados do personagem
    Dados_personagem()

    st.subheader("")

    ### Define o tema do contexto
    Selecionar_tema()

    st.subheader("")
    st.subheader("")

    ### Verifica o preenchimento
    if st.session_state["erro"] == 0:
        texto = "      "
        st.markdown(f'<p class="texto_02">{texto}</p>', unsafe_allow_html=True)
    elif st.session_state["erro"] == 1:
        texto = "Por favor, defina um Título."
        st.markdown(f'<p class="texto_02>{texto}</p>', unsafe_allow_html=True)
    elif st.session_state["erro"] == 2:
        texto = "Por favor, introduza os dados."
        st.markdown(f'<p class="texto_02">{texto}</p>', unsafe_allow_html=True)
    elif st.session_state["erro"] == 3:
        texto = "Por favor, defina um Tema."
        st.markdown(f'<p class="texto_02">{texto}</p>', unsafe_allow_html=True)
        
    ### Botao de geração do conto
    col1, col2, col3 = st.columns([4,8,4])
    with col2:
        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
        st.button(
            'Gerar Conto',
            on_click=alterar_estado,
            use_container_width=True)
