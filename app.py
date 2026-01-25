import streamlit as st
from tmdb import (
    get_popular_movies,
    get_trending_movies,
    get_genres,
    discover_by_genre,
    search_movie,
    get_similar_movies
)
from utils import get_poster

@st.cache_data(ttl=3600)
def cached_popular():
    return get_popular_movies()

@st.cache_data(ttl=3600)
def cached_trending():
    return get_trending_movies()

@st.cache_data(ttl=3600)
def cached_genres():
    return get_genres()

@st.cache_data(ttl=1800)
def cached_genre_movies(genre_id):
    return discover_by_genre(genre_id)


def show_movies(movies):
    if not movies or not isinstance(movies, list):
        st.warning("No movies found right now. Please try again in a moment.")
        return

    cols = st.columns(5)
    for i, movie in enumerate(movies[:5]):
        with cols[i % 5]:
            poster = get_poster(movie.get("poster_path"))
            if poster:
                st.image(poster)
            st.write(movie.get("title", "Unknown"))
            st.caption(f"⭐ {movie.get('vote_average', 'N/A')}")



st.set_page_config(page_title="RecoFlix", layout="wide")

# ================= HEADER =================
st.markdown(
    """
    <h1 style='text-align: center;'>🎬 RecoFlix</h1>
    <p style='text-align: center; color: gray;'>
    Are you bored and wanna watch a movie?
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)


# ================= POPULAR MOVIES (THIS MONTH) =================
st.header("Popular Movies")
show_movies(cached_popular())


# ================= TRENDING THIS WEEK =================
st.header("Trending This Week")
show_movies(cached_trending())


# ================= GENRE SELECTION =================
st.header("Discover Popular Movies by Genre")

genres = cached_genres()
genre_map = {g["name"]: g["id"] for g in genres}

genre_name = st.selectbox(
    label="Choose a genre",
    options=list(genre_map.keys()),
    index=None,
    label_visibility="collapsed"
)


# ================= GENRE RESULTS =================
if genre_name:
    st.subheader(f" Popular {genre_name} Movies")

    with st.spinner("Fetching movies..."):
        movies = cached_genre_movies(genre_map[genre_name])

    if movies:
        show_movies(movies)
    else:
        st.warning("No movies found right now. Please try again in a moment.")

# ================= SEARCH BAR =================
st.header("Search for a Movie by Name")

query = st.text_input(
    label="",
    placeholder="Type a movie name",
    label_visibility="collapsed"
)

# ================= SEARCH RESULTS =================

if query:
    results = search_movie(query)
    if results:
        selected = results[0]
        st.subheader(f"🎯 Because you searched: {selected['title']}")
        similar = get_similar_movies(selected["id"])
        show_movies(similar)
    else:
        st.warning("No results found. Try a different movie.")

