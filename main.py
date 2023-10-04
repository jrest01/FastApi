from fastapi import FastAPI, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from typing import  List
from fastapi.encoders import jsonable_encoder


from models import  User, JWTBearer, Movie
from data import movies
from config import create_config_api
from jwt_manager import create_token

from config.database import Base, engine, Session
from models.movie import Movie as MovieModel



app = FastAPI()
create_config_api(app)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['Home', 'two'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin123':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)    


@app.get('/movies', tags=['movies'], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() :
    db = Session()
    result = db.query(MovieModel).all()
    return (JSONResponse(status_code=200, content=jsonable_encoder(result)))


@app.get('/movies/{movie_id}', tags=['movies'] )
def get_movie(movie_id:int=Path(ge=1, le=2000)) :
    """
        Using route params
    """
    try:
        db = Session()
        result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

        if not result:
            return JSONResponse(status_code=404, content={'message':'Not found'})
        else:
            return JSONResponse(status_code=200,content=jsonable_encoder(result))
    except IndexError:
        return JSONResponse(status_code=404, content=[])
    

@app.get('/movies/', tags=['movies'], )
def get_movies_by_category(category: str=Query(min_length=5, max_length=20), year: int=Query(ge=1910, le=2024)) :
    """
        Using query params
    """
    try:
        db = Session()
        result = db.query(MovieModel).filter(MovieModel.category == category, MovieModel.year == year).all()
        if not result:
            return JSONResponse(status_code=404, content={'message':'Not found'})
        else:
            return JSONResponse(status_code=200,content=jsonable_encoder(result))
    except print(0):
        JSONResponse(status_code=404, content=[])


@app.post('/movies', tags=['movies'],  status_code=201)
def create_movie(movie: Movie) :
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message" : "Movie Regristred"})


@app.put('/movies/update/{id}', tags=['movies'],  status_code=200)
def update_movie(id: int, new_movie: Movie):
    """
        Updates a movie by id
    """
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    
    if not result:
        return JSONResponse(status_code=404, content={'message':'Not found'})

    result.title = new_movie.title
    result.overview = new_movie.overview
    result.year = new_movie.year
    result.rating = new_movie.rating
    result.category = new_movie.category

    db.commit()
    return JSONResponse(status_code=200, content={"message" : "Movie Updated"})
    
        

@app.delete('/movies/delete/{id}', tags=['movies'],  status_code=200)        
def delete_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'Not found'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message" : "Movie Deleted"})