import streamlit as st


from project.streamlit_app.home_nuno import home 

from project.streamlit_app.contato_nuno import contato



if "escolha" not in st.session_state:
    st.session_state["escolha"] = 'pergunta'

    
if st.session_state["escolha"] == 'pergunta':
      home()
   
elif st.session_state["escolha"] == 'gerador':
      contato()
        



    
