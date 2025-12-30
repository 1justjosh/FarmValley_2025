from src.engine.settings import *

class InventoryGUI:
    def __init__(self, generator):
        self.win = pg.display.get_surface()

        self.generator = generator

        #

        self.frame = pg.Surface((WIDTH // 2, 64),flags=pg.SRCALPHA)
        self.frame.fill("red")
        self.frame.blit(pg.transform.scale(self.generator.assets["HUD"]["frames"]["inventory"]["frame"],(WIDTH//4,64)))
        self.frame.blit(pg.transform.scale(self.generator.assets["HUD"]["frames"]["inventory"]["frame"],(WIDTH//4,64)), (WIDTH//4,0))

        self.frame_rect = self.frame.get_rect(midbottom=(WIDTH // 2, HEIGHT))

    def render(self):
        self.win.blit(self.frame, self.frame_rect)

    def update(self, dt):
        pass