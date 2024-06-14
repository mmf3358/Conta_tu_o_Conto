from streamlit_option_menu import option_menu



from navigation import get_navigation
from gerador import gerador

import streamlit as st

def home():
    st.subheader('HOME')
    st.subheader('aqui faz perguntas')
    
    def button_pergunta():
        st.session_state["escolha"] = 'gerador'
    
    confirm_button = st.button('Confirmar escolhas', on_click=button_pergunta)
  
        
       