"""Story setup form."""
from pathlib import Path
import streamlit as st
from project.streamlit_app.streamlit_utils import Define_imagem_de_fundo, Estados_iniciais

ASSETS = Path(__file__).resolve().parent


def Gerar_Contexto(nome, idade, ocupacao, tema):
    temas = [
        f"Era uma vez um {ocupacao} chamado {nome}. Tinha {idade} anos e gostava de aventuras. Um dia encontrou um castelo misterioso.",
        f"Numa floresta mágica, {nome}, um elfo {ocupacao} de {idade} anos, descobriu um portal secreto para outro mundo.",
        f"Nos campos do Reino de Chocolate, a fada {nome}, de {idade} anos, encontrou um segredo que mudaria o destino do reino.",
    ]
    return temas[tema]


def questionario():
    Estados_iniciais()
    st.markdown(f"<style>{(ASSETS / 'style.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    Define_imagem_de_fundo(str(ASSETS / "images" / "fundo_questionario.png"))
    st.title("Conta Tu o Conto")
    with st.form("configuracao"):
        titulo = st.text_input("Título do conto")
        nome = st.text_input("Nome da personagem")
        idade = st.text_input("Idade")
        ocupacao = st.text_input("Ocupação")
        tema = st.radio("Tema", ["Castelo", "Floresta", "Fadas"], horizontal=True)
        submitted = st.form_submit_button("Gerar conto")
    if submitted:
        if not all(x.strip() for x in (titulo, nome, idade, ocupacao)):
            st.error("Preenche todos os campos antes de continuar.")
            return
        st.session_state.update(
            titulo=titulo.strip(),
            dados=[nome.strip(), idade.strip(), ocupacao.strip()],
            tema=["Castelo", "Floresta", "Fadas"].index(tema),
            contexto=Gerar_Contexto(nome.strip(), idade.strip(), ocupacao.strip(), ["Castelo", "Floresta", "Fadas"].index(tema)),
            opcao="",
            alternativas=None,
            estado_inicial="gerador",
        )
        st.rerun()
