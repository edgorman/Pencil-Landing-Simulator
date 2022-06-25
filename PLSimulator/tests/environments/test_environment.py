import pytest

from PLSimulator.entities.pencil import Pencil
from PLSimulator.entities.static import Ground
from PLSimulator.entities.static import LandingPad
from PLSimulator.environments.environment import BaseEnvironment


@pytest.mark.parametrize("config", [
    (
        {
            'test': {
                'name': 'test-v0',
                'gravity': 1.0,
                'density': 2.0,
                'max_fuel': 3.0,
                'bg_colour': (4, 5, 6),
                'width': 7,
                'height': 8
            }
        }
    )
])
def test_init(config):
    x = BaseEnvironment(config)

    assert all([e in x.entities for e in ['pencil', 'ground', 'landingPad']])
    assert isinstance(x.entities['pencil'], Pencil)
    assert isinstance(x.entities['ground'], Ground)
    assert isinstance(x.entities['landingPad'], LandingPad)
