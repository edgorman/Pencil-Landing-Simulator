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

    def update_position(self, force: float, heading: float = None) -> None:
        '''
            Update the positional information of the entity

            Parameters:
                force: Force to apply to entity
                heading: New heading the entity faces
            
            Returns:
                None
        '''
        # Calculate acceleration: A = F/M
        acceleration = (
            force[0] / self.mass,
            force[1] / self.mass,
        )

        # Update velocity
        self.velocity = (
            self.velocity[0] + acceleration[0],
            self.velocity[1] + acceleration[1],
        )

        # Update position
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )

        # Update heading
        if heading is not None:
            self.angle = heading

    def render(self, pivot: tuple = (0, 0), offset: tuple = (0, 0), angle: float = 0) -> list:
        '''
            Render the entity and any sub-entities to the window

            Parameters:
                None

            Returns:
                images: List of rotated images to render
        '''
        images = []

        # Render entity
        rotated_image = pygame.transform.rotozoom(self.image, self.angle + angle, 1)
        rotated_offset = pygame.math.Vector2(offset).rotate(-(self.angle + angle))
        rotated_rect = rotated_image.get_rect(center = pygame.math.Vector2(pivot) + rotated_offset)

        images.append((rotated_image, rotated_rect))

        # Render sub-entities that are renderable
        for entity in self.entities:
            if entity.isRenderable:
                images.extend(entity.render(pivot, entity.position, self.angle + angle))

        return images
