import streamlit as st
import random
import os
import base64

from project.streamlit_app.streamlit_utils import *




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
    st.header("Opções para continuação")
    st.subheader('')
   
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
  
    st.title('o Conto')
   
    
    with st.container(height=200, border=False):
        
        if len(opcao) == 0:
            texto= f"<span style='color: black;'>{contexto}</span>"
        else:
            texto= f"<span style='color: gray;'>{contexto[:-len(opcao)]}</span> " + f"<span style='color: black;'>{opcao}</span>"

        st.markdown(texto, unsafe_allow_html=True)
        
  
  

def Gerar_alternativas():
    ### Pega dos modelos alternativas para o cont
    
    continuacoes = [
        'hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha',
        'hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe',
        'hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi',
        'hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho',
        'huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu '
        ]

    sumarizacoes = [
        'hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha ',
        'hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe ',
        'hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi ',
        'hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho ',
        'huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu '
        ]

    cont = []
    sum = []
    
    for i in range(3):
        rand = random.randint(0,4)
        
        cont.append(continuacoes[rand])
        sum.append(sumarizacoes[rand])
        
    alternativas = [cont, sum]
    
    return alternativas



def gerador():
    
    contexto = 'hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha'

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


    cwd = os.getcwd()
    bg_image_file = f"{cwd}/project/streamlit_app/images/Fundo_01 copy.png"
    style_css_file = f"{cwd}/project/streamlit_app/style.css"

    with open( style_css_file ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


    Define_imagem_de_fundo(bg_image_file)

    if "opcao" not in st.session_state:
        st.session_state["opcao"] = ""

    if "contexto" not in st.session_state:
        st.session_state["contexto"] = contexto


    Imprime_contexto(st.session_state["opcao"], st.session_state["contexto"])

    alternativas = Gerar_alternativas()
    
    Escolher_continuacao(alternativas)
  
    
  
    st.subheader('')
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
        confirm_button = st.button('reconfigurar escolhas', on_click=alterar_estado, use_container_width=True)


    