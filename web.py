import streamlit as st 
import pickle
import requests
import gzip

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

movies = pickle.load(open('movies_list.pkl', 'rb'))

with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

movies_list = movies['title'].values

st.header('Movies Recommendation System')

selected_movie = st.selectbox('Select a movie:', movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movies = []
    recommend_posters = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_posters

if st.button('Show recommendations'):
    movie_names, movie_posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            st.text(movie_names[i])
            st.image(movie_posters[i])
