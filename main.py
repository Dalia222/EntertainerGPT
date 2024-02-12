import streamlit as st
from langchain import PromptTemplate, ConversationChain
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.memory import ConversationBufferMemory
import json
import os
from datetime import datetime, timedelta

# Set OpenAI and SerpApi API keys
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "0b0548d186b96c230d5b1abc1d47380869a88de91e7ad899de2b01ed537401b4"

# Load required tools
tools = load_tools(["serpapi"])

# Templates for the prompt
template = """
    Below is an input of the movie required based on its genre and its release year and rating and language 

    Your goal is to:
    - Find the movie based on the specified genre
    - Find the movie based on the specified release year, Note that: we are currently in 2024
    - Find the movie based on the specified rating  
    - Find the movie based on the specified language  
    - find a random movie if the user chooses a random movie

    Below is the Movie, Release Year, Rating:
    GENRE: {genre}
    RELEASE YEAR: {release_year}
    RATING: {rating}
    LANGUAGE: {language}
    YOUR RESPONSE SHOULD FOLLOW THE FOLLOWING FORMAT:
    ### Here's The suitable movie I found for you
    Title: [Insert title here]
    Director: [Insert director name here]
    Starring Actors: [List the most important actors separated by commas., at most 4 actors]
    Language: [Insert language here]
    Rating:  [Insert IMDB or Rotten tomatoes rating here]
    Release Year: [Insert Release Year Here]
    Movie Poster: [Insert movie URL based on the title, if not found it will be a placeholder.]
    DESCRIPTION:  [Insert short description about the movie]
    YOUR RESPONSE:
"""

template2 = """
You are a helpful Agent that generates random movies for the user 
Your goal is to:
- find a good random movie with a random genre
- find a good random movie with a random time
- find a good random movie with a random language
- find a good random movie with a random rate
YOUR RESPONSE SHOULD FOLLOW THE FOLLOWING FORMAT:
    ### Here's a Random movie I found for you
    Title: [Insert title here]
    Director: [Insert director name here]
    Starring Actors: [List the most important actors separated by commas., at most 4 actors]
    Language: [Insert language here]
    Rating:  [Insert IMDB or Rotten tomatoes rating here]
    Release Year: [Insert Release Year Here]
    Movie Poster: [Insert movie URL based on the title, if not found it will be a placeholder.]
    DESCRIPTION:  [Insert short description about the movie]
    YOUR RESPONSE:
"""

# Initialize PromptTemplate
prompt = PromptTemplate(
    input_variables=["genre", "release_year", "rating", "language"],  
    template=template,
)
prompt2 = PromptTemplate(
    input_variables=[],  
    template=template2,
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
col1, col2,col3,col4 = st.columns(4) 
with col1:
    genre = st.selectbox(
        'Select Genre',
        ('Comedy', 'Horror','Romance', 'Sci-fi', 'Thriller', 'Drama', 'Action')
    )

with col2:
    min_year, max_year = 1920, 2024 
    release_year_range = st.slider("Release Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

with col3:
# Rating and language inputs
    option_rating = st.selectbox(
        'Select Rating Options',
        ('Top Rated ⭐⭐⭐⭐⭐', 'Highly Rated ⭐⭐⭐⭐','Average Rating ⭐⭐⭐')
    )

with col4:
    language = st.selectbox(
        'Select Language',
        ('English', 'Arabic', 'French')
    )



# Apply button
apply_button = st.button("✨ Generate! ✨")
random_button = st.button("Random Movie")

# Define prompts
prompt_standard = prompt.format(genre=genre, rating=option_rating, release_year=release_year_range, language=language)
prompt_random = prompt2.format()

# Initialize suggested_movies list
suggested_movies = st.session_state.get('suggested_movies', [])
suggested_movie = ""

# Display suggestions
st.markdown("## Suggestions 🔮:")

if apply_button:
    st.spinner("Searching...")
    suggested_movie = llm(prompt_standard)
elif random_button:
    st.spinner("Searching for a random movie...")
    suggested_movie = llm(prompt_random)

# Parse the suggested movie information if a suggestion was made
if suggested_movie:
    movie_info = suggested_movie.split('\n')

    # Output the parsed movie information dynamically
    for info in movie_info[:-1]:  # Exclude the last line which is the description
        st.write(info)

    # Add the suggested movie to the history
    suggested_movies.append(suggested_movie)
    st.session_state['suggested_movies'] = suggested_movies

    # Display description in expander
    with st.expander("Description"):
        st.info(movie_info[-1])  # Display the last line which is the description

# Display previously suggested movies in the sidebar
st.sidebar.markdown("## Previously Suggested Movies")
# Display memory of each previously suggested movie in a separate section
for movie_index, suggested_movie in enumerate(suggested_movies, start=1):
    movie_info = suggested_movie.split('\n')
    st.sidebar.markdown(f"### Movie {movie_index}")
    
    # Check if movie_info has enough elements
    if len(movie_info) > 1:
        # Find the line containing the title
        title_line = next((line for line in movie_info if "Title:" in line), None)
        if title_line:
            title = title_line.split(": ")[1].strip()
            with st.sidebar.expander(f"{title}"):
                for memory_line in movie_info:
                    st.info(memory_line)
        else:
            st.sidebar.error("Title information not found.")
    else:
        st.sidebar.error("Unable to display movie information. Please try again.")
