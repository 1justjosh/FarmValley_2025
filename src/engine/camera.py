from src.engine.settings import *


class Camera(pg.sprite.Group):
    def __init__(self, generator):
        super().__init__()
        self.generator = generator
        self.win = pg.display.get_surface()
        self.offset = pg.math.Vector2()
        self.chunk_size = generator.chunk_size

        self.rendered_chunks = None
        self.rendered_tiles = 0

    def get_rendered_chunks(self):
        self.rendered_chunks = self.get_visible_chunks()

    def get_visible_chunks(self):
        buffer = self.chunk_size
        view_rect = pg.Rect(self.offset.x, self.offset.y, WIDTH, HEIGHT).inflate(buffer, buffer)

        start_x = int(view_rect.left // self.chunk_size)
        end_x = int(view_rect.right // self.chunk_size) + 1
        start_y = int(view_rect.top // self.chunk_size) - 1
        end_y = int(view_rect.bottom // self.chunk_size) + 1

        return {f"{x};{y}" for x in range(start_x, end_x) for y in range(start_y, end_y)}

    def render(self, player):
        self.offset.x = player.hitbox.centerx + 50 - WIDTH / 2
        self.offset.y = player.hitbox.centery + 50 - HEIGHT / 2

        draw_queue = []

        # Tiles from visible chunks
        for layer in LAYERS:
            for chunk_key in self.rendered_chunks:
                draw_queue.extend(self.generator.chunk_tiles.get(chunk_key, {}).get(layer, []))

        # Player and other dynamic sprites (already in the same group)
        draw_queue.extend(self.sprites())

        # Sort everything by vertical position
        draw_queue.sort(key=lambda sprite: sprite.hitbox.bottom)

        self.rendered_tiles = len(draw_queue)

        # Draw all to screen
        for layer in LAYERS:
            for sprite in draw_queue:
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.topleft -= self.offset
                    self.win.blit(sprite.image, offset_rect)

    def update(self, *args, **kwargs):
        self.get_rendered_chunks()

        super().update(*args, **kwargs)

        for layer in LAYERS:
            for chunk_key in self.rendered_chunks:
                for tile in self.generator.chunk_tiles.get(chunk_key, {}).get(layer, []):
                    tile.update(*args, **kwargs)
