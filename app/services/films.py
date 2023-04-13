from models.movie import Movie as MovieModel
from schemas.movie import MovieAPI

class FilmsService():
    def __init__(self, db) -> None:
        self.db = db
            
    def get_films(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie_id(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).one_or_none()
        return result

    def get_films_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def get_films_by_year(self, year):
        result = self.db.query(MovieModel).filter(MovieModel.year == year).all()
        return result
    
    def get_films_by_category_and_year(self, category, year):
        result = self.db.query(MovieModel).filter(MovieModel.category == category and MovieModel.year == year).all()
        return result

    def create_movie(self, movie: MovieAPI):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return


    def update_movie(self, id: int, data: MovieAPI):
        movie_update = self.get_movie_id(id)
        movie_update.update(data.dict(exclude_unset=True))
        self.db.commit()
        self.db.refresh(movie_update)
        return
    
    def delete_movie(self, id : int):
        movie_delete = self.get_movie_id(id)
        self.db.delete(movie_delete)
        self.db.commit()
        return 
    
    def delete_all_movie(self):
        all_films_delete = self.get_films()
        for movie in all_films_delete:
            self.db.delete(movie)
        self.db.commit()
        return 