import string
import harvestosm
import json
from pathlib import Path
from itertools import product

BASE_PATH = Path(harvestosm.__file__).parent


def open_json(json_rel_path):
    """return json object, json_rel_path is path relative to module folder"""
    file_path = (BASE_PATH / json_rel_path).resolve()
    with open(file_path, 'r') as f:
        return json.load(f)


def save2json(json_rel_path, **kwargs):
    config = open_json(json_rel_path)
    config.update(kwargs)
    with open(json_rel_path, 'w') as f:
        json.dump(config, f, indent=2)


def get_name():
    """Generator of string alphabet index"""
    for i in range(1, 3+1):
        for item in product(string.ascii_uppercase, repeat=i):
            yield "".join(item)



