import json
import re

def safe_json_parse(raw):
    if not raw or not isinstance(raw, str):
        return {}

    try:
        return json.loads(raw)
    except Exception:
        pass

    # Try to extract first JSON object
    try:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            candidate = match.group(0)
            return json.loads(candidate)
    except Exception:
        pass

    # If everything fails
    return {}
