import math
import os

import pyray as rl


WINDOW_W = 1280
WINDOW_H = 720
FPS = 60

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "4.png")


class Wave:
	def __init__(self, x: float, y: float) -> None:
		self.x = x
		self.y = y
		self.radius = 0.0
		self.speed = 210.0
		self.thickness = 55.0
		self.strength = 26.0
		self.life = 1.2
		self.age = 0.0

	@property
	def alive(self) -> bool:
		return self.age < self.life

	def update(self, dt: float) -> None:
		self.age += dt
		self.radius += self.speed * dt


def clamp(v: float, v_min: float, v_max: float) -> float:
	return max(v_min, min(v, v_max))


def draw_wave_distortion(texture: rl.Texture, tx: float, ty: float, wave: Wave) -> None:
	# Sample tiny texture patches on a growing ring and push them outward.
	sigma = wave.thickness * 0.45
	life_factor = 1.0 - clamp(wave.age / wave.life, 0.0, 1.0)
	patch = 10.0

	angle_step = 7
	radial_steps = 6
	radial_start = wave.radius - (wave.thickness * 0.5)
	radial_end = wave.radius + (wave.thickness * 0.5)

	for deg in range(0, 360, angle_step):
		a = math.radians(deg)
		nx = math.cos(a)
		ny = math.sin(a)

		for i in range(radial_steps):
			t = i / max(1, radial_steps - 1)
			rr = radial_start + (radial_end - radial_start) * t

			lx = wave.x + nx * rr
			ly = wave.y + ny * rr

			if lx < 1 or ly < 1 or lx > texture.width - 1 or ly > texture.height - 1:
				continue

			gauss = math.exp(-((rr - wave.radius) ** 2) / (2.0 * sigma * sigma))
			push = wave.strength * gauss * life_factor

			src = rl.Rectangle(lx - patch * 0.5, ly - patch * 0.5, patch, patch)
			dst = rl.Rectangle(
				tx + lx - patch * 0.5 + nx * push,
				ty + ly - patch * 0.5 + ny * push,
				patch,
				patch,
			)

			alpha = int(220 * gauss * life_factor)
			tint = rl.Color(255, 255, 255, alpha)
			rl.draw_texture_pro(texture, src, dst, rl.Vector2(0, 0), 0.0, tint)


def main() -> None:
	rl.init_window(WINDOW_W, WINDOW_H, "Onda por Clique - Dilatacao de Pixels")
	rl.set_target_fps(FPS)

	if not os.path.exists(IMAGE_PATH):
		raise FileNotFoundError(f"Imagem nao encontrada: {IMAGE_PATH}")

	texture = rl.load_texture(IMAGE_PATH)
	waves: list[Wave] = []

	try:
		while not rl.window_should_close():
			dt = rl.get_frame_time()

			if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
				mx = rl.get_mouse_x()
				my = rl.get_mouse_y()

				tx = (rl.get_screen_width() - texture.width) * 0.5
				ty = (rl.get_screen_height() - texture.height) * 0.5

				local_x = mx - tx
				local_y = my - ty

				if 0 <= local_x <= texture.width and 0 <= local_y <= texture.height:
					waves.append(Wave(local_x, local_y))

			for wave in waves:
				wave.update(dt)
			waves = [wave for wave in waves if wave.alive]

			tx = (rl.get_screen_width() - texture.width) * 0.5
			ty = (rl.get_screen_height() - texture.height) * 0.5

			rl.begin_drawing()
			rl.clear_background(rl.Color(14, 17, 24, 255))

			rl.draw_texture(texture, int(tx), int(ty), rl.WHITE)

			for wave in waves:
				draw_wave_distortion(texture, tx, ty, wave)

			rl.draw_text("Clique na imagem para criar uma bolha crescente", 20, 20, 24, rl.RAYWHITE)
			rl.draw_text(f"Ondas ativas: {len(waves)}", 20, 52, 22, rl.LIGHTGRAY)

			rl.end_drawing()
	finally:
		rl.unload_texture(texture)
		rl.close_window()


if __name__ == "__main__":
	main()
