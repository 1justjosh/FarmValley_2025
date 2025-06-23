from src.engine.settings import *
from src.tiles.tiles import Tile

class AnimatedTile(Tile):
    def __init__(self,pos,frames,groups,z):
        super().__init__(pos,frames[0],groups,z)

        self.frames = frames

