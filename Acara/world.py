import pyray as rl

from camera import Camera

class World:
    def __init__(self, camera: Camera, width=100, height=100, escala=64) -> None:
        self.camera = camera
        self.width = width
        self.height = height
        self.escala = escala

        self.map = [[0 for _ in range(width)] for _ in range(height)]
        self.map[10][10] = 1
    def tick(self):
        pass

    def get_color(self, id):
        if id == 0:
            return rl.Color(100, 20, 20, 255)
        elif id == 1:
            return rl.GREEN
        elif id == 2:
            return rl.BLUE
        else:
            return rl.RED

    def render(self):
        rl.draw_text(b"Hello, World 2!", 10, 10, 20, rl.DARKGRAY)
        for x in range(self.width):
            for y in range(self.height):
                floor_rect = rl.Rectangle(x, y, 1, 1)
                self.camera.draw_rect(floor_rect, self.get_color(self.map[y][x]))