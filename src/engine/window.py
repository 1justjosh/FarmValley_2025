from src.engine.settings import *
from src.engine.scene import Scene

class Window:
    def __init__(self):
        flags = None

        self.win = pg.display.set_mode(RES,flags=flags if flags else 0)
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()

        self.scene = Scene()

        self.running = True

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            self.scene.event_handler(event)

    def render(self):
        self.win.fill((10,40,80))
        self.scene.render()
        pg.display.flip()

    def update(self):
        dt = self.clock.tick(0) / 1000
        pg.display.set_caption(f"{TITLE} | FPS: [{self.clock.get_fps() :.0f}] | DT: {dt}")

        self.scene.update(dt)

    def run(self):
        while self.running:
            self.event_handler()
            self.update()
            self.render()