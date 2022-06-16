from pygame import Vector2

from PLSimulator.entities.entity import BaseEntity



class Ground(BaseEntity):
    '''
        Ground

        This is the ground environment entity class
    '''

    def __init__(self):
        super().__init__(
            'ground.png',
            Vector2(640, 16),
            Vector2(320, 892),
            Vector2(0, 0),
            0,
            100,
            [],
            True
        )


class LandingPad(BaseEntity):
    '''
        LandingPad
    
        This is the landing pad entity class
    '''

    def __init__(self):
        super().__init__(
            'landing_zone.png',
            Vector2(256, 16),
            Vector2(320, 876),  # TODO: change position on reset method
            Vector2(0, 0),
            0,
            100,
            [],
            True
        )
