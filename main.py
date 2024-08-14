from fastapi import FastAPI, Depends
from dotenv import load_dotenv

from security.index import check_api_key

app = FastAPI()
load_dotenv()


@app.get("/")
async def root():
    # TODO:
    return {"message": "Hello World"}


@app.get("/tasks")
async def get_tasks(

        _: None = Depends(check_api_key)
):
    #     TODO: Get all tasks from database
    return {"tasks": []}
