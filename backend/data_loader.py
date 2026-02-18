import json
import os
import random


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_abstracts(randomize: bool = True):
    path = os.path.join(DATA_DIR, "abstracts.json")
    with open(path, "r", encoding="utf-8") as f:
        abstracts = json.load(f)

    if randomize:
        random.shuffle(abstracts)

    return abstracts


def load_projects():
    path = os.path.join(DATA_DIR, "projects.json")
    with open(path, "r", encoding="utf-8") as f:
        project_list = json.load(f)

    # Convert list → dict keyed by name
    projects = {p["name"]: p for p in project_list}
    return projects


def load_lab_objectives():
    path = os.path.join(DATA_DIR, "lab_objectives.json")
    with open(path, "r", encoding="utf-8") as f:
        objectives = json.load(f)

    objectives_dict = {o["name"]: o for o in objectives}
    return objectives_dict
