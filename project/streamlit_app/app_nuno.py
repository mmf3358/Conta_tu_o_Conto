import streamlit as st
import base64

from contato_nuno import home



home()

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
   
    background-size: cover;
    
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('./images/Fundo_01.png')




    
st.markdown(
    f"""
    <link href="https://fonts.googleapis.com/css2?family=Playwrite+VN:wght@100..400&display=swap" rel="stylesheet">
    <h2
    style="font-family: 'Playwrite VN', cursive;
    font-optical-sizing: auto;
    font-weight: <weight>;
    font-style: normal;
    ">Conta Tu o Conto
    </h2>""",
    unsafe_allow_html=True,
    )

