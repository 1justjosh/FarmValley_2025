import threading
from src.world.generator import Generator
from src.engine.settings import *
from src.ui.loading_scene import LoadingScreen

class Scene:
    def __init__(self):
        self.win = pg.display.get_surface()
        self.generator = None
        self.loading = True
        self.loading_ui = LoadingScreen()

        self.load_thread = threading.Thread(target=self.load_generator)
        self.load_thread.start()

    def load_generator(self):
        self.generator = Generator()
        self.loading = False

    def update(self, dt):
        if self.loading:
            self.loading_ui.update(dt)
        else:
            self.generator.update(dt)

    def render(self):
        if self.loading:
            self.loading_ui.render(self.win)
        else:
            self.generator.render()

    def event_handler(self, event):
        if not self.loading:
            self.generator.event_handler(event)
