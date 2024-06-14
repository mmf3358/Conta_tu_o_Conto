import streamlit as st
from navigation import get_navigation
from confirm import get_confirmation
from home import home 
from gerador import gerador
from contato import contato



if "escolha" not in st.session_state:
    st.session_state["escolha"] = 'pergunta'



    
if st.session_state["escolha"] == 'pergunta':
    
    home()
   
elif st.session_state["escolha"] == 'gerador':
    
    contato()
        



    
