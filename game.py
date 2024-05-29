import sys
import pygame as pg
from car import Car
from track import Track
from settings import *


class Game:
    track: Track
    car: Car

    def __init__(self) -> None:
        self.track = Track()
        self.car = Car(*self.track.get_starting_pos())

    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)

    def update(self, direction: list[int]) -> tuple[int, bool, int]:
        return self.car.update(self.track, direction)

    def draw(self) -> None:
        SCREEN.fill((0, 150, 0))
        self.track.draw()
        self.car.draw()

    def display_text(self, text: str, value: int, x: int, y: int):
        vel_text: str = f"{text}: {value}"
        text_render: pg.Surface = FONT.render(vel_text, True, (255, 255, 255))
        SCREEN.blit(text_render, (x, y))

    def reset(self) -> None:
        self.track = Track()
        self.car.reset_position(self.track)
