import requests

def envoyer_vers_traitement():
    # URL de ton API pour récupérer les personnages
    url_personnages = "http://127.0.0.1:8000/personnages"
    
    # Faire une requête GET pour récupérer les personnages depuis l'API
    response = requests.get(url_personnages, headers={"x-auth-token": "token_secret_123"})
    
    if response.status_code == 200:
        personnages = response.json()  # Récupérer la liste des personnages en format JSON
        print("Personnages récupérés:", personnages)
        
        # Envoi des personnages vers l'API /traitement pour ajouter 'niveau' et 'score_doublé'
        url_traitement = "http://127.0.0.1:8000/traitement"
        response_traitement = requests.post(url_traitement, json=personnages)
        
        if response_traitement.status_code == 200:
            # Afficher la réponse enrichie avec niveau et score_doublé
            personnages_enrichis = response_traitement.json()
            print("Réponse du traitement:", personnages_enrichis)
        else:
            print("Erreur dans le traitement:", response_traitement.status_code)
    else:
        print("Erreur lors de la récupération des personnages:", response.status_code)

# Appel de la fonction pour envoyer les personnages vers /traitement
envoyer_vers_traitement()

#uvicorn main_envoyer_personnages_traitement:app --reload