
import streamlit as st
import requests

url = "http://127.0.0.1:8000/personnages"

response = requests.get(url)
personnages = response.json()

st.title("Personnages")
for personnage in personnages:
    st.subheader(f"Nom: {personnage['nom']}")
    st.write(f"Score: {personnage['score']} | Niveau: {personnage['niveau']}")
