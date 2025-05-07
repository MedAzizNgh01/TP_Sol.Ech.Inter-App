from fastapi import FastAPI  # Import de FastAPI pour créer l'application web
from pydantic import BaseModel  # Pour définir des modèles de données robustes
from enum import Enum  # Pour créer un type énuméré (valeurs fixes)
import json  # Pour lire et écrire des fichiers JSON
import os  # Pour interagir avec le système de fichiers

# Définition d'une énumération pour le niveau du personnage
class Niveau(str, Enum):
    FAIBLE = "Faible"
    MOYEN = "Moyen"
    FORT = "Fort"

# Modèle de données reçu en entrée (depuis le client)
class PersonnageInput(BaseModel):
    nom: str
    score: int

# Modèle de données renvoyé en sortie (inclut le niveau calculé)
class PersonnageOutput(PersonnageInput):
    niveau: Niveau

# Fonction pour déterminer le niveau en fonction du score
def calculer_niveau(score: int) -> Niveau:
    if score < 50:
        return Niveau.FAIBLE
    elif score < 80:
        return Niveau.MOYEN
    else:
        return Niveau.FORT

# Fonction pour archiver les personnages dans un fichier JSON
def archiver_personnage(personnage: PersonnageOutput, fichier="webhook_log.json"):
    data = []
    if os.path.exists(fichier):  # Si le fichier existe déjà
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)  # On lit le contenu existant
        except json.JSONDecodeError:
            pass  # Si le JSON est corrompu, on ignore
    data.append(personnage.dict())  # On ajoute le nouveau personnage
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  # On sauvegarde

# Fonction pour enregistrer une notification dans un fichier texte
def enregistrer_notification(message: str, fichier="notifications.txt"):
    with open(fichier, "a", encoding="utf-8") as f:
        f.write(message + "\n")  # On ajoute la ligne de message

# Création de l'application FastAPI
app = FastAPI()

# Dictionnaire pour activer/désactiver les notifications
notifications_activées = {"active": True}

# Endpoint principal : reçoit un personnage, calcule son niveau et l’archive
@app.post("/webhook/personnage", response_model=PersonnageOutput)
def recevoir_personnage(p: PersonnageInput):
    niveau = calculer_niveau(p.score)
    personnage = PersonnageOutput(**p.dict(), niveau=niveau)  # Fusion des données
    archiver_personnage(personnage)  # Sauvegarde dans webhook_log.json
    print("✅ Personnage ajouté avec succès !")

    if notifications_activées["active"]:
        notifier(personnage)  # Appel de la fonction de notification

    return personnage  # On retourne les données enrichies

# Endpoint appelé pour envoyer une notification (peut aussi être appelée seule)
@app.post("/notifier")
def notifier(personnage: PersonnageOutput):
    message = f"📣 Nouveau personnage : {personnage.nom} - Niveau {personnage.niveau}"
    print(message)
    enregistrer_notification(message)
    return {"message": "Notification envoyée"}

# Endpoint pour activer ou désactiver les notifications
@app.post("/subscribe")
def subscribe(active: bool):
    notifications_activées["active"] = active
    return {"message": f"Notifications {'activées' if active else 'désactivées'}"}


#Pour tester : uvicorn main_webhook_api:app --reload