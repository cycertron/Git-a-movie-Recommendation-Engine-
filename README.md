Git-a-Movie — Python Recommendation Engine
Overview

Git-a-Movie is a Python-based movie recommendation engine designed to help users discover new films using similarity metrics and preference modeling. The system applies information retrieval techniques, algorithmic ranking, and modular OOP design to generate accurate and scalable movie recommendations. It features efficient data processing, clear architecture, and a simple CLI interface for interactive movie queries.

Key Features

Personalized recommendation engine using similarity scoring across movie metadata

Genre, rating, and popularity filters for targeted movie discovery

Modular code structure (data loaders, model layer, recommender engine) for easy maintenance

Fast computation using Python and NumPy

Command-line interface (CLI) for querying and retrieving recommendations

Technical Highlights

Implemented Cosine similarity, Jaccard similarity, and TF-IDF weighting for ranking relevance

Utilized NumPy vectorization to accelerate scoring and reduce computation time

Added LRU caching to avoid recalculating frequently accessed results

Structured the codebase using object-oriented design (data manager, model modules, scoring engine)

Included evaluation via precision@k, recall@k, and NDCG metrics

How to Run

Clone the repository:

git clone https://github.com/cycertron/Git-a-movie-Recommendation-Engine-.git
cd Git-a-movie-Recommendation-Engine-


Run the main application:

python main.py


Run the recommendation engine directly:

python recommender.py

Project Structure
Git-a-movie-Recommendation-Engine-/
├── data_manager.py        # Loads, cleans, and structures movie data  
├── models.py              # Similarity functions and TF-IDF weighting  
├── recommender.py         # Core recommendation engine  
├── movie_app.py           # CLI interface  
├── main.py                # Entry point  
├── ml-latest-small/       # MovieLens dataset  
└── README.md  
