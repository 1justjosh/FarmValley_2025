from src.engine.settings import *
import psutil as ps
import threading

class Debug:
    def __init__(self,window):
        self.win = pg.display.get_surface()

        self.window = window
        self.generator = self.window.scene.generator

        self.border = pg.Surface((self.win.get_width() / 4,self.win.get_height() / 3))

        self.border_rect = self.border.get_rect(topleft=(0,0))
        self.max_width = 0

        self.cpu_usage = 0.0
        self._start_cpu_monitor()

        self.frame_time_ms = 0

        self.title = TITLE_FONT.render("-----------Debug-----------",False,(100,100,100))
        self.title_rect = self.title.get_rect(midtop=self.border_rect.midtop)

        self.show = False

    def get_resource_usage(self):
        process = ps.Process(os.getpid())
        memory = process.memory_info().rss / 1024 / 1024  # Memory in MB
        return memory


    def update(self,dt):
        generator = self.window.scene.generator
        if not generator or self.window.scene.loading:
            return

        self.frame_time_ms = dt * 1000
        self.show = generator.player.show_debug

    def _start_cpu_monitor(self):
        def cpu_loop():
            while True:
                self.cpu_usage = ps.cpu_percent(interval=1)  # runs in background

        threading.Thread(target=cpu_loop, daemon=True).start()

    def render(self):
        generator = self.window.scene.generator
        if not generator or self.window.scene.loading:
            return

        self.border.fill((0,0,0))
        self.border.set_alpha(200)

        rendered_tiles = DEFAULT_FONT.render(f"Tiles Rendered: {generator.visible_sprites.rendered_tiles}",False,(100,100,100))
        width = rendered_tiles.get_width()
        memory_usage = DEFAULT_FONT.render(f"Mem Usage: {self.get_resource_usage() :.0f} Mb",False,(100,100,100))
        if memory_usage.get_width() >= width:
            width = memory_usage.get_width()
        cpu_usage = DEFAULT_FONT.render(f"CPU %: {self.cpu_usage}", False, (100, 100, 100))
        if cpu_usage.get_width() >= width:
            width = memory_usage.get_width()

        frame_label = f"Frame Time: {self.frame_time_ms:.2f} ms"
        if self.frame_time_ms > 18:
            frame_label += " ⚠️ Spike!"

        frame_time_text = DEFAULT_FONT.render(frame_label, False,
                                              (200, 80, 80) if "Spike" in frame_label else (100, 100, 100))

        if self.title.get_width() >= width:
            width = self.title.get_width()

        self.border_rect.width = width

        self.border = pg.Surface((width, self.border.get_height()))
        self.border.set_alpha(200)
        self.border_rect = self.border.get_rect(topleft=(0, 0))
        self.title_rect = self.title.get_rect(midtop=self.border_rect.midtop)

        self.border.blit(self.title,self.title_rect)
        self.border.blit(rendered_tiles,(0,self.title_rect.bottom))
        self.border.blit(memory_usage,(0,self.title_rect.bottom + rendered_tiles.get_height()))
        self.border.blit(cpu_usage,(0,self.title_rect.bottom + rendered_tiles.get_height() + memory_usage.get_height()))
        self.border.blit(frame_time_text, (0,self.title_rect.bottom + rendered_tiles.get_height() + memory_usage.get_height() + cpu_usage.get_height()))  # position accordingly

        self.win.blit(self.border,self.border_rect)

        offset_rect = generator.player.hitbox.copy()
        offset_rect.topleft -= generator.visible_sprites.offset

        pg.draw.rect(self.win,"blue",offset_rect,2)

        pg.draw.circle(self.win,"yellow",vec2(offset_rect.center) + generator.player.action_direction[generator.player.status.split("_")[0]],2)

        for rect in generator.player.collide_objects:
            offset_rect = rect.copy()
            offset_rect.topleft -= generator.visible_sprites.offset
            pg.draw.rect(self.win, "red", offset_rect, 2)