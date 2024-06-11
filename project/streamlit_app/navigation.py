import streamlit as st
from streamlit_option_menu import option_menu

def get_navigation():
    selected = option_menu(
        menu_title=None,
        options=["Home",
                 "Gerador de Contos",
                 "Contato"
                 ],
        icons=["house", "book", "telephone"],
        default_index=0,
        orientation="horizontal"
    )

    return selected
