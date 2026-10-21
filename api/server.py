
from fastapi import FastAPI

app = FastAPI(title="Stroybat API")


@app.get("/")
def home():
    return {"message": "Stroybat API работает!"}


@app.get("/status")
def status():
    return {"status": "ok"}
