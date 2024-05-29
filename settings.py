import pygame as pg
from pygame.font import SysFont, Font
from pygame.time import Clock

pg.init()
pg.font.init()

# Game/Screen settings
WIDTH: int = 800
HEIGHT: int = 800
SIZE: tuple[int, int] = WIDTH, HEIGHT
SCREEN: pg.Surface = pg.display.set_mode(SIZE)
FPS: int = 30
FONT: Font = SysFont("rockwell", 24, bold=True)
CLOCK: Clock = Clock()

# Agent settings
MAX_MEMORY: int = 100_000
BATCH_SIZE: int = 1000
LR: float = 0.001
