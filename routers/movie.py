from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from middelwares.jwt_beater import JWTBearer

from config.database import Session
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() :
    db = Session()
    result = MovieService(db).get_movies()
    return (JSONResponse(status_code=200, content=jsonable_encoder(result)))


@movie_router.get('/movies/{movie_id}', tags=['movies'] )
def get_movie(movie_id:int=Path(ge=1, le=2000)) :
    """
        Using route params
    """
    try:
        db = Session()
        result = MovieService(db).get_movie(movie_id)

        if not result:
            return JSONResponse(status_code=404, content={'message':'Not found'})
        else:
            return JSONResponse(status_code=200,content=jsonable_encoder(result))
    except IndexError:
        return JSONResponse(status_code=404, content=[])
    

@movie_router.get('/movies/', tags=['movies'], )
def get_movies_by_category(category: str=Query(min_length=5, max_length=20)) :
    """
        Using query params
    """
    try:
        db = Session()
        result = MovieService(db).get_movies_by_category(category)
        if not result:
            return JSONResponse(status_code=404, content={'message':'Not found'})
        else:
            return JSONResponse(status_code=200,content=jsonable_encoder(result))
    except print(0):
        JSONResponse(status_code=404, content=[])


@movie_router.post('/movies', tags=['movies'],  status_code=201)
def create_movie(movie: Movie) :
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message" : "Movie Regristred"})


@movie_router.put('/movies/update/{id}', tags=['movies'],  status_code=200)
def update_movie(id: int, new_movie: Movie):
    """
        Updates a movie by id
    """
    db = Session()
    result = MovieService(db).update_movie(id, new_movie)
    
    if not result:
        return JSONResponse(status_code=404, content={'message':'Not found'})
    
    return JSONResponse(status_code=200, content={"message" : "Movie Updated"})
    
        

@movie_router.delete('/movies/delete/{id}', tags=['movies'],  status_code=200)        
def delete_movie(id: int):
    db = Session()
    result = MovieService(db).delete_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message':'Not found'})
    
    return JSONResponse(status_code=200, content={"message" : "Movie Deleted"})