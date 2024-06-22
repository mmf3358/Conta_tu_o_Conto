import streamlit as st
import random
import os

from project.streamlit_app.streamlit_utils import *
from project.app.conta_app import *



def alterar_estado():
    ###  Altera estado da página
    
    st.session_state["estado_inicial"] = 'questionario'



def Altera_contexto(opcao, alternativas):
    ###  Actualiza estados das variaveis CONTEXTO e OPCAO
    
    st.session_state["contexto"] = st.session_state["contexto"] + "<br>" + alternativas[0][opcao]
    st.session_state["opcao"] = alternativas[0][opcao]
  

def Escolher_continuacao(alternativas):
    ###  Da a escolher 3 alternativas de continuação e define uma como a escolhida 

    st.subheader('')
    st.subheader("Opções para continuação")
       
    col1, col2, col3 = st.columns(3)
    
    with col1:
        confirm_button = st.button(alternativas[1][0], key = random.randint(0,42424242), on_click=Altera_contexto, args=(0, alternativas))
        
    with col2:
        confirm_button = st.button(alternativas[1][1], key = random.randint(0,42424242), on_click=Altera_contexto , args=(1, alternativas))
        
    with col3:
        confirm_button = st.button(alternativas[1][2], key = random.randint(0,42424242), on_click=Altera_contexto, args=(2, alternativas))
        
    return st.session_state["opcao"]   
    
    
    
def Imprime_contexto(opcao, contexto):
    ###  Imprime o conto
    with st.container(height=200, border=False):
        if len(opcao) == 0:
            texto= f"<span style='color: black;'>{contexto}</span>"
        else:
            texto= f"<span style='color: gray;'>{contexto[:-len(opcao)]}</span> " + f"<span style='color: black;'>{opcao}</span>"

        st.markdown(texto, unsafe_allow_html=True)
        
  
  

def Gerar_alternativas(contexto):
    ### Pega dos modelos alternativas para o cont
    cont, sum = generate_outputs(contexto)
    alternativas = [cont, sum]
    
    return alternativas

    

def gerador():
    ### Gerador dos possiveis contextos de conto a partir de IA Generativa
    cwd = os.getcwd()
    bg_image_file = f"{cwd}/project/streamlit_app/images/fundo_gerador.png"
    style_css_file = f"{cwd}/project/streamlit_app/style.css"

    with open( style_css_file ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    Define_imagem_de_fundo(bg_image_file)
    titulo = st.session_state["titulo"]
    st.markdown(f'<p class="titulo">{titulo}</p>', unsafe_allow_html=True)
    
    Imprime_contexto(st.session_state["opcao"], st.session_state["contexto"])

    alternativas = Gerar_alternativas(st.session_state["contexto"])
    
    Escolher_continuacao(alternativas)
      
    col1, col2, col3 = st.columns(3)

    ### Botao de mudança de página
    with col2:
        st.header('')
        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
        confirm_button = st.button('reconfigurar escolhas', on_click=alterar_estado, use_container_width=True)


    