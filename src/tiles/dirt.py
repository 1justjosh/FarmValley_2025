from src.engine.settings import *
from src.tiles.tiles import Tile

class Dirt(Tile):
    def __init__(self,pos,img,group):
        super().__init__(pos,img,group,"dirt")

        self.plant_type = None
        self.plant_stage = 0