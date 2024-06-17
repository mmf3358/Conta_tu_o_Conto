

import streamlit as st

def button_gerador():
    st.session_state["escolha"] = 'pergunta'
     
def contato() -> None:
    
    url = 'https://taxifare.lewagon.ai/predict'
    
    if url == 'https://taxifare.lewagon.ai/predict':

        st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

    
    st.subheader('GERADOR')
    st.subheader('aqui conta conto')
    
        
    confirm_button = st.button('Reconfigurar personagem', on_click=button_gerador)