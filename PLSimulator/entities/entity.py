import os
import pygame
from pygame import Vector2
from shapely.geometry import Polygon

from PLSimulator.constants import ASSET_DATA_DIRECTORY


class Entity:
    '''
        Entity

        This is the entity class from which all other entities will inherit.
    '''

    def __init__(
            self,
            asset_name: str,
            asset_size: Vector2 = Vector2(64, 64),
            position: Vector2 = Vector2(0, 0),
            velocity: Vector2 = Vector2(0, 0),
            angle: float = 0,
            mass: float = 1,
            entities: "list[Entity]" = [],
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
        self.acceleration = Vector2(0, 0)
        self.velocity = velocity
        self.angle = angle
        self.mass = mass + sum([e.mass for e in entities])
        self.entities = entities
        self.isRenderable = isRenderable
        self.isCollidable = isCollidable

        image_path = os.path.join(ASSET_DATA_DIRECTORY, asset_name)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.flip(self.image, self._asset_size[0] < 0, self._asset_size[1] < 0)
        self.image = pygame.transform.scale(self.image, (abs(self._asset_size[0]), abs(self._asset_size[1])))

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
        self.acceleration = force / self.mass

        # Update velocity
        self.velocity += self.acceleration

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
        # Return if entity is not renderable
        if not self.isRenderable:
            return []

        # Rotate this entity
        rotated_image = pygame.transform.rotozoom(self.image, self.angle + angle, 1)
        rotated_offset = offset.rotate(-(self.angle + angle))
        rotated_rect = rotated_image.get_rect(center=pivot + rotated_offset)

        # Add rotated image to list
        images = [(rotated_image, rotated_rect)]

        # Add all sub-entities as rotated images
        for entity in self.entities:
            images.extend(entity.render(pivot, entity.position, self.angle + angle))

        return images

    def polygon(self, pivot: Vector2 = Vector2(0, 0), offset: Vector2 = Vector2(0, 0), angle: float = 0) -> list:
        '''
            Calculate the polygon for this entity and any sub-entities

            Parameters:
                pivot: Position around which to rate
                offset: Offset from the pivot to place image
                angle: Heading of the image relative to parent

            Returns:
                images: List of rotated polygons to collide
        '''
        # Return if entity is not renderable or collidable
        if not self.isRenderable or not self.isCollidable:
            return []

        # Rotate this entity
        rotated_image = pygame.transform.rotozoom(self.image, self.angle + angle, 1)
        rotated_offset = offset.rotate(-(self.angle + angle))
        rotated_rect = rotated_image.get_rect(center=pivot + rotated_offset)

        # Add rotated polygon to list
        vertices = [rotated_rect.topleft, rotated_rect.topright, rotated_rect.bottomright, rotated_rect.bottomleft]
        polygons = [(self, Polygon(vertices))]

        # Add all sub-entities as rotated polygons
        for entity in self.entities:
            polygons.extend(entity.polygon(pivot, entity.position, self.angle + angle))

        return polygons

    def collides_with(self, other: "Entity") -> bool:
        '''
            Check whether other Entity collides with this Entity

            Parameters:
                other: Other base entity to consider

            Returns:
                collision: Whether a collision has occurred
        '''
        # Return if entity is not collidable or renderable
        if not self.isCollidable or not other.isCollidable:
            return []

        # Return if other entity is identical to self
        if self == other:
            return []

        # Generate polygons for both objects
        this_polygons = self.polygon(self.position)
        other_polygons = other.polygon(other.position)

        # For each polygon object, see if it intersects in any other polygon
        collisions = []
        for this_object, this_polygon in this_polygons:
            for other_object, other_polygon in other_polygons:
                if this_polygon.intersects(other_polygon):
                    collisions.append((this_object, other_object))

        return collisions
