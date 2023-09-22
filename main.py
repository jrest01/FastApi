from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional


app = FastAPI()
app.title = "First FastAPI App"
app.version = '0.0.1'

class Movie(BaseModel):
    id : Optional[int] = None 
    title : str
    overview : str
    year : int
    rating : float
    category : str

    def to_dict(self):
        dict = {
        'id': self.id,
        'title': self.title,
        'overview': self.overview,
        'year': self.year,
        'rating': self.rating,
        'category': self.category
        }
        print(dict)
        return dict


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Ficción'    
    } ,
    {
        'id': 2,
        'title': "Fast and Furious",
         'overview': "Fast and Furious",
         'year': 2009,
         'rating': 9,
         'category': 'Acción'    
    } ,
    {
        'id': 3,
        'title': 'Top Gun',
        'overview': "Top Gun",
        'year': 1,
        'rating': 9,
        'category': '1'  
    } 
]

@app.get('/', tags=['Home', 'two'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies


@app.get('/movies/{id}', tags=['movies'])
def get_movie(movie_id:int):
    """
        Using route params
    """
    try:
        return [movie for movie in movies if movie['id'] == movie_id][0]
    except IndexError:
        return{'error': 'Movie not found'}
    

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    """
        Using query params
    """
    try:
        return[movie for movie in movies if movie['category']==category and movie['year']==year ]
    except print(0):
        pass

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie.to_dict())
    return movies


@app.put('/movies/update/{id}', tags=['movies'])
def update_movie(id: int, new_movie: Movie):
    """
        Updates a movie by id
    """
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = new_movie.title
            movie['overview'] = new_movie.overview
            movie['year'] = new_movie.year
            movie['rating'] = new_movie.rating
            movie['category'] = new_movie.category

    return movies
        

@app.delete('/movies/delete/{id}', tags=['movies'])        
def delete_movie(id: int):
    for idx, movie in enumerate(movies):
        if movie['id'] == id:
            movies.pop(idx)
    
    return movies