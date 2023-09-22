from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "First FastAPI App"
app.version = '0.0.1'

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
         ' overview': "Fast and Furious",
         ' year': 2009,
         ' rating': 9,
         ' category': 'Acción'    
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
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    new_movie = {
        'id':id,
        'title':title,
        'overview':overview,
        'year':year,
        'rating':rating,
        'category':category,
    }
    movies.append(new_movie)
    return movies