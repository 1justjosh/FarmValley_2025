import random

from src.engine.settings import *
from src.tiles.tiles import Tile

class Dirt(Tile):
    def __init__(self,pos,assets,group):
        base = assets["tiles"]["dirt"][12].copy()  # ← make a unique surface
        super().__init__(pos, base, group, "dirt")

        self.orig_image = base.copy()  # ← unique original

        self.assets = assets

        self.plant_type = None
        self.plant_stage = 0

        self.watered = False
        self.watered_duration = 10 # seconds of being watered

    def set_watered(self):
        if not self.watered:
            self.watered = True
            self.image.blit(random.choice(self.assets["tiles"]["water-objects"]["water_puddles"]),special_flags=pg.BLEND_RGB_SUB)

    def water(self, dt):
        if self.watered:
            self.watered_duration -= dt

            if self.watered_duration <= 0:
                self.watered_duration = 10
                self.watered = False
                self.image = self.orig_image


    def update(self,dt):
        self.water(dt)