from fastapi import FastAPI

app = FastAPI()
app.title = "First FastAPI App"
app.version = '0.0.1'


@app.get('/', tags=['Home', 'two'])
def message():
    return 'hello world'
