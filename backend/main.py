from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SaaS Mariage : Backend opérationnel !"}

@app.get("/status")
def get_status():
    return {"status": "En attente de connexion à la base PostgreSQL"}