

import streamlit as st

def button_gerador():
    st.session_state["escolha"] = 'pergunta'
        
def contato() -> None:
    
    st.subheader('GERADOR')
    st.subheader('aqui conta conto')
    
        
    confirm_button = st.button('Reconfigurar personagem', on_click=button_gerador)