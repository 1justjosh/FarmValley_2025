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
        self.loading = True
        self.loading_ui = LoadingScreen()

        self.load_thread = threading.Thread(target=self.load_generator)
        self.load_thread.start()

        self.s = pg.Surface((WIDTH,HEIGHT))
        self.s.fill((1,7,133))
        self.s.set_alpha(125)

    def load_generator(self):
        self.generator = Generator()
        self.pause_menu = PausedMenu()
        self.loading = False

        pg.mixer.music.load(os.path.join(AUDIO_PATH, "bit-beats-1-168243.mp3"))
        pg.mixer.music.play(-1)

    def event_handler(self, event):
        if not self.loading:
            self.generator.event_handler(event)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.generator.paused = not self.generator.paused

    def update(self, dt):
        if self.loading:
            self.loading_ui.update(dt)
        else:
            if not self.generator.paused:
                self.generator.update(dt)
            else:
                self.pause_menu.update(dt)

    def render(self):
        if self.loading:
            self.loading_ui.render(self.win)
        else:
            self.generator.render()
            if self.generator.paused:
                self.pause_menu.render()
