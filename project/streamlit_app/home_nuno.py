


import streamlit as st
import base64



@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('Fundo_01.png')

""" def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(image_url):
    page_bg_img = '''
    <style>
    body {
    background-image: url("%s");
    background-size: cover;
    }
    </style>
    ''' % image_url

    st.markdown(page_bg_img, unsafe_allow_html=True)


def button_pergunta():
    st.session_state["escolha"] = 'gerador'

def home():

    
    set_background('images/Fundo_01.png')

    col5, col6 = st.columns([8, 2])
    
    with col5:
        st.write("Column 1")
        st.write("Content A")

# Adding elements to the second column
    with col6:
        st.write("Column 2")
        st.write("Content B")

#  """
    

    
    