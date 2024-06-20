import streamlit as st

from gerador import gerador
from questionario import questionario




if "estado_inicial" not in st.session_state:
    st.session_state["estado_inicial"] = 'questionario'

if st.session_state["estado_inicial"] == 'questionario':
      questionario()
      
      
      
elif st.session_state["estado_inicial"] == 'gerador':
      gerador()
