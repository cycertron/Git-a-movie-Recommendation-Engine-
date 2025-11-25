# data_manager.py
# Nirajan's Task

import pandas as pd
import sys
from models import Movie

def load_data(movies_file, ratings_file):
    """
    Loads movie and rating data from CSV files.

    Handles Requirement 1.1 (Load dataset, Movie class)
    Handles Requirement 1.3 (Build dictionaries and sets)
    Handles Requirement 4.1 (Missing dataset file)

    Returns:
        tuple: Contains three data structures:
            - movies_db (dict): movie_id -> Movie object
            - users_to_ratings (dict): user_id -> set of (movie_id, rating)
            - genres_to_movies (dict): genre -> set of movie_ids
    """
    print("Loading datasets...")
    try:
        movies_df = pd.read_csv(movies_file)
        ratings_df = pd.read_csv(ratings_file)
    except FileNotFoundError as e:
        print(f"--- ERROR: Missing Data File ---")
        print(f"Could not find file: {e.filename}")
        print("Please make sure the 'ml-latest-small' folder with CSVs is "
              "in the same directory as the script.")
        sys.exit(1) # Exit the program gracefully

    # 1. Create movies_db: {movie_id -> Movie object}
    movies_db = {}
    for row in movies_df.itertuples():
        genres = row.genres.split('|')
        movies_db[row.movieId] = Movie(row.movieId, row.title, genres)

    # 2. Calculate average ratings and update Movie objects
    avg_ratings = ratings_df.groupby('movieId')['rating'].mean()
    for movie_id, avg_rating in avg_ratings.items():
        if movie_id in movies_db:
            movies_db[movie_id].average_rating = avg_rating

    # 3. Create users_to_ratings: {user_id -> set((movie_id, rating))}
    users_to_ratings = {}
    for row in ratings_df.itertuples():
        users_to_ratings.setdefault(row.userId, set()).add((row.movieId, row.rating))

    # 4. Create genres_to_movies: {genre -> set(movie_id)}
    genres_to_movies = {}
    for movie in movies_db.values():
        for genre in movie.genres:
            genres_to_movies.setdefault(genre, set()).add(movie.movie_id)

    print("Data loading complete.")
    return movies_db, users_to_ratings, genres_to_movies
