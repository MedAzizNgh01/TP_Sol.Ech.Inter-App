import json         # Pour lire et manipuler les fichiers JSON
import time         # Pour faire une pause entre les envois
import requests     # Pour faire des requêtes HTTP vers une API
from tqdm import tqdm  # Pour afficher une barre de progression dans le terminal

# 1. Lecture des données JSON depuis un fichier local
with open("fichier.json", "r") as f:
    data = json.load(f)  # On charge les données dans la variable `data`

# Préparation du fichier de logs pour enregistrer les résultats des envois
log_file = open("log_envois.txt", "w", encoding="utf-8")

# 2. Transformation des données pour les adapter au format attendu par l'API
donnees_transformees = []
for item in data:
    # On crée un nouveau dictionnaire avec les champs nécessaires
    nouveau = {
        "nom": item.get("name", "Inconnu"),      # On renomme "name" en "nom", valeur par défaut : "Inconnu"
        "ville": item.get("city", "Sans Ville"), # On renomme "city" en "ville", valeur par défaut : "Sans Ville"
    }

    # On ajoute un champ "avis" basé sur le contenu du nom
    if "Chad" in nouveau["nom"]:
        nouveau["avis"] = "positif"     # Si le nom contient "Chad"
    elif "Center" in nouveau["nom"]:
        nouveau["avis"] = "neutre"      # Si le nom contient "Center"
    else:
        nouveau["avis"] = "négatif"     # Sinon

    # On ajoute cet élément transformé à la liste
    donnees_transformees.append(nouveau)

# 3. Envoi des données à une API (POST vers l'endpoint /scores)
url = "http://127.0.0.1:8000/scores"  # L’URL de l’API FastAPI locale
headers = {
    "Content-Type": "application/json",  # Indique qu’on envoie des données JSON
    # "Authorization": "Bearer VOTRE_TOKEN",  # Ligne à activer si l’API demande un token
}

# Boucle sur les données transformées pour les envoyer une par une
for item in tqdm(donnees_transformees, desc="Envoi des données à l'API..."):
    try:
        response = requests.post(url, headers=headers, json=item)  # Envoi HTTP POST
        if response.status_code == 200:
            log_file.write(f"✅ Succès : {item['nom']} à {item['ville']}\n")  # Succès : log OK
        else:
            log_file.write(f"❌ Échec ({response.status_code}) : {item['nom']}\n")  # Erreur HTTP : log KO
    except Exception as e:
        log_file.write(f"⚠️ Erreur exception : {item['nom']} - {str(e)}\n")  # Exception réseau ou autre

    time.sleep(0.5)  # Pause de 0,5 seconde pour ne pas surcharger le serveur

# Fermeture du fichier de log
log_file.close()

# Message final une fois que tous les envois sont terminés
print("Tous les envois ont été traités. Voir log_envois.txt pour les détails.")
