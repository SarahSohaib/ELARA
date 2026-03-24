from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# sample dataset
DATA = [
    "Interstellar - Sci-fi movie about space",
    "Inception - Mind-bending thriller",
    "The Matrix - Virtual reality sci-fi",
    "The Notebook - Romantic drama",
]

# create embeddings
embeddings = model.encode(DATA)

# create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


def process_query(query):
    query_embedding = model.encode([query])

    D, I = index.search(np.array(query_embedding), k=2)

    results = [DATA[i] for i in I[0]]

    # format response nicely
    response = "Top recommendations:\n"
    for i, item in enumerate(results, 1):
        response += f"{i}. {item}\n"

    return response
