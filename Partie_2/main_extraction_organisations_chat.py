import requests  # Importation de la bibliothèque pour effectuer des requêtes HTTP
import json  # Importation de la bibliothèque pour manipuler des données JSON
import time  # Importation de la bibliothèque pour effectuer des pauses dans l'exécution

def main():
    # 1. Choisir une API paginée (ici, l'API de ProPublica qui liste des organisations)
    url_base = "https://projects.propublica.org/nonprofits/api/v2/search.json"
    query = "chat"  # Recherche d'organisations ayant le mot "chat" dans leur nom ou description
    
    # 3. Stocker tous les résultats dans une liste Python
    toutes_donnees = []  # Liste pour stocker toutes les données récupérées
    current_page = 0  # Initialisation du compteur de pages
    max_pages = 100  # Limite pour éviter une boucle infinie en cas d'erreur
    
    print(f"Extraction des données pour la requête '{query}'...")
    
    # 2. Écrire une boucle while pour appeler chaque page jusqu'à ce qu'il n'y ait plus de résultats
    while current_page < max_pages:
        # Création de l'URL avec les paramètres nécessaires (mot-clé et numéro de page)
        url = f"{url_base}?q={query}&page={current_page}"
        print(f"Récupération de la page {current_page}...")
        
        # Envoi de la requête GET à l'API
        response = requests.get(url)
        
        # Vérification du code de statut de la réponse pour savoir si la requête a réussi
        if response.status_code != 200:
            print(f"Erreur lors de la requête: Code {response.status_code}")
            break  # Arrêt de la boucle si la requête échoue
            
        data = response.json()  # Conversion de la réponse JSON en dictionnaire Python
        
        # Vérification si des organisations sont présentes dans la réponse
        if "organizations" in data:
            organizations = data["organizations"]
            if not organizations:  # Si la liste est vide, cela signifie que nous avons atteint la fin des pages
                print("Plus de résultats disponibles.")
                break  # Sortie de la boucle si aucune organisation n'est trouvée
                
            # Ajout des résultats récupérés à la liste des toutes_donnees
            toutes_donnees.extend(organizations)
            print(f"Page {current_page}: {len(organizations)} résultats récupérés")
            
            # Passer à la page suivante
            current_page += 1
            
            # Pause de 0.5 seconde pour éviter de surcharger l'API et respecter les limites de requêtes
            time.sleep(0.5)
        else:
            print("Format de réponse inattendu.")
            break  # Sortie de la boucle si la réponse ne correspond pas au format attendu
    
    print(f"Extraction terminée. {len(toutes_donnees)} résultats récupérés au total.")
    
    # 4. Filtrage des données pour ne conserver que celles qui ont une ville
    print("Filtrage des données...")
    donnees_filtrees = [org for org in toutes_donnees if org.get("city")]
    print(f"Filtrage terminé: {len(donnees_filtrees)} résultats sur {len(toutes_donnees)} conservés.")
    
    # 5. Enregistrement des données filtrées dans un fichier JSON
    nom_fichier = "organisations_chat.json"  # Nom du fichier de sortie
    print(f"Enregistrement des données dans {nom_fichier}...")
    
    # Ouverture du fichier en mode écriture et sauvegarde des données au format JSON
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(donnees_filtrees, f, indent=2, ensure_ascii=False)
    
    print(f"Données enregistrées avec succès dans {nom_fichier}")

# Appel de la fonction main si ce script est exécuté directement
if __name__ == "__main__":
    main()


#pour tester : uvicorn main_extraction_organisations_chat:app --reload