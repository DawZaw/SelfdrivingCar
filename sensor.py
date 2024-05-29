from __future__ import annotations

import math
import pygame as pg
from typing import TYPE_CHECKING

from track import Track
from settings import *

if TYPE_CHECKING:
    from car import Car


class Sensor:
    surface: pg.Surface
    angle: float
    length: float
    hit_point: tuple[float, float] | None

    def __init__(self, angle: float, surface: pg.Surface) -> None:
        self.surface = surface
        self.angle = angle
        self.length = 0
        self.hit_point = None

    def draw(self, car: Car) -> None:
        if self.hit_point:
            pg.draw.line(SCREEN, (0, 0, 255), (car.x, car.y), self.hit_point)
            pg.draw.circle(SCREEN, (0, 255, 0), self.hit_point, 3)

    def update(self, car: Car, track: Track) -> None:
        self.raycast(car, track)

    def raycast(self, car: Car, track: Track) -> None:
        # Calculate angle of ray
        cos: float = math.cos(math.radians(car.angle + self.angle))
        sin: float = math.sin(math.radians(car.angle + self.angle))

        # Get flipped mask based on ray angle
        flip_x: bool = cos < 0
        flip_y: bool = sin < 0
        flipped_mask: pg.Mask = track.masks[flip_x][flip_y]

        # Cast ray as long as possible
        x_dest: float = 400 + 1000 * abs(cos)
        y_dest: float = 400 + 1000 * abs(sin)

        # Draw ray on surface
        self.surface.fill((0, 0, 0, 0))
        pg.draw.line(self.surface, (255, 255, 255), (400, 400), (x_dest, y_dest))
        beam_mask = pg.mask.from_surface(self.surface)

        # Calculate offset based on position and which mask was used
        offset_x: float = 400 - car.x if flip_x else car.x - 400
        offset_y: float = 400 - car.y if flip_y else car.y - 400
        hit: tuple[float, float] | None = flipped_mask.overlap(
            beam_mask, (offset_x, offset_y)
        )

        # Get point of intersection with ray and edge of track
        if hit is not None and (hit[0] != car.x or hit[1] != car.y):
            hx: float = 799 - hit[0] if flip_x else hit[0]
            hy: float = 799 - hit[1] if flip_y else hit[1]
            self.hit_point = (hx, hy)

            # Calculate total length of ray
            self.length = math.sqrt(
                (car.x - self.hit_point[0]) ** 2 + (car.y - self.hit_point[1]) ** 2
            )
