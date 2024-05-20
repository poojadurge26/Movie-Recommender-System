import streamlit as st
import pickle
import pandas as pd
import requests

def add_bg_from_url():
        st.markdown(
            f"""
             <style>
             .stApp {{
                 background-image: url('https://www.freepik.com/free-photo/movie-background-collage_33752468.htm#fromView=search&page=1&position=47&uuid=a19a0e3b-a500-485b-9714-cc65123e9cec');
                 background-attachment: fixed;
                 background-size: cover
             }}
             </style>
             """,
            unsafe_allow_html=True
        )
        
add_bg_from_url()

def fetch_poster(Movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=7546171017b4a2e4c4124c25dd7febb6&language=en-US".format(Movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


    
def recommend(movie):
    index = movies[movies['Movie_Name'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:
        # Fetch movie posters from API
        Movie_id = movies.iloc[i[0]].Movie_id
        recommended_movie_posters.append(fetch_poster(Movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].Movie_Name)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Assuming the 'movie_id' column needs to be renamed to 'Movie_id'
movies.rename(columns={'movie_id': 'Movie_id'}, inplace=True)

similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox('Select or type the Movie Name', movies['Movie_Name'].values) 

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    
    # Arrange in two rows with medium-sized posters
    col1, col2 = st.columns(2)
    
    with col1:
        for i in range(5):
            st.text(recommended_movie_names[i][:50])  # Display a substring of the name
            st.image(recommended_movie_posters[i], width=250)  # Adjust width as needed
    
    with col2:
        for i in range(5, 10):
            st.text(recommended_movie_names[i][:50])
            st.image(recommended_movie_posters[i], width=250)
