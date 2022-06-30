import pytest

from PLSimulator.entities.pencil import Pencil
from PLSimulator.entities.static import Ground
from PLSimulator.entities.static import LandingPad
from PLSimulator.environments.environment import Environment


@pytest.mark.parametrize("config", [
    (
        {
            'name': 'test-v0',
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
        }
    )
])
def test_init(config):
    x = Environment(config)

    assert isinstance(x.pencil, Pencil)
    assert isinstance(x.ground, Ground)
    assert isinstance(x.pad, LandingPad)
