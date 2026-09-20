import pyray as rl
import math
import random

from building import Building

class Camera():
    def __init__(self, game_manager, pos:rl.Vector2, escala:float=64.0) -> None:
        self.game_manager = game_manager
        self.pos = pos 
        self.target = None
        self.zoom = 1.0
        self.escala = escala
        self.vel = 0.1
        self.shake_timer = 0
        self.shake_intensity = 0.0
        self.shake_offset = rl.Vector2(0, 0)
        
    def tick(self):
        # Detexta WASD ou setas para mover a camera
        if self.shake_timer > 0:
            self.shake_timer -= 1
            self.shake_offset.x = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_offset.y = random.uniform(-self.shake_intensity, self.shake_intensity)
        else:
            self.shake_offset.x = 0
            self.shake_offset.y = 0

        if rl.is_key_down(rl.KEY_W) or rl.is_key_down(rl.KEY_UP):
            self.pos.y += self.vel/self.zoom
        if rl.is_key_down(rl.KEY_S) or rl.is_key_down(rl.KEY_DOWN):
            self.pos.y -= self.vel/self.zoom
        if rl.is_key_down(rl.KEY_A) or rl.is_key_down(rl.KEY_LEFT):
            self.pos.x += self.vel/self.zoom
        if rl.is_key_down(rl.KEY_D) or rl.is_key_down(rl.KEY_RIGHT):
            self.pos.x -= self.vel/self.zoom

        # Obtém a largura da barra de recursos à esquerda (padrão 200 no resource_bar.py)
        left_hud_width = 200 
        right_hud_width = self.game_manager.hud.sidebar.width

        # apenas se o mouse estiver fora do HUD, para não interferir na rolagem do HUD
        if left_hud_width < rl.get_mouse_x() < rl.get_screen_width() - right_hud_width:
            # Scroll do mouse para aumentar/diminuir o zoom
            mouse_wheel_move = rl.get_mouse_wheel_move()
            if mouse_wheel_move != 0:
                old_zoom = self.zoom
                self.zoom += mouse_wheel_move * 0.1
                
                # Limites
                if self.zoom < 0.1:
                    self.zoom = 0.1
                elif self.zoom > 10.0:
                    self.zoom = 10.0
                    
                # Só faz o cálculo de compensação se o zoom realmente mudou (não travou no limite)
                if self.zoom != old_zoom:
                    # Pega a posição do mouse na tela (em pixels)
                    mouse_x = rl.get_mouse_x()
                    mouse_y = rl.get_mouse_y()
                    
                    # Calcula a diferença necessária para manter o ponto do mundo fixo sob o mouse
                    dx = (mouse_x / self.escala) * (1.0 / self.zoom - 1.0 / old_zoom)
                    dy = (mouse_y / self.escala) * (1.0 / self.zoom - 1.0 / old_zoom)
                    
                    # Aplica a correção na posição da câmera
                    self.pos.x += dx
                    self.pos.y += dy

    def draw_rect(self, rect:rl.Rectangle, color):
        rl.draw_rectangle(
            math.ceil(self.x(rect.x)*self.escala*self.zoom), 
            math.ceil(self.y(rect.y)*self.escala*self.zoom), 
            math.ceil(rect.width*self.escala*self.zoom), 
            math.ceil(rect.height*self.escala*self.zoom),
            color)
        rl.draw_rectangle_lines(
            math.ceil(self.x(rect.x)*self.escala*self.zoom), 
            math.ceil(self.y(rect.y)*self.escala*self.zoom), 
            math.ceil(rect.width*self.escala*self.zoom), 
            math.ceil(rect.height*self.escala*self.zoom),
            rl.BLACK)

    def draw_building(self, img_sprite_sheet, building:Building, highlight=False):
        color = rl.WHITE
        if highlight:
            color = rl.YELLOW
        rl.draw_texture_pro(
            img_sprite_sheet,
            rl.Rectangle(building.x_sprite_sheet*self.escala, building.y_sprite_sheet*self.escala, building.width*self.escala, building.height*self.escala),
            rl.Rectangle(self.x(building.x)*self.escala*self.zoom, self.y(building.y)*self.escala*self.zoom, building.width*self.escala*self.zoom, building.height*self.escala*self.zoom),
            rl.Vector2(0, 0),
            0,
            color
        )

    def start_shake(self, duration, intensity):
        self.shake_timer = duration
        self.shake_intensity = intensity

    def x(self, x):
        return self.pos.x + x + self.shake_offset.x

    def y(self, y):
        return self.pos.y + y + self.shake_offset.y