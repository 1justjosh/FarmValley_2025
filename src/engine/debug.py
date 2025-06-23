from src.engine.settings import *
import psutil as ps

class Debug:
    def __init__(self,window):
        self.win = pg.display.get_surface()

        self.window = window
        self.generator = self.window.scene.generator

        self.border = pg.Surface((self.win.get_width() / 4,self.win.get_height() / 3))

        self.border_rect = self.border.get_rect(topleft=(0,0))

        self.title = TITLE_FONT.render("-----------Debug-----------",False,(100,100,100))
        self.title_rect = self.title.get_rect(midtop=self.border_rect.midtop)

        self.show = False

    def get_resource_usage(self):
        process = ps.Process(os.getpid())
        memory = process.memory_info().rss / 1024 / 1024  # Memory in MB
        cpu = process.cpu_percent()  # CPU usage over 0.1 seconds
        return memory, cpu

    def render(self):
        generator = self.window.scene.generator
        if not generator or self.window.scene.loading:
            return

        self.border.fill((0,0,0))
        self.border.set_alpha(100)

        rendered_tiles = DEFAULT_FONT.render(f"Tiles Rendered: {generator.visible_sprites.rendered_tiles}",False,(100,100,100))
        memory_usage = DEFAULT_FONT.render(f"Mem Usage: {self.get_resource_usage()[0] :.0f} Mb",False,(100,100,100))
        cpu_usage = DEFAULT_FONT.render(f"CPU %: {self.get_resource_usage()[1]}",False,(100,100,100))

        self.border.blit(self.title,self.title_rect)
        self.border.blit(rendered_tiles,(0,self.title_rect.bottom))
        self.border.blit(memory_usage,(0,self.title_rect.bottom + rendered_tiles.get_height()))
        self.border.blit(cpu_usage,(0,self.title_rect.bottom + rendered_tiles.get_height() + memory_usage.get_height()))

        self.win.blit(self.border,self.border_rect)
