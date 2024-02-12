import streamlit as st
from langchain import PromptTemplate,ConversationChain
from langchain.llms import OpenAI
from langchain.agents import load_tools
import json
import os
from datetime import datetime, timedelta

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
    YOUR RESPONSE SHOULD FOLLOW THE FOLLOWING FORMAT:
    ### Here's The suitable movie I found for you\n\n
    Title: [Insert title here]\n
    Director: [Insert director name here]\n
    Starring Actors: [List the most important actors separated by commas., at most 4 actors]\n
    Language: [Insert language here]\n
    Rating:  [Insert IMDB or Rotten tomatoes rating here]\n
    Release Year: [Insert Release Year Here]\n
    Movie Poster: [Insert movie URL based on the title, if not found it will be a placeholder.]\n
    YOUR RESPONSE:
"""

# Initialize PromptTemplate
prompt = PromptTemplate(
    input_variables=["genre", "release_year", "rating", "language"],  
    template=template,
)

# Function to load Language Model
def load_LLM():
    llm = OpenAI(temperature=1)
    return llm

# Load Language Model
llm = load_LLM()
conversation = ConversationChain(llm=llm, verbose=True)
# Streamlit page configuration
st.set_page_config(page_title="EntertainerGPT", page_icon="🎬🍿", layout="wide")
st.header("Hi, I'm your EntertainerGPT!")

# Sidebar title
st.sidebar.title("Recommended movies 🎬")

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

# Apply button
apply_button = st.button("Apply")

# Display suggestions
st.markdown("## Suggestions 🔮:")

if apply_button:
    if genre:
        st.spinner("Searching...")
        
        prompt_with_movie = prompt.format(genre=genre, rating=option_rating, release_year=release_year_range, language=language)
        
        suggested_movie = llm(prompt_with_movie)
        
        # Parse the suggested movie information
        movie_info = suggested_movie.split('\n')

        # Output the parsed movie information dynamically
        for info in movie_info:
            st.write(info)



# Get suggested movies for different time intervals
suggested_movies = st.session_state.get('suggested_movies', [])

# Get current date
current_date = datetime.now()
# Display previously suggested movie based on time intervals
st.sidebar.markdown("## Previously Suggested Movies")

# Get suggested movies for different time intervals
suggested_movies = st.session_state.get('suggested_movies', [])

# Get current date
current_date = datetime.now()

# Display previously suggested movies for different time intervals
for days, interval_name in [(0, "Today"), (3, "Previous 3 Days"), (30, "Previous 30 Days")]:
    st.sidebar.markdown(f"### {interval_name}")
    interval_date = current_date - timedelta(days=days)
    movies_in_interval = [movie for movie in suggested_movies if movie]
    if movies_in_interval:
        for movie in movies_in_interval:
            st.sidebar.write(movie)
    else:
        st.sidebar.write("No suggestions")
