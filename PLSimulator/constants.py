import os


PARENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DATA_DIRECTORY = os.path.join(PARENT_DIRECTORY, "data")
ASSET_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, "assets")
MODEL_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, "models")

ENV_CONFIG = {
    'earth': {
        'gravity': 9.8,
        'density': 1.0,
        'max_fuel': 100,
        'bg_color': (137, 207, 240)
    },
    'mars': {
        'gravity': 4.9,
        'density': 0.1,
        'max_fuel': 50,
        'bg_color': (110, 38, 14)
    },
    'moon': {
        'gravity': 1.6,
        'density': 0.0,
        'max_fuel': 25,
        'bg_color': (169, 169, 169)
    }
}