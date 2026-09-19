import pyray as rl
from resources import Resources

class ResourceBar:
    def __init__(self, hud):
        self.hud = hud
        self.width = 120
        self.item_height = 40
        self.padding = 10
        self.scroll_y = 0.0
        self.scroll_speed = 30.0

    def update(self):
        # Verifica rolagem do mouse apenas se o cursor estiver na área da barra esquerda
        if rl.get_mouse_x() < self.width:
            wheel = rl.get_mouse_wheel_move()
            if wheel != 0:
                self.scroll_y += wheel * self.scroll_speed

    def render(self):
        screen_h = rl.get_screen_height()
        
        # Fundo semi-transparente da barra lateral esquerda
        rl.draw_rectangle(0, 0, self.width, screen_h, rl.fade(rl.BLACK, 0.2))
        
        # Filtra apenas os recursos que possuem quantidade maior que 0
        owned_resources = {k: v for k, v in self.hud.resources.items() if v > 0}
        items = list(owned_resources.items()) # Lista de tuplas: (nome, quantidade)
        
        total_height = len(items) * (self.item_height + self.padding) + self.padding
        
        # Limita o Scroll para não passar do topo nem do fim
        min_scroll = min(0, screen_h - total_height)
        if self.scroll_y > 0:
            self.scroll_y = 0
        elif self.scroll_y < min_scroll:
            self.scroll_y = min_scroll

        # Ativa o Scissor Mode na esquerda para esconder itens fora da tela
        rl.begin_scissor_mode(0, 0, self.width, screen_h)
        
        current_y = self.padding + self.scroll_y
        escala_sprite = self.hud.game_manager.camera.escala
        sprite_sheet = self.hud.game_manager.world.img_sprite_sheet_resources
        
        for name, count in items:
            if current_y + self.item_height > 0 and current_y < screen_h:
                rect = rl.Rectangle(self.padding, current_y, self.width - (self.padding * 2), self.item_height)
                
                # Desenha fundo e borda do item de recurso
                rl.draw_rectangle_rec(rect, rl.LIGHTGRAY)
                rl.draw_rectangle_lines_ex(rect, 1, rl.DARKGRAY)
                
                # Pega a posição do ícone na spritesheet com base na classe Resources
                idx = Resources.info.get(name, 0)
                sy = idx if isinstance(idx, int) else idx[0]
                sx = 0 if isinstance(idx, int) else idx[1]
                
                # Desenha o ícone do recurso redimensionado para caber no item (32x32)
                if sprite_sheet.id > 0:
                    rl.draw_texture_pro(
                        sprite_sheet,
                        rl.Rectangle(sx * escala_sprite, sy * escala_sprite, escala_sprite, escala_sprite),
                        rl.Rectangle(rect.x + 4, rect.y + 4, 32, 32),
                        rl.Vector2(0, 0),
                        0,
                        rl.WHITE
                    )
                
                # Desenha o texto (Nome do recurso + Quantidade)
                text_str = f": {count}"
                rl.draw_text(text_str.encode('utf-8'), int(rect.x + 42), int(rect.y + 10), 16, rl.DARKGRAY)
                
            current_y += self.item_height + self.padding

        rl.end_scissor_mode()