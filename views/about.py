import streamlit as st
from PIL import Image

def load_view():

    st.markdown("<h1 style='text-align: Center; color: White; margin-top: -200px;'>About Us</h1>", unsafe_allow_html=True)
    


    st.header('Our Mission : ')
    mission = """
    Create easy to use digital tool for blind people to read thee local languge in braille
    """
    st.subheader(mission)

    


