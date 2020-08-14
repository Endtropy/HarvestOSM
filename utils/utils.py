import random, string
import geojson
from pathlib import Path
from itertools import product


def random_name():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(5))


def get_area_tags():
    base_path = Path(__file__).parent
    file_path = (base_path / "../utils/area_tags.json").resolve()
    with open(file_path, 'r') as f:
        return geojson.load(f)


def get_name():
    for i in range(1, 3+1):
        for item in product(string.ascii_uppercase, repeat=i):
            yield "".join(item)










