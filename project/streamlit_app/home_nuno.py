


import streamlit as st

def button_pergunta():
    st.session_state["escolha"] = 'gerador'
    
def home():
    st.subheader('HOME')
    st.subheader('aqui faz perguntas')
    
  
    confirm_button = st.button('Confirmar escolhas', on_click=button_pergunta)
    
 
        
       