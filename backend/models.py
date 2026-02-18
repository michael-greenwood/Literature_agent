from datetime import datetime


def initialize_memory(projects_dict):
    memory = {
        "engine": {
            "status": "idle",
            "total_processed": 0,
            "total_routed": 0,
            "total_discarded": 0,
            "last_update_time": None,
        },
        "papers": {},
        "projects": {},
        "discarded": [],
        "current_processing": None,
        "event_log": []
    }

    # Initialize project buckets
    for project_name, project_data in projects_dict.items():
        memory["projects"][project_name] = {
            "description": project_data.get("description", ""),
            "keywords": project_data.get("keywords", []),
            "techniques": project_data.get("techniques", []),

            "paper_ids": [],
            "total_papers": 0,
            "avg_relevance": 0.0,
            "high_relevance_count": 0
        }


    return memory


def update_engine_timestamp(memory):
    memory["engine"]["last_update_time"] = datetime.utcnow().isoformat()
