from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Sentinels of Truth backend is running"}