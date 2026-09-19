import pyray as rl

class UIButton:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = rl.Rectangle(x, y, width, height)
        
    def update_and_draw(self):
        """
        Desenha o botão e retorna True se ele foi clicado neste frame.
        """
        mouse_pos = rl.get_mouse_position()
        is_hover = rl.check_collision_point_rec(mouse_pos, self.rect)
        clicked = False
        
        # Cores do botão
        bg_color = rl.LIGHTGRAY
        text_color = rl.DARKGRAY
        
        if is_hover:
            bg_color = rl.GRAY
            text_color = rl.WHITE
            if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                clicked = True
                
        # Desenha fundo e borda
        rl.draw_rectangle_rec(self.rect, bg_color)
        rl.draw_rectangle_lines_ex(self.rect, 2, rl.DARKGRAY)
        
        # Desenha texto centralizado verticalmente
        text_bytes = self.text.encode('utf-8')
        rl.draw_text(
            text_bytes, 
            int(self.rect.x + 15), 
            int(self.rect.y + self.rect.height / 2 - 10), 
            20, 
            text_color
        )
        
        return clicked