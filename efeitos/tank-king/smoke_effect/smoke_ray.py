import pyray as rl
import random

screen_width = 750
screen_height = 650
FPS = 60

rl.init_window(screen_width, screen_height, "Smoke Effect")
rl.set_target_fps(FPS)

IMAGE = rl.load_texture("smoke.png")


class SmokeParticle:
    def __init__(self, x=screen_width // 2, y=screen_height // 2):
        self.x = x
        self.y = y
        self.scale_k = 0.1
        self.alpha = 255
        self.alpha_rate = 3
        self.alive = True
        self.vx = 0
        self.vy = 4 + random.randint(7, 10) / 10
        self.k = 0.01 * random.random() * random.choice([-1, 1])

    def update(self):
        self.x += self.vx
        self.vx += self.k
        self.y -= self.vy
        self.vy *= 0.99
        self.scale_k += 0.005
        self.alpha -= self.alpha_rate
        if self.alpha < 0:
            self.alpha = 0
            self.alive = False
        self.alpha_rate -= 0.1
        if self.alpha_rate < 1.5:
            self.alpha_rate = 1.5

    def draw(self):
        src = rl.Rectangle(0, 0, IMAGE.width, IMAGE.height)
        dst = rl.Rectangle(
            self.x - (IMAGE.width * self.scale_k) / 2,
            self.y - (IMAGE.height * self.scale_k) / 2,
            IMAGE.width * self.scale_k,
            IMAGE.height * self.scale_k,
        )
        origin = rl.Vector2(0, 0)
        tint = rl.Color(255, 255, 255, int(self.alpha))
        rl.draw_texture_pro(IMAGE, src, dst, origin, 0.0, tint)


class Smoke:
    def __init__(self, x=screen_width // 2, y=screen_height // 2 + 150):
        self.x = x
        self.y = y
        self.particles = []
        self.frames = 0

    def update(self):
        self.particles = [i for i in self.particles if i.alive]
        self.frames += 1
        if self.frames % 2 == 0:
            self.frames = 0
            for _ in range(1): # 15 to test lag
                self.particles.append(SmokeParticle(self.x, self.y))
        for i in self.particles:
            i.update()

    def draw(self):
        for i in self.particles:
            i.draw()


smoke = Smoke()


def main_game():
    while not rl.window_should_close():
        smoke.update()
        smoke.draw()
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        smoke.draw()

        # Print FPS on the screen
        fps = rl.get_fps()
        rl.draw_text(f"FPS: {fps}", 10, 10, 20, rl.WHITE)

        rl.end_drawing()

    rl.unload_texture(IMAGE)
    rl.close_window()


main_game()
