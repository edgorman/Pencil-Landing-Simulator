from lib2to3.pytree import Base
import os
import pygame
from pygame import Vector2
from shapely.geometry import Polygon

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
        entities: "list[BaseEntity]" = [],
        isRenderable: bool = True,
        isCollidable: bool = True) -> None:
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
                isCollidable: Whether the entity is collidable

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
        self.isCollidable = isCollidable

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

    def render(self, pivot: Vector2 = Vector2(0, 0), offset: Vector2 = Vector2(0, 0), angle: float = 0, showNonCollidable: bool = True) -> list:
        '''
            Render the entity and any sub-entities to the window

            Parameters:
                pivot: Position around which to rate
                offset: Offset from the pivot to place image
                angle: Heading of the image relative to parent

            Returns:
                images: List of rotated images to render
        '''
        # Return if entity is not renderable
        if not self.isRenderable:
            return []

        # Return if should not show non collidable, and entity is not collidable
        if not showNonCollidable and not self.isCollidable:
            return []

        # Render this entity
        rotated_image = pygame.transform.rotozoom(self.image, self.angle + angle, 1)
        rotated_offset = offset.rotate(-(self.angle + angle))
        rotated_rect = rotated_image.get_rect(center = pivot + rotated_offset)

        # Render all sub-entities
        images = [(rotated_image, rotated_rect)]
        for entity in self.entities:
            if entity.isRenderable:
                images.extend(entity.render(pivot, entity.position, self.angle + angle, showNonCollidable))

        return images

    def collides_with(self, other: "BaseEntity") -> bool:
        '''
            Check whether other BaseEntity collides with this BaseEntity

            Parameters:
                other: Other base entity to consider
            
            Returns:
                collision: Whether a collision has occurred
        '''
        # Return if entity is not collidable or renderable
        if not self.isCollidable or not self.isRenderable:
            return False

        # Generate the rectangles for each entity
        this_rects = [r for _, r in self.render(self.position + self._asset_size, showNonCollidable=False)]
        other_rects = [r for _, r in other.render(other.position + other._asset_size, showNonCollidable=False)]

        # Convert these into polygon objects
        this_polygons = [Polygon([r.topleft, r.topright, r.bottomright, r.bottomleft]) for r in this_rects]
        other_polygons = [Polygon([r.topleft, r.topright, r.bottomright, r.bottomleft]) for r in other_rects]

        # For each polygon object, see if it intersects in any other polygon
        for t in this_polygons:
            for o in other_polygons:
                if t.intersects(o):
                    # A collision has occurred, exit early
                    return True

        # No collision has occurred
        return False


class Pencil(BaseEntity):
    '''
        Pencil

        This is the pencil entity class, including flame and rcs as sub-entities
    '''

    def __init__(self):
        super().__init__(
            'pencil.png', 
            Vector2(16, 128),
            Vector2(0, 0),
            Vector2(0, 0),
            0,
            30,  # TODO: to change on reset method
            [
                BaseEntity('engine_firing.png', Vector2(16, 80), Vector2(0, 84), Vector2(0, 0), 0, 0, [], False, False),
                BaseEntity('rcs_firing.png', Vector2(16, 16), Vector2(14, 53), Vector2(0, 0), 180, 0, [], False, False),
                BaseEntity('rcs_firing.png', Vector2(16, 16), Vector2(14, -53), Vector2(0, 0), 0, 0, [], False, False),
            ],
            True,
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
            Vector2(32, 876),  # TODO: to change on reset method
            Vector2(0, 0),
            0,
            100,
            [],
            True
        )
    