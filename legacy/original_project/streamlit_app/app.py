import streamlit as st

from streamlit_utils import *
from gerador import gerador
from questionario import questionario




if "estado_inicial" not in st.session_state:
      st.session_state["estado_inicial"] = 'questionario'

if st.session_state["estado_inicial"] == 'questionario':
    if "contexto" not in st.session_state:
        st.session_state["contexto"] = ""
    st.session_state["contexto"] = questionario()

elif st.session_state["estado_inicial"] == 'gerador':
      gerador()
