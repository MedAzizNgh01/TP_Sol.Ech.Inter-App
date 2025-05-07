# Importation des modules nécessaires depuis FastAPI et Pydantic
from fastapi import FastAPI, Header, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Création d'une instance de l'application FastAPI
app = FastAPI()

# Configuration du middleware CORS pour autoriser les requêtes depuis le frontend (localhost:5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],  # Origines autorisées
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],  # Méthodes HTTP autorisées
    allow_headers=["X-Auth-Token", "Content-Type"],  # En-têtes autorisés
)

# Définition du token d'authentification à utiliser dans les requêtes
API_TOKEN = "token_secret_123"

# Modèle de données pour représenter un personnage
class Personnage(BaseModel):
    id: int
    nom: str
    profession: str
    age: int
    univers: str
    score: int  # Score du personnage
    niveau: Optional[str] = None  # Niveau (déterminé plus tard)

# Données simulées (comme une base de données)
personnages = [
    Personnage(id=1, nom="Harry Potter", profession="Sorcier", age=17, univers="Harry Potter", score=85),
    Personnage(id=2, nom="Ron Weasley", profession="Sorcier", age=17, univers="Harry Potter", score=75),
    Personnage(id=3, nom="Hermione Granger", profession="Sorcière", age=17, univers="Harry Potter", score=90),
    Personnage(id=4, nom="Albus Dumbledore", profession="Directeur de Poudlard", age=115, univers="Harry Potter", score=55)
]

# Route GET pour récupérer la liste des personnages
@app.get("/personnages", response_model=List[Personnage])
def get_personnages(
    token: str = Header(..., alias="x-auth-token"),  # Récupère le token depuis l'en-tête HTTP
    prenom: Optional[str] = None  # Filtre optionnel sur le prénom
):
    # Vérifie si le token est correct
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )
    
    # Si un prénom est fourni, filtre les personnages dont le nom commence par ce prénom
    if prenom:
        return [p for p in personnages if p.nom.lower().startswith(prenom.lower())]
    
    # Sinon, retourne tous les personnages
    return personnages

# Modèle pour représenter un avis utilisateur (feedback)
class Feedback(BaseModel):
    nom: str
    ville: str
    avis: str

# Route POST pour recevoir un avis utilisateur
@app.post("/scores")
def post_score(feedback: Feedback):
    print("Reçu :", feedback)  # Affiche l'avis reçu dans la console (pour le débogage)
    return {"message": "Succès", "data": feedback}  # Renvoie une confirmation avec les données reçues

# Route POST pour traiter une liste de personnages et leur attribuer un niveau en fonction du score
@app.post("/traitement")
async def traitement(personnages: List[Personnage]):
    # Boucle sur chaque personnage pour lui attribuer un niveau selon son score
    for personnage in personnages:
        if personnage.score >= 80:
            personnage.niveau = "expert"
        elif personnage.score >= 60:
            personnage.niveau = "intermédiaire"
        else:
            personnage.niveau = "débutant"
    
    # Renvoie la liste des personnages mise à jour avec le niveau calculé
    return personnages



#uvicorn main_personnages_api:app --reload
