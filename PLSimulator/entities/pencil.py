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
                RCS(Vector2(-13, -52), flip_x=True),
                RCS(Vector2(14, -52), flip_x=False),
                Leg(Vector2(-9, 46), flip_x=False),
                Leg(Vector2(10, 46), flip_x=True),
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
    def __init__(self, position: Vector2, flip_x: bool):
        asset_size = Vector2(-16, 16) if flip_x else Vector2(16, 16)
        super(RCS, self).__init__(
            'rcs_firing.png',
            asset_size,
            position,
            Vector2(0, 0),
            0,
            1,
            [],
            False,
            False
        )

class Leg(BaseEntity):
    def __init__(self, position: Vector2, flip_x: bool):
        asset_size = Vector2(-8, 48) if flip_x else Vector2(8, 48)
        super(Leg, self).__init__(
            "leg.png",
            asset_size,
            position,
            Vector2(0, 0),
            0,
            3,
            [],
            True,
            True
        )
