import pyray as rl
import math
from building import Building

class EndgameManager:
    def __init__(self, game_manager):
        self.gm = game_manager
        self.state = "NONE"
        self.timer = 0
        self.flash_timer = 0    
        self.flash_state = None 

    def is_defended(self, target_x, target_y):
        for y in range(self.gm.world.height):
            for x in range(self.gm.world.width):
                b = self.gm.world.map[y][x]
                if b.id == "defensive nuke" and b.parent is None:
                    # Centro da nuke é (+1, +1)
                    nx, ny = b.x + 1, b.y + 1
                    # Checa se o centro do evento alvo está na área 41x41 da nuke
                    if abs(target_x - nx) <= 20 and abs(target_y - ny) <= 20:
                        return True
        return False
        
    def tick(self):
        if self.state == "NONE":
            # Checa a cada 60 frames para não pesar, se "the face" foi construído
            if self.timer % 60 == 0:
                for y in range(self.gm.world.height):
                    for x in range(self.gm.world.width):
                        b = self.gm.world.map[y][x]
                        if b.id == "the face" and b.parent is None:
                            self.state = "FADE_1"
                            self.timer = 0
                            return
            self.timer += 1

        elif self.state == "FADE_1":
            self.timer += 1
            if self.timer >= 200: # 10 segundos
                self.state = "FADE_2"
                self.timer = 0

        elif self.state == "FADE_2":
            self.timer += 1
            if self.timer >= 180: # 3 segundos
                self.state = "AIMING"
                self.timer = 0

        elif self.state == "AIMING":
            if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                cam = self.gm.camera
                exact_x = (rl.get_mouse_x() / (cam.escala * cam.zoom)) - cam.pos.x
                exact_y = (rl.get_mouse_y() / (cam.escala * cam.zoom)) - cam.pos.y
                grid_x = math.floor(exact_x)
                grid_y = math.floor(exact_y)
                
                # Checa se o local mirado pelo jogador está protegido
                if self.is_defended(grid_x, grid_y):
                    # Interceptado! Ativa o clarão branco sem destruir nada
                    self.flash_timer = 60
                    self.flash_state = 'white'
                    if hasattr(cam, 'start_shake'):
                        cam.start_shake(30, 0.2) # Tremor mais leve
                else:
                    # Não protegido. Destrói área de 3x3 (Centro + bordas)
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            wx, wy = grid_x + dx, grid_y + dy
                            if 0 <= wx < self.gm.world.width and 0 <= wy < self.gm.world.height:
                                self.gm.world.destroy_building(wx, wy)
                    
                    if hasattr(cam, 'start_shake'):
                        cam.start_shake(60, 0.5)

                self.state = "WAITING"
                self.timer = 1 * 60 * 60 # 1 minutos (18000 frames a 60 FPS)

        elif self.state == "WAITING":
            self.timer -= 1
            # Checa se o total possível de armazenar pessoas caiu a 0 (Destruiu os apartamentos/tendas)
            people_capacity = self.gm.resources_storage.get("people", 0)
            
            if people_capacity == 0:
                self.state = "WIN"
            elif self.timer <= 0:
                self.state = "DEFEAT"
        
        elif self.state in ["WIN", "DEFEAT"]:
            # Verifica o clique no botão de Restart
            mouse_pos = rl.get_mouse_position()
            btn_rect = rl.Rectangle(rl.get_screen_width()//2 - 100, rl.get_screen_height()//2 + 50, 200, 50)
            if rl.check_collision_point_rec(mouse_pos, btn_rect) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                self.restart_game()

    def render(self):
        if self.state == "NONE": return
        
        screen_w = rl.get_screen_width()
        screen_h = rl.get_screen_height()

        # --- Desenha o clarão branco caso o meteoro seja defendido ---
        if hasattr(self, 'flash_timer') and self.flash_timer > 0:
            self.flash_timer -= 1
            color = rl.WHITE if self.flash_state == 'white' else rl.RED
            rl.draw_rectangle(0, 0, screen_w, screen_h, rl.fade(color, 0.8))
        # -----------------------------------------------------------
        
        if self.state in ["FADE_1", "FADE_2"]:
            # Fade out gradativo para o preto
            alpha = min(1.0, self.timer / 200.0) if self.state == "FADE_1" else 1.0
            rl.draw_rectangle(0, 0, screen_w, screen_h, rl.fade(rl.BLACK, alpha))
            
            # Texto 1
            text1 = b"Ribopolho isn't going to let Elon Musk steal his gold."
            rl.draw_text(text1, screen_w//2 - rl.measure_text(text1, 20)//2, screen_h//2 - 20, 20, rl.RAYWHITE)
            
            # Texto 2 (após 3 seg)
            if self.state == "FADE_2":
                text2 = b"He must destroy all Elons empire with just one meteor..."
                rl.draw_text(text2, screen_w//2 - rl.measure_text(text2, 20)//2, screen_h//2 + 20, 20, rl.RED)

        elif self.state == "AIMING":
            cam = self.gm.camera
            exact_x = (rl.get_mouse_x() / (cam.escala * cam.zoom)) - cam.pos.x
            exact_y = (rl.get_mouse_y() / (cam.escala * cam.zoom)) - cam.pos.y
            grid_x = math.floor(exact_x)
            grid_y = math.floor(exact_y)
            
            # Desenha a grade vermelha de área alvo 3x3
            cam.draw_rect(rl.Rectangle(grid_x - 1, grid_y - 1, 3, 3), rl.fade(rl.RED, 0.5))

            msg = b"AIM YOUR METEOR! Destroy the empire!"
            rl.draw_text(msg, screen_w//2 - rl.measure_text(msg, 30)//2, 50, 30, rl.RED)

        elif self.state == "WAITING":
            time_left = self.timer // 60
            text = f"Time left to collapse: {time_left}s".encode()
            rl.draw_text(text, screen_w//2 - rl.measure_text(text, 30)//2, 50, 30, rl.RED)

        elif self.state in ["WIN", "DEFEAT"]:
            rl.draw_rectangle(0, 0, screen_w, screen_h, rl.fade(rl.BLACK if self.state == "WIN" else rl.MAROON, 0.8))
            
            if self.state == "WIN":
                msg = b"Win: Ribopolho prevent Elon Musk to destroy its planet"
                color = rl.GREEN
            else:
                msg = b"Defeat: Ribopolho was not able to stop Elon Musk"
                color = rl.WHITE
                
            rl.draw_text(msg, screen_w//2 - rl.measure_text(msg, 25)//2, screen_h//2 - 50, 25, color)
            
            # Botão Restart
            btn_rect = rl.Rectangle(screen_w//2 - 100, screen_h//2 + 50, 200, 50)
            mouse_pos = rl.get_mouse_position()
            is_hover = rl.check_collision_point_rec(mouse_pos, btn_rect)
            
            rl.draw_rectangle_rec(btn_rect, rl.GRAY if is_hover else rl.DARKGRAY)
            rl.draw_rectangle_lines_ex(btn_rect, 2, rl.WHITE)
            rl.draw_text(b"Restart", int(screen_w//2 - rl.measure_text(b"Restart", 20)//2), int(screen_h//2 + 65), 20, rl.WHITE)

    def restart_game(self):
        self.gm.should_restart = True