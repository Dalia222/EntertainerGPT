import streamlit as st


st.set_page_config(page_title="EntertainerGPT", page_icon=":robot:", layout="centered")
st.header('Hi, I\'m your EntertainerGPT!')

input_text = st.text_area(label="What kind of movie are you in the mood for?", placeholder="Movie Genre...",  max_chars=20)

