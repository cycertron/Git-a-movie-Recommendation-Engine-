# movie_app.py
# Aditya's Task

import data_manager
from recommender import GenreRecommender, UserSimilarityRecommender

class MovieApp:
    """
    Main application class for the movie recommendation system.
    Handles Requirement 5 (User Interaction)
    Handles Requirement 3 (Recursive Menu)
    Handles Requirements 4.2, 4.3 (Error Handling)
    """
    def __init__(self, movies_file, ratings_file):
        # Load all data
        (self.movies_db, 
         self.users_to_ratings, 
         self.genres_to_movies) = data_manager.load_data(movies_file, ratings_file)
        
        # Instantiate recommenders
        self.genre_recommender = GenreRecommender(
            self.movies_db, self.users_to_ratings, self.genres_to_movies)
        self.user_sim_recommender = UserSimilarityRecommender(
            self.movies_db, self.users_to_ratings, self.genres_to_movies)
        
        self.current_user_id = self._get_user()

    def _get_user(self):
        """Prompts for a user ID and validates it."""
        max_user_id = max(self.users_to_ratings.keys())
        while True:
            try:
                user_id_str = input(f"Enter your user ID (1-{max_user_id}), "
                                    "or a new ID to create a profile: ")
                user_id = int(user_id_str)
                
                if user_id in self.users_to_ratings:
                    print(f"Welcome back, User {user_id}!")
                    return user_id
                elif user_id > 0:
                    print(f"Welcome, new User {user_id}! "
                          "Your profile has been created.")
                    self.users_to_ratings[user_id] = set()
                    return user_id
                else:
                    print("User ID must be a positive number.")
            except ValueError:
                # Requirement 4.2: Handle invalid number input
                print(f"--- ERROR: Invalid Input ---")
                print("Please enter a whole number.")

    def run(self):
        """Starts the main application loop."""
        self._main_menu()

    def _main_menu(self):
        """
        Displays the main menu.
        This is the RECURSIVE feature (Requirement 3).
        """
        print("\n--- Main Menu ---")
        print("1. Search for a movie")
        print("2. Rate a movie")
        print("3. Get movie recommendations")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            self._search_menu()
        elif choice == '2':
            self._rate_movie()
        elif choice == '3':
            self._recommend_menu()
        elif choice == '4':
            print("Thank you for using the movie recommender. Goodbye! 👋")
            return # Base case for the recursion
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            
        self._main_menu() # Recursive call

    def _search_menu(self):
        """Handles the movie search submenu."""
        print("\n--- Search Menu ---")
        print("t. Search by Title")
        print("g. Search by Genre")
        choice = input("Enter choice (t/g): ").lower()
        
        if choice == 't':
            self._search_by_title()
        elif choice == 'g':
            self._search_by_genre()
        else:
            print("Invalid choice.")

    def _search_by_title(self):
        """Searches for movies by partial title match."""
        query = input("Enter movie title to search for: ").lower()
        if not query:
            return

        results = [movie for movie in self.movies_db.values() 
                   if query in movie.title.lower()]
        
        self._print_movie_list(results, "Search Results")

    def _search_by_genre(self):
        """Searches for top-rated movies by genre."""
        query = input("Enter genre to search for: ").capitalize()
        
        movie_ids = self.genres_to_movies.get(query, set())
        
        if not movie_ids:
            # Requirement 4.2: Handle movie not found (by genre)
            print(f"--- No Results ---")
            print(f"No movies found for genre: '{query}'")
            return
            
        results = [self.movies_db[mid] for mid in movie_ids]
        results.sort(key=lambda m: m.average_rating, reverse=True)
        
        self._print_movie_list(results, f"Top-Rated Movies in '{query}'")

    def _rate_movie(self):
        """Allows the current user to rate a movie."""
        query = input("Enter the EXACT movie title you want to rate: ").lower()
        
        # Find exact match
        movie_to_rate = None
        for movie in self.movies_db.values():
            if query == movie.title.lower():
                movie_to_rate = movie
                break
        
        if not movie_to_rate:
            # Requirement 4.2: Handle movie not found
            print(f"--- ERROR: Movie Not Found ---")
            print(f"No movie found with the exact title: '{query}'")
            return

        while True:
            try:
                rating_str = input(f"Enter your rating for {movie_to_rate.title} (0.5 - 5.0): ")
                rating = float(rating_str)
                
                if 0.5 <= rating <= 5.0:
                    # Add or update the rating
                    # First, remove old rating if it exists
                    self.users_to_ratings[self.current_user_id].discard(
                        (movie_to_rate.movie_id, rating)
                    )
                    # Add the new rating
                    self.users_to_ratings[self.current_user_id].add(
                        (movie_to_rate.movie_id, rating)
                    )
                    print(f"Rating for {movie_to_rate.title} saved as {rating}!")
                    
                    # Note: In a real app, you'd recalculate the movie's 
                    # average rating. We skip that for simplicity.
                    break
                else:
                    print("Invalid rating. Please enter a number between 0.5 and 5.0.")
            except ValueError:
                # Requirement 4.2: Handle invalid number input
                print("--- ERROR: Invalid Input ---")
                print("Please enter a number (e.g., 3.5 or 4).")

    def _recommend_menu(self):
        """Handles the recommendation submenu."""
        print("\n--- Get Recommendations ---")
        print("g. By your favorite genres")
        print("u. Based on users similar to you")
        choice = input("Enter choice (g/u): ").lower()
        
        recs = []
        if choice == 'g':
            recs = self.genre_recommender.recommend(self.current_user_id)
        elif choice == 'u':
            recs = self.user_sim_recommender.recommend(self.current_user_id)
        else:
            print("Invalid choice.")
            return
            
        self._print_movie_list(recs, "Your Recommendations")

    def _print_movie_list(self, movies, title):
        """Helper function to print a list of movies."""
        print(f"\n--- {title} ---")
        if not movies:
            # Requirement 4.3: Handle empty recommendations
            print("Sorry, no movies found for your request. 😢")
            print("Try rating more movies (especially 4.0+) to improve results.")
            return
            
        for i, movie in enumerate(movies[:20]): # Show max 20
            print(f"{i+1}. {movie}")
