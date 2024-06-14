import streamlit as st
from streamlit_option_menu import option_menu

def get_confirmation():
    selected = option_menu(
        menu_title="Conta Tu o Conto",
        options=["Home",
                 "Confirm",
                 "Contato"
                 ],
        icons=["house", "book", "telephone"],
        default_index=0,
        orientation="horizontal"
    )

    return selected
