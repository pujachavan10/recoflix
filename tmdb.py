import requests
import os
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def fetch_data(endpoint, params=None):
    if params is None:
        params = {}

    params.update({
        "api_key": API_KEY,
        "language": "en-US",
        "region": "US"
    })

    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print("TMDB API error:", e)
        return {}



def get_popular_movies():
    return fetch_data(
        "discover/movie",
        {
            "sort_by": "popularity.desc"
        }
    ).get("results", [])


def get_trending_movies():
    return fetch_data("trending/movie/week").get("results", [])


def get_genres():
    return fetch_data("genre/movie/list").get("genres", [])


def discover_by_genre(genre_id):
    return fetch_data(
        "discover/movie",
        {
            "with_genres": genre_id,
            "sort_by": "popularity.desc"
        }
    ).get("results", [])



def search_movie(query):
    return fetch_data(
        "search/movie",
        {"query": query}
    ).get("results", [])


def get_similar_movies(movie_id):
    return fetch_data(
        f"movie/{movie_id}/similar"
    ).get("results", [])
