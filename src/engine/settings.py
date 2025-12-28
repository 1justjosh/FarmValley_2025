import pygame as pg
from pygame.math import Vector2 as vec2
import os
import math

VERSION_MAJOR = 0
VERSION_MINOR = 2
VERSION_PATCH = 6

VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

RES = WIDTH,HEIGHT = 1080,720
TITLE = f"Farm Valley | Version: {VERSION}"

TILE_SIZE = 64

IMAGE_PATH = os.path.join("assets", "images")
WORLD_PATH = os.path.join("assets", "world", "maps")
AUDIO_PATH = os.path.join("assets", "audio")

LAYERS = [
    "water",
    "floor",
    "dirt",
    "main"
]


COLLIDE_LAYERS = [
    "world-end"
]

pg.init()

SAVE_TIMER = 3 # seconds for auto save

MINUTE_COUNT = 60

DEFAULT_FONT = pg.font.Font("assets/fonts/Minecraft.ttf")
TITLE_FONT = pg.font.Font("assets/fonts/Minecraft.ttf",60)