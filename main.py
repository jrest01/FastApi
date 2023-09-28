from fastapi import FastAPI, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from typing import  List


from models import Movie, User, JWTBearer
from data import movies
from config import create_config_api
from jwt_manager import create_token



app = FastAPI()
create_config_api(app)


@app.get('/', tags=['Home', 'two'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin123':
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)    


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() :
    return (JSONResponse(status_code=200, content=movies))


@app.get('/movies/{movie_id}', tags=['movies'], response_model=Movie)
def get_movie(movie_id:int=Path(ge=1, le=2000)) :
    """
        Using route params
    """
    try:
        item = [movie for movie in movies if movie['id'] == movie_id][0]
        return JSONResponse(content=item)
    except IndexError:
        return JSONResponse(status_code=404, content=[])
    

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str=Query(min_length=5, max_length=20), year: int=Query(ge=1910, le=2024)) :
    """
        Using query params
    """
    try:
        data = [movie for movie in movies if movie['category']==category and movie['year']==year ]
        return JSONResponse(content=data)
    except print(0):
        JSONResponse(status_code=404, content=[])

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) :
    movies.append(movie.to_dict())
    return JSONResponse(status_code=201, content={"message" : "Movie Regristred"})


@app.put('/movies/update/{id}', tags=['movies'], response_model=dict, status_code=200)
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

    return JSONResponse(status_code=200, content={"message" : "Movie Updated"})
        

@app.delete('/movies/delete/{id}', tags=['movies'], response_model=dict, status_code=200)        
def delete_movie(id: int):
    for idx, movie in enumerate(movies):
        if movie['id'] == id:
            movies.pop(idx)
    
    return JSONResponse(status_code=200, content={"message" : "Movie Deleted"})