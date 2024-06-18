import streamlit as st
import random




def alterar_estado():
    
    st.session_state["estado_inicial"] = 'questionario'



def escolher_alternativa(opcao, alternativas):
    
    st.session_state["contexto"] = st.session_state["contexto"] + '\n' + alternativas[0][opcao]
 
  

def escolher_continuacao(alternativas):
   
    if "opcao" not in st.session_state:
        st.session_state["opcao"] = ""

    
    
    st.subheader('')
    st.subheader("opção de continuação")
   
    col1, col2, col3 = st.columns(3)
    
    with col1:
        confirm_button = st.button(alternativas[1][0], key = random.randint(0,42424242), on_click=escolher_alternativa, args=(0, alternativas))
        
    with col2:
        confirm_button = st.button(alternativas[1][1], key = random.randint(0,42424242), on_click=escolher_alternativa , args=(1, alternativas))
        
    with col3:
        confirm_button = st.button(alternativas[1][2], key = random.randint(0,42424242), on_click=escolher_alternativa, args=(2, alternativas))
        
        
    
def imprime_contexto(contexto):
    
    st.subheader(contexto)

def gerar_alternativas():
    
    continuacoes = [
        'hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha',
        'hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe',
        'hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi',
        'hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho',
        'huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu huhuhu '
        ]

    sumarizacoes = [
        'hahaha',
        'hehehe',
        'hihihi',
        'hohoho',
        'huhuhu'
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

    if "gerar_conto" not in st.session_state:
        st.session_state.stream = False

    if "contexto" not in st.session_state:
        st.session_state["contexto"] = contexto

    imprime_contexto(st.session_state["contexto"])

    alternativas = gerar_alternativas()
    
    escolher_continuacao(alternativas)
  
  
    st.subheader('')
  
    confirm_button = st.button('reconfigurar escolhas', on_click=alterar_estado)
