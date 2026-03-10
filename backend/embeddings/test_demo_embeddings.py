import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# -----------------------
# Load embedding model
# -----------------------
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# -----------------------
# Load data
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent
data_dir = BASE_DIR / "data"

with open(data_dir / "abstracts.json", "r") as f:
    abstracts = json.load(f)

with open(data_dir / "projects.json", "r") as f:
    projects = json.load(f)

# -----------------------
# Embed abstracts
# -----------------------
print("Embedding abstracts...")
for paper in abstracts:
    paper["embedding"] = model.encode(paper["abstract"])

print(f"Embedded {len(abstracts)} papers.\n")

# -----------------------
# Cosine similarity
# -----------------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# -----------------------
# Evaluate each project
# -----------------------
for project in projects:

    print("=" * 70)
    print(f"PROJECT: {project['name']}")
    print("=" * 70)

    query_text = project["description"]
    query_embedding = model.encode(query_text)

    scores = []

    for paper in abstracts:
        score = cosine_similarity(query_embedding, paper["embedding"])
        scores.append(score)
        paper["similarity"] = score

    scores = np.array(scores)

    mean = scores.mean()
    std = scores.std()

    threshold = mean + 1.0 * std   # ← Tune multiplier here

    print(f"Mean similarity: {mean:.4f}")
    print(f"Std deviation : {std:.4f}")
    print(f"Trigger thresh : {threshold:.4f}\n")

    # Rank papers
    ranked = sorted(abstracts, key=lambda x: x["similarity"], reverse=True)

    print("Top Matches:")
    for paper in ranked[:5]:
        flag = " <-- FLAG" if paper["similarity"] > threshold else ""
        print(f"{paper['title'][:60]:60} | {paper['similarity']:.4f}{flag}")

    print("\n")
