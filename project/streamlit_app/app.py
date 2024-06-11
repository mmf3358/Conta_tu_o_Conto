import streamlit as st
from navigation import get_navigation
from home import home as home_page
from gerador import gerador
from contato import contato

selected = get_navigation()

if selected == "Home":
    home_page()
elif selected == "Gerador de Contos":
    gerador()
elif selected == "Contato":
    contato()
