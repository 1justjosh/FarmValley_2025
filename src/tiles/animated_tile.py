from src.engine.settings import *
from src.tiles.tiles import Tile

class AnimatedTile(Tile):
    def __init__(self,pos,frames,groups,z):
        super().__init__(pos,frames[0],groups,z)


        self.index = 0
        self.anim_speed = 4

        self.frames = frames

    def animate(self,dt):
        self.index += self.anim_speed * dt

        if self.index >= len(self.frames):
            self.index = 0

        self.image = self.frames[int(self.index)]

    def update(self,dt):
        self.animate(dt)