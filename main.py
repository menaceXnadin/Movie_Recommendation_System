import streamlit as st
import pickle
from dotenv import load_dotenv
import os
import requests
load_dotenv(override=True)

def fetch_poster(movie_id):
    # Try to get API key from Streamlit secrets first, then fall back to .env
    api_key = None
    try:
        api_key = st.secrets["API_KEY"]
        print(f"DEBUG: API key loaded from secrets: {api_key[:10]}...")  # Debug log
    except KeyError:
        print("DEBUG: API key not found in secrets, trying environment variable")
        api_key = os.environ.get('API_KEY')
        if api_key:
            print(f"DEBUG: API key loaded from environment: {api_key[:10]}...")
        else:
            print("DEBUG: No API key found in environment either")

    if not api_key:
        st.error("❌ API Key Missing! Please set up your TMDB API key in Streamlit secrets.")
        return "https://via.placeholder.com/500x750?text=API+Key+Missing"

    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'
    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            # Return a placeholder image if no poster is available
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        # Return placeholder for any API errors
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"

movies_list = pickle.load(open('movies.pkl','rb'))
similar_movies = pickle.load(open('similarity.pkl','rb'))

# movies_list = movies_list['title'].values
# st.write(movies_list)
# Debug: Check if secrets are loaded
try:
    test_key = st.secrets["API_KEY"]
except KeyError:
    st.error("❌ API Key NOT found in secrets!")

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
