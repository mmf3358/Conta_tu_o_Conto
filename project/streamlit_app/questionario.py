import streamlit as st
import os
import base64

from project.streamlit_app.streamlit_utils import *



@st.cache_data
def get_base64_of_bin_file(bin_file):
    ###  Codificador da imagem
    
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()



def Define_imagem_de_fundo(png_file):
    ###  Define a imagem de fundo
    
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
        <style>
        .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        }
        </style>
        ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


def questionario():
    
    st.header('la la la')
    
    
    cwd = os.getcwd()
    bg_image_file = f"{cwd}/project/streamlit_app/images/Fundo_01 copy.png"
    style_css_file = f"{cwd}/project/streamlit_app/style.css"

    with open( style_css_file ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    
    Define_imagem_de_fundo(bg_image_file)
    

def alterar_estado():
    st.session_state["estado_inicial"] = 'gerador'

def questionario():
    st.subheader("questionario")
    confirm_button = st.button('gerar conto', on_click=alterar_estado)