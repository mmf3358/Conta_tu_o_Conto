import streamlit as st
import base64


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



def Estados_iniciais():
    ### Inicializa os estados inicias das variaveis persistentes
    if "tema_botao" not in st.session_state:
        st.session_state["tema_botao"] = ['"button-escolha"','"button-escolha"','"button-escolha"']

    if "tema" not in st.session_state:
        st.session_state["tema"] = None

    if "dados" not in st.session_state:
        st.session_state["dados"] = [None, None, None]

    if "opcao" not in st.session_state:
        st.session_state["opcao"] = ""

    if "contexto" not in st.session_state:
        st.session_state["contexto"] = ""

    if "tentativa_alt_estado" not in st.session_state:
        st.session_state["tentativa_alt_estado"] = False
        
    if "opcao" not in st.session_state:
        st.session_state["opcao"] = ""
        
    if "titulo" not in st.session_state:
        st.session_state["titulo"] = None
        
    if "erro" not in st.session_state:
        st.session_state["erro"] = 0


