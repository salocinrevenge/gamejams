import pyray as rl
import asyncio

from gameManager import GameManager

def init_window():
    rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
    rl.init_window(1000, 700, b"A cara")
    rl.set_target_fps(60)

def tick():
    pass

def draw(game_manager):
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    game_manager.render()

    rl.end_drawing()

async def main():
    init_window()
    game_manager = GameManager()

    while not rl.window_should_close():
        # --- Atualizacao ---
        game_manager.tick()

        # --- Desenho ---
        draw(game_manager)
        await asyncio.sleep(0)

    game_manager.on_close()
    rl.close_window()

if __name__ == "__main__":
    asyncio.run(main())

# Pah rodah na webi usa isso aqui:
# python -m pygbag .
# e vai no http://localhost:8000/