
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from models import Personnage, PersonnageBase, calculer_niveau
from db import get_db_connection

app = FastAPI()

@app.post("/personnages", response_model=Personnage)
def create_personnage(personnage: PersonnageBase):
    niveau = calculer_niveau(personnage.score)
    conn = get_db_connection()
    conn.execute('''
    INSERT INTO personnages (nom, score, niveau) 
    VALUES (?, ?, ?)
    ''', (personnage.nom, personnage.score, niveau))
    conn.commit()
    conn.close()
    return {**personnage.dict(), "niveau": niveau}

@app.get("/personnages/{id}", response_model=Personnage)
def get_personnage(id: int):
    conn = get_db_connection()
    personnage = conn.execute('SELECT * FROM personnages WHERE id = ?', (id,)).fetchone()
    conn.close()
    if personnage is None:
        raise HTTPException(status_code=404, detail="Personnage non trouvé")
    return dict(personnage)

@app.get("/personnages")
def get_personnages(skip: int = 0, limit: int = 10, tri: Optional[str] = "score"):
    conn = get_db_connection()
    query = f"SELECT * FROM personnages ORDER BY {tri} LIMIT ? OFFSET ?"
    personnages = conn.execute(query, (limit, skip)).fetchall()
    conn.close()
    return [dict(p) for p in personnages]
