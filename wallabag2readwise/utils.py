import json


def check_valid_json(data: str) -> bool:
    try:
        json.loads(data)
    except ValueError:
        return False
    return True
