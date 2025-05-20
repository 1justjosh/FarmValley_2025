from src.engine.settings import *
from src.world.generator import Generator

class Scene:
    def __init__(self):
        self.win = pg.display.get_surface()

        self.generator = Generator()

    def event_handler(self,event):
        self.generator.event_handler(event)

    def update(self,dt):
        self.generator.update(dt)

    def render(self):
        self.generator.render()