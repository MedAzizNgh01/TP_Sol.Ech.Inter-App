# fichier: main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Feedback(BaseModel):
    nom: str
    ville: str
    avis: str

@app.post("/scores")
def post_score(data: Feedback):
    return {"message": "Succès", "reçu": data}
