

import streamlit as st

def contato() -> None:

    # img = get_img_as_base64("images/clouds.png")

    # page_bg_img = f"""
    # <style>
    # [data-testid="stAppViewContainer"] > .main {{
    # background-image: url("data:image/png;base64,{img}");
    # background-size: 100%;
    # background-position: center;
    # background-repeat: no-repeat;
    # background-attachment: fixed;
    # }}

    # [data-testid="stHeader"] {{
    # background: rgba(0,0,0,0);
    # }}

    # [data-testid="stToolbar"] {{
    # right: 2rem;
    # }}
    # </style>
    # """

    # st.markdown(page_bg_img, unsafe_allow_html=True)

    person1 = {
        "name": "Batata 1",
        "photo": Image.open("images/potato.jpg"),
        "linkedin": "https://www.linkedin.com/in/Nuno/"
    }

    person2 = {
        "name": "Batata 2",
        "photo": Image.open("images/potato.jpg"),
        "linkedin": "https://www.linkedin.com/in/Vick/"
    }

    person3 = {
        "name": "Batata 3",
        "photo": Image.open("images/potato.jpg"),
        "linkedin": "https://www.linkedin.com/in/Rafa/"
    }

    st.title("Manda um Alô!")

    contact_info = st.container()

    col1, col2, col3 = contact_info.columns(3)

    with col1:
        st.image(person1["photo"], use_column_width=True)
        st.write(f"**{person1['name']}**")
        st.write(f"[LinkedIn]({person1['linkedin']})")

    with col2:
        st.image(person2["photo"], use_column_width=True)
        st.write(f"**{person2['name']}**")
        st.write(f"[LinkedIn]({person2['linkedin']})")

    with col3:
        st.image(person3["photo"], use_column_width=True)
        st.write(f"**{person3['name']}**")
        st.write(f"[LinkedIn]({person3['linkedin']})")

    contact_info.header("Manda um Alô!")
    contact_info.markdown("### Nosso Time")
    contact_info.markdown("#### Agradecemos o seu interesse e aceitamos feedbacks.")

    st.write('---')

    st.write('Copyright 2024. Todos os direitos reservados.')
