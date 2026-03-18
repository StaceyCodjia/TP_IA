import os
import re

# --- CONFIGURATION ---
path = "corpus/arc_pain"
taille_chunk = 800
mon_corpus = {}
chunks_naruto = []

# --- FONCTION DE NETTOYAGE ---
def nettoyer_texte(texte):
    # Enlever les codes HTML comme &#44;
    texte = re.sub(r'&#\d+;', '', texte)
    # Enlever les balises bizarre et les sauts de ligne en trop
    texte = re.sub(r'\s+', ' ', texte)
    return texte.strip()

print("--- 1. Ingestion ---")
if os.path.exists(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
                mon_corpus[filename] = f.read()
    print(f"Chargé : {len(mon_corpus)} documents.")
else:
    print("Erreur : Dossier introuvable.")

print("\n--- 2. Chunking & Nettoyage ---")
for nom_fichier, texte in mon_corpus.items():
    # On nettoie le texte AVANT de le découper
    texte_propre = nettoyer_texte(texte)
    
    for i in range(0, len(texte_propre), taille_chunk):
        morceau = texte_propre[i : i + taille_chunk]
        chunks_naruto.append(morceau)

print(f"Total : {len(chunks_naruto)} chunks propres créés.")

# --- VERIFICATION ---
if chunks_naruto:
    print("\nExemple du premier chunk propre :")
    print(chunks_naruto[0][:300] + "...")