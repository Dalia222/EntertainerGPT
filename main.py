import streamlit as st

st.set_page_config(page_title="EntertainerGPT", page_icon="🎬🍿", layout="centered")
st.header("Hi, I'm your EntertainerGPT!")

col1, col2 = st.columns([2, 1])  
with col1:
    st.image('face-with-cinema-elements.jpg', width=450, caption='Movie time..?')

with col2:
    st.markdown("Feeling indecisive about what to watch? Type your thoughts here, and let us help you discover something exciting!")
    st.markdown("This tool is powered by [LangChain](https://www.langchain.com) and [OpenAI](https://openai.com/) and made by [@DaliaRaafat](https://github.com/Dalia222) .")

st.markdown("## What kind of movie are you in the mood for?")

col1,col2 = st.columns(2)
with col1:
    option_release_date = st.selectbox(
        'Select Release Year',
        ('Past Year 📅', 'Past Decade 📅📅', 'All Time 🕰️')
    )
with col2:
    option_rating = st.selectbox(
        'Select Rating Options',
        ('Top Rated ⭐⭐⭐⭐⭐', 'Highly Rated ⭐⭐⭐⭐','Average Rating ⭐⭐⭐')
    )
def get_text():
    input_text = st.text_area("", placeholder="Movie Genre...", key="movie_input", max_chars=20)
    return input_text

movie_input = get_text()

st.write(movie_input)

st.markdown("## Suggestions:")

if movie_input:
    st.write(movie_input)