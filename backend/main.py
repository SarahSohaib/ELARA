from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="ELARA")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "ELARA backend running"}