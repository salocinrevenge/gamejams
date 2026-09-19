import pyray as rl

class HUD:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        
        # Configurações do Menu Lateral
        self.menu_width = 200
        self.btn_height = 40
        self.btn_padding = 10
        
        # Estado do Menu e Scroll
        self.current_menu = "main"  # Pode ser "main", "build" ou "research"
        self.scroll_y = 0.0         # Deslocamento vertical da rolagem
        self.scroll_speed = 30.0

    def tick(self):
        # Atualiza o HUD
        
        # Verifica rolagem do mouse apenas se o cursor estiver em cima da área do menu
        screen_w = rl.get_screen_width()
        mouse_x = rl.get_mouse_x()
        
        if mouse_x > screen_w - self.menu_width:
            wheel = rl.get_mouse_wheel_move()
            if wheel != 0:
                self.scroll_y += wheel * self.scroll_speed

    def draw_button(self, text, x, y, width, height):
        """
        Desenha um botão e retorna True se ele foi clicado neste frame.
        """
        rect = rl.Rectangle(x, y, width, height)
        mouse_pos = rl.get_mouse_position()
        
        is_hover = rl.check_collision_point_rec(mouse_pos, rect)
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
        rl.draw_rectangle_rec(rect, bg_color)
        rl.draw_rectangle_lines_ex(rect, 2, rl.DARKGRAY)
        
        # Desenha texto centralizado verticalmente (convertendo str para bytes)
        text_bytes = text.encode('utf-8')
        rl.draw_text(text_bytes, int(x + 15), int(y + height/2 - 10), 20, text_color)
        
        return clicked

    def render(self):
        # Renderiza o HUD Placeholder
        rl.draw_text(b"HUD Placeholder", 10, 10, 20, rl.DARKGRAY)
        rl.draw_rectangle_lines(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.RED)
        
        # ---- MENU LATERAL ----
        screen_w = rl.get_screen_width()
        screen_h = rl.get_screen_height()
        menu_x = screen_w - self.menu_width
        
        # Fundo do menu
        rl.draw_rectangle(int(menu_x), 0, self.menu_width, screen_h, rl.fade(rl.BLACK, 0.8))
        
        # Define quais itens mostrar baseado na aba atual
        items = []
        if self.current_menu == "main":
            items = ["Build", "Move", "Destroy", "Research"]
        elif self.current_menu == "build":
            items = ["Back"] + [f"B{i}" for i in range(1, 21)]
        elif self.current_menu == "research":
            items = ["Back", "R1", "R2", "R3"]

        # Calcula altura total do menu para limitar o scroll
        total_height = len(items) * (self.btn_height + self.btn_padding) + self.btn_padding
        
        # Limita o Scroll para não rolar para o infinito vazio
        min_scroll = min(0, screen_h - total_height)
        if self.scroll_y > 0:
            self.scroll_y = 0
        elif self.scroll_y < min_scroll:
            self.scroll_y = min_scroll

        # Ativa o Scissor Mode para esconder os botões que saírem da tela pelo scroll
        rl.begin_scissor_mode(int(menu_x), 0, self.menu_width, screen_h)
        
        # Desenha a lista de botões
        current_y = self.btn_padding + self.scroll_y
        for item in items:
            # Otimização: Só desenha o botão se ele estiver dentro dos limites visíveis da tela
            if current_y + self.btn_height > 0 and current_y < screen_h:
                
                # Botão é clicado?
                if self.draw_button(item, menu_x + self.btn_padding, current_y, self.menu_width - (self.btn_padding * 2), self.btn_height):
                    self.handle_click(item)
                    
            current_y += self.btn_height + self.btn_padding

        rl.end_scissor_mode()

    def handle_click(self, item):
        """
        Gereciona a lógica de quando um botão específico é clicado
        """
        if item == "Back":
            self.current_menu = "main"
            self.scroll_y = 0  # Reseta o scroll ao trocar de aba
            
        elif item == "Build":
            self.current_menu = "build"
            self.scroll_y = 0
            
        elif item == "Research":
            self.current_menu = "research"
            self.scroll_y = 0
            
        else:
            # Aqui você adiciona a lógica para Move, Destroy, B1..B20 e R1..R3
            print(f"Ação executada: {item}")