from lib2to3.pytree import Base
import os
import pygame
from pygame import Vector2

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
        position: Vector2 = Vector2(0, 0),
        velocity: Vector2 = Vector2(0, 0),
        angle: float = 0,
        mass: float = 1,
        entities: list = [],
        isRenderable: bool = True) -> None:
        '''
            Initialise the entity

            Parameters:
                asset_name: Name of image to use in GUI
                asset_size: Size of the image to scale to
                position: Current position of entity
                velocity: Current velocity of entity
                angle: Current angle of the entity
                mass: Mass of entity (may change)
                entities: List of sub entities to render
                isRenderable: Whether the entity is renderable

            Returns:
                None
        '''
        self._asset_name = asset_name
        self._asset_size = asset_size
        self.position = position
        self.velocity = velocity
        self.angle = angle
        self.mass = mass
        self.entities = entities
        self.isRenderable = isRenderable

        image_path = os.path.join(ASSET_DATA_DIRECTORY, asset_name)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, asset_size)

    def update_position(self, force: Vector2, heading: float = None) -> None:
        '''
            Update the positional information of the entity

            Parameters:
                force: Force to apply to entity
                heading: New heading the entity faces
            
            Returns:
                None
        '''
        # Calculate acceleration: A = F/M
        acceleration = force / self.mass

        # Update velocity
        self.velocity += acceleration

        # Update position
        self.position += self.velocity

        # Update heading
        if heading is not None:
            self.angle = heading

    def render(self, pivot: Vector2 = Vector2(0, 0), offset: Vector2 = Vector2(0, 0), angle: float = 0) -> list:
        '''
            Render the entity and any sub-entities to the window

            Parameters:
                pivot: Position around which to rate
                offset: Offset from the pivot to place image
                angle: Heading of the image relative to parent

            Returns:
                images: List of rotated images to render
        '''
        images = []

        # Render entity
        rotated_image = pygame.transform.rotozoom(self.image, self.angle + angle, 1)
        rotated_offset = offset.rotate(-(self.angle + angle))
        rotated_rect = rotated_image.get_rect(center = pivot + rotated_offset)
        images.append((rotated_image, rotated_rect))

        # Render sub-entities that are renderable
        for entity in self.entities:
            if entity.isRenderable:
                images.extend(entity.render(pivot, entity.position, self.angle + angle))

        return images

    def collides_with(self, other: object):
        '''
            Check whether other BaseEntity object collides with this object

            Parameters:
                other: Other base entity to consider
            
            Returns:
                collision: Whether a collision has occurred
        '''

        return False
