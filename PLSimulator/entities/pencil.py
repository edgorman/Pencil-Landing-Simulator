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
            Vector2(312, 64),
            Vector2(0, 0),
            0,
            20,
            [
                Engine(),
                RCS(flip_x=False),
                RCS(flip_x=True),
                Leg(flip_x=False),
                Leg(flip_x=True),
            ],
            True,
            True
        )

        self.dry_mass = self.mass
        self.start_fuel, self.fuel_mass = 20, 20
        self.mass = self.dry_mass + self.fuel_mass
    
    def fire_engine(self):
        if self.fuel_mass > 0:
            self.fuel_mass -= 0.1
            self.mass = self.dry_mass + self.fuel_mass
            return True
        return False
    
    def update_entities(self, action):
        for i in range(len(action)):
            self.entities[i].isRenderable = action[i] != 0


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
    def __init__(self, flip_x: bool):
        asset_size = Vector2(-16, 16) if flip_x else Vector2(16, 16)
        position = Vector2(-13, -52) if flip_x else Vector2(13, -52)
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
    def __init__(self, flip_x: bool):
        asset_size = Vector2(-8, 48) if flip_x else Vector2(8, 48)  # TODO: Fix image, not correct asset_size
        position = Vector2(10, 46) if flip_x else Vector2(-9, 46)
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
