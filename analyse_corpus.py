import os
import re

# --- CONFIGURATION ---
path = "corpus/arc_pain"
taille_chunk = 800
mon_corpus = {}
chunks_propres = []

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
        chunks_propres.append(morceau)

print(f"Total : {len(chunks_propres)} chunks propres créés.")

# --- VERIFICATION ---
if chunks_propres:
    print("\nExemple du premier chunk propre :")
    print(chunks_propres[0][:300] + "...")

from sentence_transformers import SentenceTransformer

print("\n--- 3. Vectorisation (Embeddings) ---")

# Chargement du modèle mentionné dans ton TP
model = SentenceTransformer('all-MiniLM-L6-v2')

# On transforme nos chunks propres en vecteurs (embeddings)
# Cette étape peut prendre quelques secondes selon ton ordi
embeddings = model.encode(chunks_propres)

print(f"Vectorisation terminée !")
print(f"Nombre de vecteurs créés : {len(embeddings)}")
print(f"Dimension de chaque vecteur : {len(embeddings[0])}") # Doit être 384