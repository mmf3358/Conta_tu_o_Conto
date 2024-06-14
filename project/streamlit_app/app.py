import streamlit as st
from navigation import get_navigation
from confirm import get_confirmation
from home import home as home_page
from gerador import gerador
from contato import contato



if "escolha" not in st.session_state:
    st.session_state["escolha"] = 'pergunta'
else:
    st.session_state["escolha"] = st.session_state["escolha"] 


if st.session_state["escolha"] == 'pergunta':
    

    if "nome" not in st.session_state:
        st.session_state["nome"] = ""
        
    st.subheader("Nome do Personagem")
    nome = st.text_input(f"Nome do Personagem: ", value=st.session_state["nome"])

    if nome != None:
        st.subheader(nome)
        
if st.session_state["escolha"] == 'gerador':
    gerador()

confirm_button = st.button('Confirmar escolhas')
if confirm_button:
    st.session_state["escolha"] = 'gerador'
    

