import threading

from src.ui.paused_menu import PausedMenu
from src.world.generator import Generator
from src.engine.settings import *
from src.ui.loading_scene import LoadingScreen

class Scene:
    def __init__(self):
        self.win = pg.display.get_surface()
        self.generator = None
        self.pause_menu = None
        self.paused = False
        self.loading = True
        self.loading_ui = LoadingScreen()

        self.load_thread = threading.Thread(target=self.load_generator)
        self.load_thread.start()

    def load_generator(self):
        self.generator = Generator()
        self.pause_menu = PausedMenu()
        self.loading = False

    def event_handler(self, event):
        if not self.loading:
            self.generator.event_handler(event)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused

    def update(self, dt):
        if self.loading:
            self.loading_ui.update(dt)
        else:
            if not self.paused:
                self.generator.update(dt)
            else:
                self.pause_menu.update(dt)

    def render(self):
        if self.loading:
            self.loading_ui.render(self.win)
        else:
            self.generator.render()
            if self.paused:
                self.pause_menu.render()
