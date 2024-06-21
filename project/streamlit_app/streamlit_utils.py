import streamlit as st
import os
import base64

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

