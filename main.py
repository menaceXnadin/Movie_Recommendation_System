import streamlit as st
import pickle
from dotenv import load_dotenv
import os
import requests
load_dotenv(override=True)
def fetch_poster(movie_id):
    api_key = os.environ.get('API_KEY')
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'
    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"}

    data = requests.get(url, headers=headers)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

movies_list = pickle.load(open('movies.pkl','rb'))
similar_movies = pickle.load(open('similarity.pkl','rb'))

# movies_list = movies_list['title'].values
# st.write(movies_list)
st.title('Movie Recommendation System')
st.write('Select a movie:')
selected_movie = st.selectbox('Movies', movies_list.title.values)

def recommend(movie):
    similar_list_posters = []
    movie_index = movies_list[movies_list['title']==movie].index[0]
    distances = similar_movies[movie_index]
    similar_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]
    for i in similar_list:
        similar_list_posters.append(fetch_poster(movies_list.iloc[i[0]].id))
    return similar_list_posters,similar_list


if st.button('Recommend'):
    recommendations_posters,recommendations = recommend(selected_movie)
    # print(recommendations.index(0))
    col1, col2, col3,col4,col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    for idx,i in enumerate(recommendations):
        with columns[idx]:
            st.image(recommendations_posters[recommendations.index(i)])
            st.write(movies_list.iloc[i[0]].title)
