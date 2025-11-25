# models.py
# Nirajan's Task

class Movie:
    """
    Represents a single movie.
    """
    def __init__(self, movie_id, title, genres):
        """
        Initializes a Movie object.

        Args:
            movie_id (int): The movie's unique ID.
            title (str): The movie's title.
            genres (list): A list of strings representing the movie's genres.
        """
        self.movie_id = movie_id
        self.title = title
        self.genres = genres
        self.average_rating = 0.0  # Will be calculated and set by DataManager

    def get_genres_str(self):
        """Returns a string representation of the movie's genres."""
        return "|".join(self.genres)

    def __str__(self):
        """String representation for easy printing."""
        return (f"{self.title} ({self.get_genres_str()}) - "
                f"Avg Rating: {self.average_rating:.2f}")

    def __repr__(self):
        """Official string representation."""
        return f"Movie(id={self.movie_id}, title='{self.title}')"
