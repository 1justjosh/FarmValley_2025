import pygame as pg
from pygame.math import Vector2 as vec2
import os

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_PATCH = 0

VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

RES = WIDTH,HEIGHT = 1080,720
TITLE = f"Farm Valley | Version: {VERSION}"

TILE_SIZE = 64

IMAGE_PATH = os.path.join("assets", "images")
WORLD_PATH = os.path.join("assets", "world", "maps")

LAYERS = [
    "water",
    "floor",
    "entities"
]

COLLIDE_LAYERS = [
    "world-end"
]