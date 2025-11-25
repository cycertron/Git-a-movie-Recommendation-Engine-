# main.py
# Aditya's Task

from movie_app import MovieApp
import os

# Define file paths relative to the script location
# Assumes the 'ml-latest-small' folder is in the same directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_FILE = os.path.join(BASE_DIR, "ml-latest-small", "movies.csv")
RATINGS_FILE = os.path.join(BASE_DIR, "ml-latest-small", "ratings.csv")

if __name__ == "__main__":
    print("Starting Movie Recommendation System... 🚀")
    
    # Initialize and run the application
    app = MovieApp(MOVIES_FILE, RATINGS_FILE)
    app.run()

