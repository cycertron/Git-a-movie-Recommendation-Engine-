# recommendationengine.py
# Saharsha's Task (Member No: 2)

from abc import ABC, abstractmethod

class Recommender(ABC):
  
    def __init__(self, movies_db, users_to_ratings, genres_to_movies):
        self.movies_db = movies_db
        self.users_to_ratings = users_to_ratings
        self.genres_to_movies = genres_to_movies

    @abstractmethod
    def recommend(self, user_id, num_recs=10):
        pass

    def _get_movies_rated_by_user(self, user_id):
        return self.users_to_ratings.get(user_id, set())

    def _get_movie_ids_rated_by_user(self, user_id):
        return {movie_id for movie_id, rating in self._get_movies_rated_by_user(user_id)}


class GenreRecommender(Recommender):
   
    def recommend(self, user_id, num_recs=10):
        user_ratings = self._get_movies_rated_by_user(user_id)
        if not user_ratings:
            return [] 
        

        genre_scores = {}
        genre_counts = {}
        for movie_id, rating in user_ratings:
            if rating >= 4.0:
                movie = self.movies_db.get(movie_id)
                if movie:
                    for genre in movie.genres:
                        genre_scores[genre] = genre_scores.get(genre, 0) + rating
                        genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        if not genre_scores:
            return [] # User hasn't liked any movies

       
        avg_genre_scores = {g: genre_scores[g] / genre_counts[g] for g in genre_scores}
        
        
        top_genres = sorted(avg_genre_scores, key=avg_genre_scores.get, reverse=True)[:3]
        
        # Get all movies from those genres
        candidate_movies = set()
        for genre in top_genres:
            candidate_movies.update(self.genres_to_movies.get(genre, set()))
            
        # Filter out movies the user has already seen
        seen_movies = self._get_movie_ids_rated_by_user(user_id)
        unseen_candidates = candidate_movies - seen_movies
        
        # Sort unseen candidates by their average rating
        sorted_candidates = sorted(
            unseen_candidates,
            key=lambda mid: self.movies_db[mid].average_rating,
            reverse=True
        )
        
        
        return [self.movies_db[mid] for mid in sorted_candidates[:num_recs]]


class UserSimilarityRecommender(Recommender):

    def recommend(self, user_id, num_recs=10):
        target_user_liked = {mid for mid, r in self._get_movies_rated_by_user(user_id) if r >= 4.0}
        if not target_user_liked:
            return [] 
        
        similar_users = [] 
        for other_id, other_ratings in self.users_to_ratings.items():
            if other_id == user_id:
                continue
            
            other_user_liked = {mid for mid, r in other_ratings if r >= 4.0}
            
           
            intersection = target_user_liked.intersection(other_user_liked)
            union = target_user_liked.union(other_user_liked)
            
            if not union:
                continue 
                
            similarity = len(intersection) / len(union)
            
            if similarity > 0.1: 
                similar_users.append((similarity, other_id))
        
        if not similar_users:
            return [] 

        
        similar_users.sort(key=lambda x: x[0], reverse=True)
        top_similar_users = similar_users[:10]
        
        
        candidate_scores = {} 
        target_user_seen = self._get_movie_ids_rated_by_user(user_id)
        
        for sim_score, other_id in top_similar_users:
            for movie_id, rating in self._get_movies_rated_by_user(other_id):
                if movie_id not in target_user_seen and rating >= 4.0:
                    weighted_rating = sim_score * rating
                    candidate_scores.setdefault(movie_id, []).append(weighted_rating)
        
        if not candidate_scores:
            return []

        
        final_scores = {mid: sum(scores) / len(scores) for mid, scores in candidate_scores.items()}
        
        
        sorted_candidates = sorted(final_scores, key=final_scores.get, reverse=True)
        
        return [self.movies_db[mid] for mid in sorted_candidates[:num_recs]]

    # -----------------------------------------------------------
    # 🔁 Recursive Function Added (Requirement 3 - Recursion)
    # -----------------------------------------------------------
    def find_similar_users_recursive(self, user_id, depth=2, visited=None):
        """
        Recursively find 'friends of friends' (similar users of similar users).
        This function satisfies the Recursion Requirement.
        """
        if visited is None:
            visited = set()
        if depth == 0:
            return set()  # Base case (stop recursion)

        visited.add(user_id)
        similar_users = set()

        target_liked = {mid for mid, r in self._get_movies_rated_by_user(user_id) if r >= 4.0}

        for other_id, other_ratings in self.users_to_ratings.items():
            if other_id == user_id or other_id in visited:
                continue
            other_liked = {mid for mid, r in other_ratings if r >= 4.0}
            if not target_liked or not other_liked:
                continue
            similarity = len(target_liked & other_liked) / len(target_liked | other_liked)
            if similarity >= 0.3:
                similar_users.add(other_id)

        # Recursive step: find similar users of similar users
        for friend_id in list(similar_users):
            similar_users |= self.find_similar_users_recursive(friend_id, depth - 1, visited)

        return similar_users
