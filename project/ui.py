from pathlib import Path
import base64
import logging
import streamlit as st
from project.engine import ModelUnavailable, get_engine
from project.story import StoryState, make_context

HERE = Path(__file__).resolve().parent


def page_style(generator=False):
    name = 'fundo_gerador.png' if generator else 'fundo_questionario.png'
    background = HERE / 'images' / name
    if background.is_file():
        image = base64.b64encode(background.read_bytes()).decode('ascii')
        # Both original PNGs are 1366x800, but the illustration ends at row 650.
        # Scale the illustrated 1366x651 area to cover the viewport, leaving the
        # baked-in white bottom margin below the viewport without editing the asset.
        st.markdown('<style>.stApp,[data-testid="stAppViewContainer"]{background-color:#f7f1e5;background-image:url("data:image/png;base64,' + image + '");background-position:center top;background-size:max(100vw,209.832vh) auto;background-repeat:no-repeat;background-attachment:fixed}</style>', unsafe_allow_html=True)
    st.markdown('''<style>
    .block-container{max-width:1080px;padding-top:1rem;padding-bottom:1rem}
    h1{color:#521c0b!important} h2,h3{color:#54362a!important}
    [data-testid="stMainBlockContainer"],.block-container,
    [data-testid="stMain"], [data-testid="stHeader"]{background:transparent!important}
    .st-key-story_box,.st-key-option_0,.st-key-option_1,.st-key-option_2,
    [data-testid="stForm"]{background:rgba(255,252,244,.94)!important;border-radius:14px}
    .st-key-story_box,.st-key-option_0,.st-key-option_1,.st-key-option_2{
      border:1px solid rgba(82,28,11,.24)!important;padding:1rem!important;
      box-shadow:0 4px 14px rgba(82,28,11,.07)}
    [data-testid="stText"]{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;color:#35271e}
    [data-testid="stCaptionContainer"]{color:#514438}
    div.stButton>button{white-space:normal;min-height:3rem}
    div.stButton>button,div.stDownloadButton>button{background:#fffaf0;color:#521c0b;border-color:#bd9f7a}
    .st-key-option_text_0,.st-key-option_text_1,.st-key-option_text_2{background:transparent!important}
    @media(max-width:700px){.block-container{padding:1rem!important}}
    </style>''', unsafe_allow_html=True)


def questionario():
    st.title('Conta tu o Conto')
    st.write('Cria uma personagem, escolhe um cenário e decide como a história continua.')
    st.caption('Protótipo com GPT-2 pré-treinado. O modelo original já não está disponível; o texto pode ser incoerente ou inadequado. Requer revisão humana.')
    with st.form('story_setup'):
        title = st.text_input('Título do conto', max_chars=120)
        name = st.text_input('Nome da personagem', max_chars=80)
        age = st.number_input('Idade', min_value=1, max_value=999, value=20)
        occupation = st.text_input('Ocupação', max_chars=100)
        theme = st.radio('Tema', ['Castelo', 'Floresta', 'Fadas'], horizontal=True)
        language = st.selectbox('Idioma do conto', ['Português', 'English'])
        st.caption('Português descarrega também dois tradutores. English é o modo mais leve; escreve os dados da personagem em inglês.')
        submitted = st.form_submit_button('Começar conto', use_container_width=True)
    if submitted:
        if not all(text.strip() for text in [title, name, occupation]):
            st.error('Preenche o título, o nome e a ocupação.')
            return
        lang = 'pt' if language == 'Português' else 'en'
        st.session_state['story'] = StoryState(title.strip(), make_context(name, age, occupation, theme, lang), lang)
        st.rerun()


def gerador():
    story = st.session_state['story']
    st.title(story.title)
    st.caption('Escolhe uma continuação para construir o conto, passo a passo.')
    with st.container(height=180, border=True, key='story_box'):
        for paragraph in [story.opening, *story.paragraphs]:
            st.text(paragraph)
    save_col, new_col, retry_col = st.columns(3)
    save_col.download_button('Guardar conto', story.export(), file_name='conto.txt', mime='text/plain', key='save_story', use_container_width=True)
    if new_col.button('Novo conto', key='new_story'):
        del st.session_state['story']
        st.rerun()
    if story.alternatives and retry_col.button('Gerar outras opções', key='refresh_choices'):
        story.alternatives = []
        st.rerun()
    try:
        with st.spinner('A gerar três continuações. O primeiro uso pode demorar devido aos downloads…'):
            alternatives = story.ensure_choices(get_engine().generate)
    except (ModelUnavailable, ValueError) as exc:
        st.error(str(exc))
        if st.button('Tentar novamente', key='retry_generation'):
            st.rerun()
        return
    except Exception:
        logging.exception('Unexpected application error')
        st.error('Não foi possível iniciar a geração. Consulta o terminal para ver o erro de configuração.')
        return
    st.subheader('Como continua a história?')
    for i, (column, continuation) in enumerate(zip(st.columns(3, gap='medium'), alternatives)):
        with column:
            with st.container(border=True, key=f'option_{i}'):
                st.caption(f'Opção {i + 1}')
                with st.container(height=190, border=False, key=f'option_text_{i}'):
                    st.text(continuation)
                if st.button(f'Escolher opção {i + 1}', key=f'choice_{story.round}_{i}', use_container_width=True):
                    story.choose(i)
                    st.rerun()


def main():
    st.set_page_config(page_title='Conta tu o Conto', page_icon='📖', layout='wide')
    active = 'story' in st.session_state
    page_style(generator=active)
    gerador() if active else questionario()
