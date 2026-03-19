import streamlit as st
import pickle
import pandas as pd
import requests
import warnings
import ssl

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Create a custom SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create a session with custom SSL adapter
session = requests.Session()
adapter = requests.adapters.HTTPAdapter()
session.mount('https://', adapter)

def fetch_poster(movie_id):
    try:
        response = session.get('https://api.themoviedb.org/3/movie/{}?api_key=462fd946a20d55e5c67bd5d88eabd71a&language=en-US'.format(movie_id), timeout=10)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except Exception as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommendation')
selected_movie_name= st.selectbox(
    'How would you like to be contacted',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])
    with col3:
        st.header(names[2])
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])