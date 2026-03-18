import os
import re
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from openai import OpenAI

# --- CONFIGURATION ---
path = "corpus/arc_pain"
taille_chunk = 800
OPENROUTER_API_KEY = "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"

# --- FONCTION DE NETTOYAGE ---
def nettoyer_texte(texte):
    texte = re.sub(r'&#\d+;', '', texte)
    texte = re.sub(r'\s+', ' ', texte)
    return texte.strip()

# --- 1. INGESTION ---
print("--- 1. Ingestion ---")
mon_corpus = {}
if os.path.exists(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
                mon_corpus[filename] = f.read()
    print(f"Chargé : {len(mon_corpus)} documents.")
else:
    print("Erreur : Dossier introuvable.")
    exit()

# --- 2. CHUNKING & NETTOYAGE ---
print("\n--- 2. Chunking & Nettoyage ---")
chunks_propres = []
for nom_fichier, texte in mon_corpus.items():
    texte_propre = nettoyer_texte(texte)
    for i in range(0, len(texte_propre), taille_chunk):
        chunks_propres.append(texte_propre[i : i + taille_chunk])
print(f"Total : {len(chunks_propres)} chunks créés.")

# --- 3. VECTORISATION & BASE FAISS ---
print("\n--- 3. Préparation de la base de connaissances (IA) ---")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
documents_langchain = [Document(page_content=t) for t in chunks_propres]
vectorstore = FAISS.from_documents(documents_langchain, embedding_model)
print("Base de données prête !")

# --- 4. CONFIGURATION DU CLIENT IA ---
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

# --- BOUCLE DE TEST INTERACTIVE ---
print("\n" + "="*50)
print("BIENVENUE CHEZ L'EXPERT NARUTO (ARC PAIN)")
print("Pose tes questions ! Tape 'quitter' pour arrêter.")
print("="*50)

while True:
    query = input("\nTa question : ")
    
    if query.lower() in ['quitter', 'exit', 'quit']:
        print("Fermeture du programme...")
        break

    # 1. Retrieval 
    resultats = vectorstore.similarity_search(query, k=5)
    contexte_extraits = "\n\n".join([doc.page_content for doc in resultats])

    # 2. Generation (Appel au LLM)
    try:
        response = client.chat.completions.create(
          model="google/gemini-2.0-flash-001",
          messages=[
            {"role": "system", "content": "Tu es un expert de l'arc Pain dans Naruto. Réponds en markdown de façon concise en te basant sur les extraits fournis.Si l'information est partiellement présente, utilise tes connaissances pour lier les points logiquement,tout en restant fidèle à l'esprit des documents."},
            {"role": "user", "content": f"Extraits du wiki :\n{contexte_extraits}\n\nQuestion : {query}"}
          ]
        )
        
        print("\n--- RÉPONSE DE L'EXPERT ---")
        print(response.choices[0].message.content)
        print("-" * 30)
        
    except Exception as e:
        print(f"Erreur lors de l'appel à l'IA : {e}")