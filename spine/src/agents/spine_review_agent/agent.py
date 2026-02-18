import json
from llm import query_llm
from memory import ScientificMemory

memory = ScientificMemory()

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

    data = json.loads(raw)
    memory.add_paper(data)

    return data

def answer_question(question: str):
    context = f"""
You are reasoning over structured scientific memory.

Memory:
{memory.summary()}

Answer the question using only this information.
"""
    return query_llm(context + "\n\nQuestion:\n" + question)
