from src.engine.settings import *
from src.engine.utils import load_tile_map

class PausedMenu:
    def __init__(self):
        self.win = pg.display.get_surface()

        self.filter = pg.Surface((WIDTH, HEIGHT))
        self.filter.set_alpha(100)

        self.border = load_tile_map("assets/images/emojis/emoji style ui/Inventory_Blocks_Spritesheet.png",48,48,scale=(WIDTH,HEIGHT))[6]
        self.border_rect = self.border.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.title = TITLE_FONT.render("PAUSED",False,(255,255,255))

    def update(self,dt):
        pass

    def render(self):
        self.win.blit(self.filter)

        self.border.blit(self.title,vec2(self.border_rect.midtop) + vec2(0,128))

        self.win.blit(self.border,self.border_rect)
