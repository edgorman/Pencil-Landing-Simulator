from pygame import Vector2

from PLSimulator.entities.entity import BaseEntity


class Pencil(BaseEntity):
    '''
        Pencil

        This is the pencil entity class
    '''

    def __init__(self):
        super().__init__(
            'pencil.png', 
            Vector2(16, 128),
            Vector2(0, 0),
            Vector2(0, 0),
            0,
            20,  # TODO: change start mass on reset method
            [
                Engine(),
                RCS(Vector2(14, 53), 180),
                RCS(Vector2(14, -53), 0),
                Leg('leg_left.png', Vector2(-9, 46)),
                Leg('leg_right.png', Vector2(10, 46)),
            ],
            True,
            True
        )


class Engine(BaseEntity):
    def __init__(self):
        super(Engine, self).__init__(
            'engine_firing.png',
            Vector2(16, 80),
            Vector2(0, 84),
            Vector2(0, 0),
            0,
            5,
            [],
            False,
            False
        )

class RCS(BaseEntity):
    def __init__(self, position: Vector2, angle: float):
        super(RCS, self).__init__(
            'rcs_firing.png',
            Vector2(16, 16),
            position,
            Vector2(0, 0),
            angle,
            1,
            [],
            False,
            False
        )

class Leg(BaseEntity):
    def __init__(self, image: str, position: Vector2):
        super(Leg, self).__init__(
            image,
            Vector2(8, 48),
            position,
            Vector2(0, 0),
            0,
            3,
            [],
            True,
            True
        )
