from models.movie import Movie as MovieModel
from schemas.movie import Movie



class MovieService():
    def __init__(self, db):
        self.db = db

    def get_movies(self):
        return self.db.query(MovieModel).all()

    def get_movie(self, id: int):
        return self.db.query(MovieModel).filter(MovieModel.id == id).first()
    
    def get_movies_by_category(self, category):
        return self.db.query(MovieModel).filter(MovieModel.category == category).all()
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()

    def update_movie(self, id: int, new_movie: Movie):
        movie = self.get_movie(id = id)

        if not movie:
            return False
        
        movie.title = new_movie.title
        movie.overview = new_movie.overview
        movie.year = new_movie.year
        movie.rating = new_movie.rating
        movie.category = new_movie.category

        self.db.commit()
        return True
    
    def delete_movie(self, id):
        movie = self.get_movie(id)
        if not movie:
            return False
        self.db.delete(movie)
        self.db.commit()
        
        return True