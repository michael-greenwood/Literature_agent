import json

from old_code.data_loader import load_abstracts, load_projects, load_lab_objectives
from prompt_loader import load_prompt
from llm_client import query_llm
from llm_parsing import safe_json_parse


def run_single_test(paper_index=1):

    abstracts = load_abstracts(randomize=False)
    projects = load_projects()
    lab_objectives = load_lab_objectives()

    paper = abstracts[paper_index]

    print("\n==============================")
    print("PAPER UNDER TEST")
    print("==============================")
    print("Title:", paper["title"])
    print("DOI:", paper.get("doi"))
    print("\nAbstract:\n", paper["abstract"])
    print("==============================\n")

    # -------------------------
    # EXTRACTION
    # -------------------------

    extraction_template = load_prompt("extraction.txt")
    extraction_prompt = extraction_template.format(
        title=paper["title"],
        abstract=paper["abstract"]
    )

    print("\n=== EXTRACTION PROMPT ===\n")
    print(extraction_prompt)

    raw_extraction = query_llm(extraction_prompt)

    print("\n--- RAW EXTRACTION RESPONSE ---\n")
    print(raw_extraction)

    try:
        extraction = safe_json_parse(raw_extraction)
        print("\n--- PARSED EXTRACTION ---\n")
        print(json.dumps(extraction, indent=2))
    except Exception as e:
        print("Extraction parsing failed:", e)
        return

    # -------------------------
    # PROJECT SCORING LOOP
    # -------------------------

    for project_name, project in projects.items():

        print("\n==============================")
        print(f"PROJECT: {project_name}")
        print("==============================\n")

        scoring_template = load_prompt("project_scoring.txt")
        scoring_prompt = scoring_template.format(
            project_name=project_name,
            project_description=project.get("description", ""),
            project_keywords=project.get("keywords", []),
            project_techniques=project.get("techniques", []),
            title=paper["title"],
            abstract=paper["abstract"],
            extraction=json.dumps(extraction, indent=2)
        )

        print("\n--- SCORING PROMPT ---\n")
        print(scoring_prompt)

        raw_score = query_llm(scoring_prompt)

        print("\n--- RAW SCORING RESPONSE ---\n")
        print(raw_score)

        try:
            parsed_score = safe_json_parse(raw_score)
            print("\n--- PARSED SCORE ---\n")
            print(json.dumps(parsed_score, indent=2))
        except Exception as e:
            print("Scoring parsing failed:", e)

    print("\n==============================")
    print("END TEST")
    print("==============================\n")


if __name__ == "__main__":
    run_single_test(paper_index=0)
