import os


PARENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DATA_DIRECTORY = os.path.join(PARENT_DIRECTORY, "data")
ASSET_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, "assets")
MODEL_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, "models")

ENV_CONFIG = {
    'earth': {
        'name': 'earth-v0',
        'agent': {
            'min_fuel': 20,
            'max_fuel': 20,
            'min_pos': (0.5, 0.1),
            'max_pos': (0.5, 0.1),
            'min_vel': (0, 0),
            'max_vel': (0, 0),
            'min_ang': 0,
            'max_ang': 0
        },
        'physics': {
            'gravity': 9.8,
            'density': 1.0,
            'entities': [],
            'land_ang': 5,
            'land_vel': 2
        },
        'window': {
            'width': 640,
            'height': 900,
            'colour': (137, 207, 240)
        }
    },
    'moon': {
        'name': 'moon-v0',
        'agent': {
            'min_fuel': 20,
            'max_fuel': 20,
            'min_pos': (0.5, 0.1),
            'max_pos': (0.5, 0.1),
            'min_vel': (0, 0),
            'max_vel': (0, 0),
            'min_ang': 0,
            'max_ang': 0
        },
        'physics': {
            'gravity': 1.6,
            'density': 0.0,
            'entities': [],
            'land_ang': 5,
            'land_vel': 2
        },
        'window': {
            'width': 640,
            'height': 900,
            'colour': (169, 169, 169)
        }
    },
    'mars': {
        'name': 'mars-v0',
        'agent': {
            'min_fuel': 20,
            'max_fuel': 20,
            'min_pos': (0.5, 0.1),
            'max_pos': (0.5, 0.1),
            'min_vel': (0, 0),
            'max_vel': (0, 0),
            'min_ang': 0,
            'max_ang': 0
        },
        'physics': {
            'gravity': 4.9,
            'density': 0.2,
            'entities': [],
            'land_ang': 5,
            'land_vel': 2
        },
        'window': {
            'width': 640,
            'height': 900,
            'colour': (110, 38, 14),
        }
    }
}
