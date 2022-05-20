import os
import pygame

from PLSimulator.constants import ASSET_DATA_DIRECTORY


class BaseEntity:
    '''
        BaseEntity

        This is the entity class from which all other entities will inherit.
    '''

    def __init__(
        self,
        asset_name: str,
        asset_size: tuple,
        position: tuple = (0, 0),
        velocity: tuple = (0, 0),
        angle: float = 0,
        ang_velocity: float = 0,
        mass: float = 1,
        isMovable: bool = True,
        isRenderable: bool = True) -> None:
        '''
            Initialise the entity

            Parameters:
                asset_name: Name of image to use in GUI
                asset_size: Size of the image to scale to
                position: Current position of entity
                velocity: Current velocity of entity
                angle: Current angle of the entity
                ang_velocity: Current angular velocity of entity
                mass: Mass of entity (may change)
                isMovable: Whether the entity is movable
                isRenderable: Whether the entity is renderable

            Returns:
                None
        '''
        self._asset_name = asset_name
        self.position = position
        self.velocity = velocity
        self.angle = angle
        self.ang_velocity = ang_velocity
        self.mass = mass
        self._isMovable = isMovable
        self._isRenderable = isRenderable

        image_path = os.path.join(ASSET_DATA_DIRECTORY, asset_name)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, asset_size)
