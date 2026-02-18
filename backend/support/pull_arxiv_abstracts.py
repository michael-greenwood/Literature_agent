import json
import time
import re
import requests
import xml.etree.ElementTree as ET

ARXIV_API = "http://export.arxiv.org/api/query"

# -----------------------------
# CONFIG
# -----------------------------
TOPICS = {
    "co2_capture": 'all:"CO2 capture" OR all:"carbon capture"',
    "zeolite_adsorption": 'all:"zeolite" AND all:"adsorption"',
    "battery_dendrite": 'all:"lithium dendrite" OR all:"battery dendrite"',
    "digital_twin": 'all:"digital twin"',
    "additive_manufacturing": 'all:"additive manufacturing" AND all:"materials"',
}

RESULTS_PER_TOPIC = 10
OUTPUT_FILE = "abstracts_real.json"
SLEEP_S = 1.0  # be polite


# -----------------------------
# ARXIV API
# -----------------------------
def query_arxiv(search_query: str, max_results: int) -> str:
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    r = requests.get(ARXIV_API, params=params, timeout=30)
    r.raise_for_status()
    return r.text


def _clean_ws(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def parse_arxiv_atom(xml_data: str):
    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

    parsed = []

    for entry in root.findall("atom:entry", ns):
        title = _clean_ws(entry.findtext("atom:title", default="", namespaces=ns))
        abstract = _clean_ws(entry.findtext("atom:summary", default="", namespaces=ns))

        # arXiv id from <id> URL
        arxiv_url = entry.findtext("atom:id", default="", namespaces=ns)
        arxiv_id = arxiv_url.split("/")[-1] if arxiv_url else None

        published = entry.findtext("atom:published", default="", namespaces=ns)
        year = int(published[:4]) if published and published[:4].isdigit() else None

        # authors
        authors = []
        for a in entry.findall("atom:author", ns):
            name = _clean_ws(a.findtext("atom:name", default="", namespaces=ns))
            if name:
                authors.append(name)

        # DOI: best effort (arXiv sometimes provides <arxiv:doi>)
        doi = entry.findtext("arxiv:doi", default="", namespaces=ns)
        doi = _clean_ws(doi) or None

        parsed.append({
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "year": year,
            "source": "arXiv",
            "doi": doi,
            "arxiv_id": arxiv_id,
        })

    return parsed


# -----------------------------
# MAIN
# -----------------------------
def main():
    print("Pulling abstracts from arXiv...\n")

    # Deduplicate by arxiv_id (or title fallback)
    dedup = {}

    for topic_name, query in TOPICS.items():
        print(f"Querying: {topic_name} -> {query}")

        try:
            xml_data = query_arxiv(query, RESULTS_PER_TOPIC)
            entries = parse_arxiv_atom(xml_data)

            for e in entries:
                key = e["arxiv_id"] or e["title"].lower()
                dedup[key] = e

            time.sleep(SLEEP_S)

        except Exception as ex:
            print(f"  ERROR: {ex}")

    # Convert to your schema + stable paper ids
    final = []
    for i, e in enumerate(dedup.values(), start=1):
        final.append({
            "id": f"paper_{i:03d}",
            "title": e["title"],
            "abstract": e["abstract"],
            "authors": e["authors"],
            "year": e["year"],
            "source": e["source"],
            "doi": e["doi"],
            "arxiv_id": e["arxiv_id"],
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)

    print("\nDone.")
    print(f"Saved {len(final)} abstracts to {OUTPUT_FILE}")
    print("Note: DOI availability on arXiv is hit-or-miss; many entries will have null DOI.")


if __name__ == "__main__":
    main()
