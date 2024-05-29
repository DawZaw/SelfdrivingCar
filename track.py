import math
import random
import pygame as pg
from settings import *


class Track:
    width: int
    track: list[tuple[float, float]]
    surface: pg.Surface
    masks: list[list[pg.Mask]]

    def __init__(self) -> None:
        self.width = 50
        self.track = self.init_track()
        self.surface = self.track_surface()
        self.masks = self.track_masks()

    def draw(self) -> None:
        # Draw border of a track
        for point in self.track:
            pg.draw.circle(SCREEN, (15, 15, 15), point, self.width + 10)
        # Draw track
        for point in self.track:
            pg.draw.circle(SCREEN, (60, 60, 60), point, self.width)

    def init_track(self) -> list[tuple[float, float]]:
        # Create points in a circle with random variation
        track: list[tuple[float, float]] = []
        for i in range(0, 360, 18):
            x: float = 400 + random.randint(250, 350) * math.cos(math.radians(i))
            y: float = 400 + random.randint(250, 350) * math.sin(math.radians(i))
            track.append((x, y))

        # Interpolate between those points to get more points to draw track
        new_track: list[tuple[float, float]] = []
        for i in range(len(track)):
            start: tuple[float, float] = track[i]
            end: tuple[float, float] = track[(i + 1) % len(track)]
            for i in range(11):
                hx: float = pg.math.lerp(start[0], end[0], i / 10)
                hy: float = pg.math.lerp(start[1], end[1], i / 10)
                new_track.append((hx, hy))
        return new_track

    def get_starting_pos(self) -> tuple[float, float]:
        return self.track[0][0], self.track[0][1]

    def track_surface(self) -> pg.Surface:
        # Create track surface
        surface: pg.Surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        surface.fill(0)
        for point in self.track:
            pg.draw.circle(surface, (255, 255, 255), point, self.width)
        return surface

    def track_masks(self) -> list[list[pg.Mask]]:
        # Create masks for track with 4 flipped versions
        mask: pg.Mask = pg.mask.from_surface(self.surface)
        mask_fx: pg.Mask = pg.mask.from_surface(
            pg.transform.flip(self.surface, True, False)
        )
        mask_fy: pg.Mask = pg.mask.from_surface(
            pg.transform.flip(self.surface, False, True)
        )
        mask_fx_fy: pg.Mask = pg.mask.from_surface(
            pg.transform.flip(self.surface, True, True)
        )
        pg.mask.Mask.invert(mask)
        pg.mask.Mask.invert(mask_fx)
        pg.mask.Mask.invert(mask_fy)
        pg.mask.Mask.invert(mask_fx_fy)
        return [[mask, mask_fy], [mask_fx, mask_fx_fy]]
