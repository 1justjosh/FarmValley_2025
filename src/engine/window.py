from src.engine.debug import Debug
from src.engine.settings import *
from src.engine.scene import Scene

class Window:
    def __init__(self):
        flags = pg.SCALED

        self.win = pg.display.set_mode(RES,flags=flags if flags else 0)
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.dt = 0

        self.scene = Scene()
        self.debug = Debug(self)
        self.running = True

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.JOYBUTTONDOWN:
                self.joystick_active = True
            if event.type == pg.KEYDOWN:
                self.joystick_active = False
                if event.key == pg.K_F2:
                    pg.display.toggle_fullscreen()

            self.scene.event_handler(event)

    def render(self):
        self.win.fill((10, 40, 80))
        self.scene.render()

        if self.debug and self.debug.show:
            self.debug.render()

        pg.display.flip()

    def update(self):
        dt = self.clock.tick(0) / 1000
        self.dt = dt

        self.debug.update(dt)

        pg.display.set_caption(f"{TITLE} | FPS: [{self.clock.get_fps() :.0f}] | DT: [{dt}]")

        self.scene.update(dt)

    def run(self):
        while self.running:
            self.event_handler()
            self.update()
            self.render()