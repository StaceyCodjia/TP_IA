import os

# Chemin vers mes données Naruto
path = "corpus/arc_pain"
mon_corpus = {}

print("--- Début de l'ingestion ---")

# On vérifie si le dossier existe pour éviter un crash
if os.path.exists(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
                # On stocke dans un dictionnaire : {Nom du fichier : Texte}
                texte = f.read()
                mon_corpus[filename] = texte
                print(f"Chargé : {filename} ({len(texte)} caractères)")
else:
    print(f"Erreur : Le dossier {path} est introuvable !")

print(f"--- Fin de l'ingestion : {len(mon_corpus)} documents en mémoire ---")

# Exemple : Afficher un petit bout du premier document pour tester
if mon_corpus:
    premier_fichier = list(mon_corpus.keys())[0]
    print(f"\nExtrait de {premier_fichier} :\n{mon_corpus[premier_fichier][:200]}...")