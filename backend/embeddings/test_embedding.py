from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model (small + fast)
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# --- Sample abstracts ---
papers = [
    {
        "title": "CO2 Zeolite Monoliths",
        "abstract": "We investigate CO2 capture using 3D printed zeolite monolith structures with enhanced adsorption kinetics."
    },
    {
        "title": "Battery Recycling Process",
        "abstract": "Lithium-ion battery recycling through hydrometallurgical separation of critical metals."
    },
    {
        "title": "MOF Sorbent Optimization",
        "abstract": "Metal-organic frameworks are optimized for direct air capture applications under cyclic thermal swing conditions."
    }
]

# --- Embed abstracts ---
for paper in papers:
    paper["embedding"] = model.encode(paper["abstract"])

# --- Project description query ---
project_description = "Development of architected sorbent structures for CO2 direct air capture"

query_embedding = model.encode(project_description)

# --- Cosine similarity function ---
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# --- Rank papers ---
results = []

for paper in papers:
    score = cosine_similarity(query_embedding, paper["embedding"])
    results.append((paper["title"], score))

# Sort by similarity
results.sort(key=lambda x: x[1], reverse=True)

print("\nTop Matches:\n")
for title, score in results:
    print(f"{title}  |  similarity = {score:.4f}")
