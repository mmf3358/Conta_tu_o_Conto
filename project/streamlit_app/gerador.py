"""Interactive story continuation page."""
from pathlib import Path
import streamlit as st
from project.streamlit_app.streamlit_utils import Define_imagem_de_fundo
from project.app.conta_app import generate_outputs

ASSETS = Path(__file__).resolve().parent


def alterar_estado():
    st.session_state["estado_inicial"] = "questionario"
    st.session_state["alternativas"] = None


def Altera_contexto(opcao, alternativas):
    st.session_state["contexto"] += "\n\n" + alternativas[0][opcao]
    st.session_state["opcao"] = alternativas[0][opcao]
    st.session_state["alternativas"] = None


def gerador():
    st.markdown(f"<style>{(ASSETS / 'style.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    Define_imagem_de_fundo(str(ASSETS / "images" / "fundo_gerador.png"))
    st.title(st.session_state.get("titulo", "Conta Tu o Conto"))
    st.text(st.session_state.get("contexto", ""))

    if st.session_state.get("alternativas") is None:
        with st.spinner("A gerar alternativas..."):
            try:
                st.session_state["alternativas"] = generate_outputs(st.session_state["contexto"])
            except Exception as exc:
                st.error(f"Não foi possível gerar as alternativas: {exc}")
                return

    alternativas = st.session_state["alternativas"]
    st.subheader("Escolhe a continuação")
    for i, (continuacao, resumo) in enumerate(zip(*alternativas)):
        with st.expander(f"Opção {i + 1}: {resumo}"):
            st.write(continuacao)
            st.button(f"Escolher opção {i + 1}", key=f"escolha_{i}", on_click=Altera_contexto, args=(i, alternativas))
    st.button("Reconfigurar escolhas", on_click=alterar_estado)
