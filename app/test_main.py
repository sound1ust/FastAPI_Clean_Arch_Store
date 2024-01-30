from fastapi import FastAPI, Response
from datetime import datetime

app = FastAPI()


@app.get("/")
def root(response: Response):
    now = datetime.now()
    response.set_cookie(key="last_visit", value=now)
    response.set_cookie(key="ok", value="Yes", secure=True)
    return {"message": "Cookies setted up"}
