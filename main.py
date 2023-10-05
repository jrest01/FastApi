from fastapi import FastAPI
from fastapi.responses import HTMLResponse


from middelwares.error_handler import ErrorHandler
from config import create_config_api

from config.database import Base, engine
from routers.movie import movie_router
from routers.user import user_router


app = FastAPI()
create_config_api(app)

app.add_middleware(ErrorHandler)

app.include_router(movie_router)
app.include_router(user_router)


Base.metadata.create_all(bind=engine)

@app.get('/', tags=['Home', 'two'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')