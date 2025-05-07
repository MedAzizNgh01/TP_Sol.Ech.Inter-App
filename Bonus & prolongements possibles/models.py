
from pydantic import BaseModel
from enum import Enum
from typing import Optional

class Niveau(str, Enum):
    FAIBLE = "Faible"
    MOYEN = "Moyen"
    FORT = "Fort"

class PersonnageBase(BaseModel):
    nom: str
    score: int

class Personnage(PersonnageBase):
    id: int
    niveau: Niveau
    badge: Optional[str] = None  # Nouveau champ badge

def calculer_niveau(score: int) -> Niveau:
    if score < 50:
        return Niveau.FAIBLE
    elif score < 80:
        return Niveau.MOYEN
    else:
        return Niveau.FORT
