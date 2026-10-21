"""Run with: streamlit run project/streamlit_app/app.py"""
import streamlit as st
from project.streamlit_app.gerador import gerador
from project.streamlit_app.questionario import questionario

if "estado_inicial" not in st.session_state:
    st.session_state["estado_inicial"] = "questionario"

if st.session_state["estado_inicial"] == "gerador":
    gerador()
else:
    questionario()
