def get_poster(path):
    if path:
        return f"https://image.tmdb.org/t/p/w500{path}"
    return "https://via.placeholder.com/500x750?text=No+Poster"
