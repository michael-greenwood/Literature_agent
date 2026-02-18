import requests
import json

OLLAMA_URL = "http://132.156.103.65:11434/api/generate"
MODEL = "llama3.1:8b"

# ------------------------
# LLM Wrapper
# ------------------------
def query_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()["response"]

def safe_json_parse(raw):
    start = raw.find("{")
    end = raw.rfind("}") + 1
    return json.loads(raw[start:end])

# ------------------------
# Memory
# ------------------------
class ScientificMemory:
    def __init__(self):
        self.papers = []
        self.concepts = set()

    def add_paper(self, extraction):
        self.papers.append(extraction)

        for m in extraction.get("Materials", []):
            self.concepts.add(m)

        for method in extraction.get("Methods", []):
            self.concepts.add(method)

    def summary(self):
        return {
            "num_papers": len(self.papers),
            "concepts": list(self.concepts)
        }

memory = ScientificMemory()

# ------------------------
# Agent Functions
# ------------------------
EXTRACTION_PROMPT = """
You are an information extraction system.

Extract:
- Research Problem
- Materials (list)
- Methods (list)
- Key Findings (list)
- Limitations (list)

Return JSON only.
"""

def ingest_abstract(abstract: str):
    prompt = EXTRACTION_PROMPT + "\n\nAbstract:\n" + abstract
    raw = query_llm(prompt)
    data = safe_json_parse(raw)
    memory.add_paper(data)
    return data

def answer_question(question: str):
    context = f"""
You are reasoning over structured scientific memory.

Memory:
{json.dumps(memory.summary(), indent=2)}

Answer the question using only this information.
"""
    return query_llm(context + "\n\nQuestion:\n" + question)

# ------------------------
# Standalone Test
# ------------------------
if __name__ == "__main__":
    abstract = """
    This study investigates 3D printed zeolite structures for CO2 capture.
    Humidity was found to reduce adsorption efficiency by 15%.
    """

    print("---- INGESTING ABSTRACT ----")
    extraction = ingest_abstract(abstract)
    print(json.dumps(extraction, indent=2))

    print("\n---- MEMORY SUMMARY ----")
    print(json.dumps(memory.summary(), indent=2))

    print("\n---- ASKING QUESTION ----")
    answer = answer_question("What limits performance?")
    print(answer)
