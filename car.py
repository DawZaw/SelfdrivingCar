import math
import pygame as pg
from sensor import Sensor
from track import Track
from settings import *


class Car:
    # Car variables
    width: float
    height: float
    color: tuple[int, int, int]
    x: float
    y: float
    angle: float
    points: list[tuple[float, float]]
    score: int
    # Speed variables
    acc: float
    vel: float
    max_vel: float
    # Sensor variables
    sensors: list[Sensor]

    def __init__(self, x, y) -> None:
        # Car variables
        self.width = 14.142
        self.height = 22.360
        self.color = (200, 15, 15)
        self.x, self.y = x, y
        self.angle = 270
        self.points = self.get_points()
        self.score = 0
        # Speed variables
        self.acc = 0
        self.vel = 0
        self.max_vel = 3
        # Sensor variables
        sensor_count: int = 7
        sensor_surface: pg.Surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.sensors = [
            Sensor(angle, sensor_surface)
            for angle in range(-90, 91, 180 // (sensor_count - 1))
        ]

    def draw(self) -> None:
        for sensor in self.sensors:
            sensor.draw(self)
        pg.draw.polygon(SCREEN, self.color, self.points)

    def drive(self) -> None:
        # Apply acceleration if velocity < max velocity
        if self.vel <= self.max_vel:
            self.acc += 1
            self.acc *= 0.9
            self.vel += self.acc
        self.vel *= 0.9

    def update(self, track: Track, direction: list[int]) -> tuple[int, bool, int]:
        # Move car
        self.acc = 0
        self.drive()
        self.steer(direction)

        # Update position
        self.x += self.vel * math.cos(math.radians(self.angle))
        self.y += self.vel * math.sin(math.radians(self.angle))
        self.points = self.get_points()

        # Update sensor and check if game over
        for sensor in self.sensors:
            sensor.update(self, track)
            if self.game_over(sensor):
                reward: int = -500
                game_over: bool = True
                return reward, game_over, self.score

        # Update score based on frames alive
        self.score += 1
        reward = 1
        game_over = False
        return reward, game_over, self.score

    def steer(self, direction: list[int]) -> None:
        # Directions [turn_left, dont_turn, turn_right]
        selection: int = direction.index(1)
        if selection == 0:
            self.angle -= math.pi / 2
        if selection == 2:
            self.angle += math.pi / 2

    def reset_position(self, track: Track) -> None:
        self.x = track.track[0][0]
        self.y = track.track[0][1]
        self.angle = 270
        for sensor in self.sensors:
            sensor.update(self, track)
        self.score = 0

    def game_over(self, sensor: Sensor) -> bool:
        return sensor.length < 5

    def get_points(self) -> list[tuple[float, float]]:
        return [
            (
                self.x + self.width * math.cos(math.radians(self.angle + 45)),
                self.y + self.width * math.sin(math.radians(self.angle + 45)),
            ),
            (
                self.x + self.height * math.cos(math.radians(self.angle + 153.435)),
                self.y + self.height * math.sin(math.radians(self.angle + 153.435)),
            ),
            (
                self.x + self.height * math.cos(math.radians(self.angle + 206.565)),
                self.y + self.height * math.sin(math.radians(self.angle + 206.565)),
            ),
            (
                self.x + self.width * math.cos(math.radians(self.angle + 315)),
                self.y + self.width * math.sin(math.radians(self.angle + 315)),
            ),
        ]
