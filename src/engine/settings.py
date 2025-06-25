import pygame as pg
from pygame.math import Vector2 as vec2
import os

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 6

VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

RES = WIDTH,HEIGHT = 1080,720
TITLE = f"Farm Valley | Version: {VERSION}"

TILE_SIZE = 64

IMAGE_PATH = os.path.join("assets", "images")
WORLD_PATH = os.path.join("assets", "world", "maps")

LAYERS = [
    "water",
    "floor",
    "dirt",
    "plants",
    "entities"
]

COLLIDE_LAYERS = [
    "world-end"
]

pg.font.init()

DEFAULT_FONT = pg.font.Font(pg.font.get_default_font())
TITLE_FONT = pg.font.Font(pg.font.get_default_font(),30)