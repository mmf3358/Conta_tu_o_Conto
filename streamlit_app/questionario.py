import streamlit as st

def alterar_estado():
    st.session_state["estado_inicial"] = 'gerador'

def questionario():
    st.subheader("questionario")
    confirm_button = st.button('gerar conto', on_click=alterar_estado)