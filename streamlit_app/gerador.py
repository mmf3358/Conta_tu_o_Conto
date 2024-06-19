import streamlit as st

def alterar_estado():
    st.session_state["estado_inicial"] = 'questionario'


def confirmar_escolha(opcao_escolhida):
    return opcao_escolhida


def escolher_continuacao(alternativas):

    if "opcao" not in st.session_state:
        st.session_state["opcao"] = ""

    n_escolha = range(3)

    st.subheader("opção de continuação")
    lista_continuacao = [" ",
                   alternativas[1][0],
                   alternativas[1][1],
                   alternativas[1][2]
                  ]
    opcao = st.selectbox("opção de continuação", lista_continuacao)

    for i,sumarizacao in enumerate(alternativas[1]):
        if opcao == sumarizacao:
            opcao_escolhida = i

            confirm_button = st.button('confirmar escolha', on_click=confirmar_escolha)

            st.subheader(f"a opcao escolhida é {alternativas[1][opcao_escolhida]}")
            return opcao_escolhida




def comecar_conto():
    st.session_state.stream = not st.session_state.stream

def imprime_contexto(contexto):

    st.subheader(contexto)

def gerador():

    contexto = 'hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha hahaha'

    opcoes = [
        'hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe hehehe',
        'hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi hihihi',
        'hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho hohoho'
        ]

    sumarizacoes = [
        'hehehe',
        'hihihi',
        'hohoho'
    ]

    alternativas = [opcoes, sumarizacoes]
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    if "gerar_conto" not in st.session_state:
        st.session_state.stream = False

    if "contexto" not in st.session_state:
        st.session_state["contexto"] = contexto

    imprime_contexto(st.session_state["contexto"])

    n_alternativa = escolher_continuacao(alternativas)
    st.subheader(n_alternativa)


    if n_alternativa != None:

        escolha = alternativas[0][n_alternativa]

        st.session_state["contexto"] = st.session_state["contexto"] + "\n" + escolha



    st.subheader("gerador")
    confirm_button = st.button('reconfigurar escolhas', on_click=alterar_estado)
