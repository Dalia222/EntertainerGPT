import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.agents import load_tools
import os

# Set OpenAI and SerpApi API keys
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "0b0548d186b96c230d5b1abc1d47380869a88de91e7ad899de2b01ed537401b4"

# Load required tools
tools = load_tools(["serpapi"])

# Template for the prompt
template = """
    Below is an input of the movie required based on its genre and its release year and rating and language

    Your goal is to:
    - Find the movie based on the specified genre
    - Find the movie based on the specified release year, Note that: we are currently in 2024
    - Find the movie based on the specified rating  
    - Find the movie based on the specified language  

    Below is the Movie, Release Year, Rating:
    GENRE: {genre}
    RELEASE YEAR: {release_year}
    RATING: {rating}
    LANGUAGE: {language}
    YOUR RESPONSE
"""

# Initialize PromptTemplate
prompt = PromptTemplate(
    input_variables=["genre", "release_year", "rating"],  
    template=template,
)

# Function to load Language Model
def load_LLM():
    """Logic for loading the chain you want to use should go here"""
    llm = OpenAI(temperature=1)
    return llm

# Load Language Model
llm = load_LLM()

# Streamlit page configuration
st.set_page_config(page_title="EntertainerGPT", page_icon="🎬🍿", layout="centered")
st.header("Hi, I'm your EntertainerGPT!")

# Display image and description
col1, col2 = st.columns([2, 1])  
with col1:
    st.image('face-with-cinema-elements.jpg', width=450, caption='Movie time..?')

with col2:
    st.markdown("Feeling indecisive about what to watch? Type your thoughts here, and let us help you discover something exciting!")
    st.markdown("This tool is powered by [LangChain](https://www.langchain.com) and [OpenAI](https://openai.com/) and made by [@DaliaRaafat](https://github.com/Dalia222) .")

# Genre input
st.markdown("## What kind of movie are you in the mood for?")
# Function to get user input genre
def get_text():
    genre = st.text_area("", placeholder="Movie Genre...", key="movie_input", max_chars=20)
    return genre

# Get user input genre
genre = get_text()

# Release year slider
st.markdown("## Select Release Year")
min_year, max_year = 1920, 2024  # Example range
release_year_range = st.slider("Release Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Rating and language inputs
option_rating = st.selectbox(
    'Select Rating Options',
    ('Top Rated ⭐⭐⭐⭐⭐', 'Highly Rated ⭐⭐⭐⭐','Average Rating ⭐⭐⭐')
)

language = st.selectbox(
    'Select Language',
    ('English', 'Arabic', 'French')
)


# Display suggestions
st.markdown("## Suggestions 🔮:")

if genre:
    # Format the prompt with user inputs
    prompt_with_movie = prompt.format(genre=genre, rating=option_rating, release_year=release_year_range, language=language)
    # Use the Language Model to generate suggestions
    suggested_movie = llm(prompt_with_movie)
    st.write(suggested_movie)
