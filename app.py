import os
import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_poster(movie_id):
    api_key = os.getenv('TMDB_API_KEY')
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'.format(movie_id))
    data=response.json()
    # return st.text(data)
    return "https://image.tmdb.org/t/p/original" +data['poster_path']

def recommend(movie):
    movie_index= movies[movies['title'].values==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate (distances)),key=lambda x:x[1],reverse=True)[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]

    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


similarity= pickle.load(open('similarity.pkl', 'rb'))
movies= pickle.load(open('movies.pkl','rb'))
st.title('Movie Recommender System')


selected_movie_name= st.selectbox(
    'Which movie would you like to get recomendations based upon? ',
    (movies['title'].values)
)

if st.button('Show Recommendations'):
    names, posters=recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
