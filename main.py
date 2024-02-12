import streamlit as st
from langchain import PromptTemplate, ConversationChain
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv, dotenv_values
import json
import os
from datetime import datetime, timedelta
st.set_page_config(page_title="EntertainerGPT", page_icon="🎬🍿", layout="wide")
# Load environment variables from .env file
load_dotenv()
config = dotenv_values(".env")

# Set OpenAI and SerpApi API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")

with open('./waves.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Load required tools
# tools = load_tools(["serpapi"])

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
    **Title**: [Insert title here]
    **Director**: [Insert director name here]
    **Starring Actors**: [List the most important actors separated by commas., at most 4 actors]
    **Language**: [Insert language here]
    **Rating**:  [Insert IMDB or Rotten tomatoes rating here]
    **Release Year**: [Insert Release Year Here]
    **Movie Poster**: [Insert movie URL based on the title, if not found it will be a placeholder.]
    **DESCRIPTION**:  [Insert short description about the movie]
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
    **Title**: [Insert title here]
    **Director**: [Insert director name here]
    **Starring Actors**: [List the most important actors separated by commas., at most 4 actors]
    **Language**: [Insert language here]
    **Rating**:  [Insert IMDB or Rotten tomatoes rating here]
    **Release Year**: [Insert Release Year Here]
    **Movie Poster**: [Insert movie URL based on the title, if not found it will be a placeholder.]
    **DESCRIPTION**:  [Insert short description about the movie]
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

st.header("Welcome to EntertainerGPT!")

# Sidebar title
st.sidebar.title("Recommended movies 🎬")

# Display image and description
col1, col2 = st.columns([2, 1])  
with col1:
    st.image('face-with-cinema-elements.jpg', 
             width=650,
             caption='Movie time..?',
             output_format='auto')


with col2:
    st.markdown(
        """
        <div style='padding: 20px; background-color: #f9f9f9; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: #333;'>Feeling indecisive about what to watch?</h3>
            <p style='color: #555;'>Type your thoughts here, and let me help you discover something exciting!</p>
            <p style='color: #555;'>This tool is powered by <a href="https://www.langchain.com" style='color: #0072c6; text-decoration: none;'>LangChain</a> and <a href="https://openai.com/" style='color: #0072c6; text-decoration: none;'>OpenAI</a> and made by <a href="https://github.com/Dalia222" style='color: #0072c6; text-decoration: none;'>@DaliaRaafat</a>.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
st.markdown("## What kind of movie are you in the mood for?")

# Use columns for layout
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])



# Styling for genre selectbox
with col1:
    st.markdown(
        """
        <div style='padding: 15px; border-radius: 10px; background-color: #ffffff53; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
            <h3 style='text-align: center;'>Genre 🚀</h3>
            <p style='text-align: center;'>Choose the genre that matches your mood.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    genre = st.selectbox(
        '',
        ('Comedy', 'Horror', 'Romance', 'Sci-fi', 'Thriller', 'Drama', 'Action')
    )

# Styling for release year slider
with col2:
    st.markdown(
        """
        <div style='padding: 15px; border-radius: 10px; background-color: #ffffff53; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
            <h3 style='text-align: center;'>Release Year 🕰️</h3>
            <p style='text-align: center;'>Choose the range of release years of the movie.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    min_year, max_year = 1920, 2024
    release_year_range = st.slider("", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Styling for rating selectbox
with col3:
    st.markdown(
        """
        <div style='padding: 15px; border-radius: 10px; background-color: #ffffff53; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
            <h3 style='text-align: center;'>Rating 💫</h3>
            <p style='text-align: center;'>Choose the desired rating of the movie.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    option_rating = st.selectbox(
        '',
        ('Top Rated ⭐⭐⭐⭐⭐', 'Highly Rated ⭐⭐⭐⭐', 'Average Rating ⭐⭐⭐')
    )

# Styling for language selectbox
with col4:
    st.markdown(
        """
        <div style='padding: 15px; border-radius: 10px; background-color: #ffffff53; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);'>
            <h3 style='text-align: center;'>Language 🌐</h3>
            <p style='text-align: center;'>Choose the desired language of the movie.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    language = st.selectbox(
        '',
        ('English', 'Arabic', 'French')
    )






col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    apply_button = st.button(
        "Generate! ✨", 
        key="generate_button"
    )

with col2:
    st.markdown("<div class='card'><div class='card-content'>Not sure what to watch?</div></div>", unsafe_allow_html=True)

with col3:
    random_button = st.button("Random Movie! 🎲", key="random_button")






# Define prompts
prompt_standard = prompt.format(genre=genre, rating=option_rating, release_year=release_year_range, language=language)
prompt_random = prompt2.format()

# Initialize suggested_movies list
suggested_movies = st.session_state.get('suggested_movies', [])
suggested_movie = ""

# Display suggestions
st.markdown("## Suggestions 🔮:")

if apply_button:
    with st.spinner("Looking for a good movie..."):
        suggested_movie = llm(prompt_standard)
elif random_button:
    with st.spinner("Looking for a random movie..."):
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
    with st.expander("**Description**"):
        st.info(movie_info[-1])  # Display the last line which is the description










# Display previously suggested movies in the sidebar
st.sidebar.markdown("Here you will find Previously Suggested Movies")
# Display memory of each previously suggested movie in a separate section
for movie_index, suggested_movie in enumerate(suggested_movies, start=1):
    movie_info = suggested_movie.split('\n')
    st.sidebar.markdown(f"### Movie {movie_index}")
    
    # Check if movie_info has enough elements
    if len(movie_info) > 1:
        # Find the line containing the title
        title_line = next((line for line in movie_info if "**Title**:" in line), None)
        if title_line:
            title = title_line.split(": ")[1].strip()
            with st.sidebar.expander(f"{title}"):
                for memory_line in movie_info:
                    st.info(memory_line)
        else:
            st.sidebar.error("Title information not found.")
    else:
        st.sidebar.error("Unable to display movie information. Please try again.")
