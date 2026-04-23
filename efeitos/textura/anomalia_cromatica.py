import math
import os

import pyray as rl


IMAGE_PATH = os.path.join(os.path.dirname(__file__), "4.png")
WINDOW_TITLE = "Anomalia Cromatica - Pyray"
FPS = 60


def clamp(value: float, min_value: float, max_value: float) -> float:
	return max(min_value, min(value, max_value))


def draw_chromatic_texture(texture: rl.Texture, center_x: float, center_y: float, intensity: float) -> None:
	"""Draws three RGB-shifted passes to simulate chromatic aberration."""
	src = rl.Rectangle(0, 0, float(texture.width), float(texture.height))

	# Slightly different shift per channel gives a cleaner chromatic split.
	shifts = [
		(-intensity, -intensity * 0.30, rl.Color(255, 70, 70, 180)),
		(0.0, 0.0, rl.Color(120, 255, 120, 170)),
		(intensity, intensity * 0.30, rl.Color(90, 120, 255, 180)),
	]

	for shift_x, shift_y, tint in shifts:
		dst = rl.Rectangle(
			center_x - (texture.width / 2) + shift_x,
			center_y - (texture.height / 2) + shift_y,
			float(texture.width),
			float(texture.height),
		)
		rl.draw_texture_pro(texture, src, dst, rl.Vector2(0, 0), 0.0, tint)


def main() -> None:
	rl.init_window(1280, 720, WINDOW_TITLE)
	rl.set_target_fps(FPS)

	if not os.path.exists(IMAGE_PATH):
		raise FileNotFoundError(f"Imagem nao encontrada: {IMAGE_PATH}")

	texture = rl.load_texture(IMAGE_PATH)

	try:
		while not rl.window_should_close():
			screen_w = rl.get_screen_width()
			screen_h = rl.get_screen_height()
			center = rl.Vector2(screen_w / 2.0, screen_h / 2.0)
			mouse = rl.get_mouse_position()

			dx = mouse.x - center.x
			dy = mouse.y - center.y
			mouse_distance = math.sqrt(dx * dx + dy * dy)

			max_distance = math.sqrt((screen_w / 2.0) ** 2 + (screen_h / 2.0) ** 2)
			normalized = clamp(mouse_distance / max_distance, 0.0, 1.0)
			aberration_intensity = normalized * 18.0

			rl.begin_drawing()
			rl.clear_background(rl.Color(16, 18, 24, 255))

			rl.begin_blend_mode(rl.BlendMode.BLEND_ADDITIVE) # Additive blending helps the colors pop without darkening the image.
			draw_chromatic_texture(texture, center.x, center.y, aberration_intensity)
			rl.end_blend_mode()

			rl.draw_text("Mova o mouse para longe do centro", 20, 20, 24, rl.RAYWHITE)
			rl.draw_text(
				f"Intensidade: {aberration_intensity:.2f}",
				20,
				52,
				22,
				rl.LIGHTGRAY,
			)

			rl.draw_circle_v(center, 4.0, rl.YELLOW)
			rl.end_drawing()
	finally:
		rl.unload_texture(texture)
		rl.close_window()


if __name__ == "__main__":
	main()
