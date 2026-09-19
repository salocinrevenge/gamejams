import pyray as rl
from building import Building
from ui_button import UIButton

class SidebarMenu:
    def __init__(self, hud):
        self.hud = hud
        self.width = 200
        self.btn_height = 40
        self.btn_padding = 10
        
        self.current_menu = "main"
        self.scroll_y = 0.0
        self.scroll_speed = 30.0

    def update(self):
        # Verifica rolagem do mouse apenas se o cursor estiver sobre a área do menu
        screen_w = rl.get_screen_width()
        if rl.get_mouse_x() > screen_w - self.width:
            wheel = rl.get_mouse_wheel_move()
            if wheel != 0:
                self.scroll_y += wheel * self.scroll_speed

    def get_items(self):
        if self.current_menu == "main":
            return ["Build", "Move", "Destroy", "Research"]
        elif self.current_menu == "build":
            return ["Back"] + Building.get_buildings_names()
        elif self.current_menu == "research":
            return ["Back", "R1", "R2", "R3"]
        return []

    def render(self):
        screen_w = rl.get_screen_width()
        screen_h = rl.get_screen_height()
        menu_x = screen_w - self.width
        
        # Fundo semi-transparente do menu
        rl.draw_rectangle(int(menu_x), 0, self.width, screen_h, rl.fade(rl.BLACK, 0.2))
        
        items = self.get_items()
        total_height = len(items) * (self.btn_height + self.btn_padding) + self.btn_padding
        
        # Limita o Scroll
        min_scroll = min(0, screen_h - total_height)
        if self.scroll_y > 0:
            self.scroll_y = 0
        elif self.scroll_y < min_scroll:
            self.scroll_y = min_scroll

        # Ativa o Scissor Mode para mascarar o que passa dos limites da tela
        rl.begin_scissor_mode(int(menu_x), 0, self.width, screen_h)
        
        current_y = self.btn_padding + self.scroll_y
        for item in items:
            if current_y + self.btn_height > 0 and current_y < screen_h:
                btn = UIButton(item, menu_x + self.btn_padding, current_y, self.width - (self.btn_padding * 2), self.btn_height)
                if btn.update_and_draw():
                    self.handle_click(item)
                    
            current_y += self.btn_height + self.btn_padding

        rl.end_scissor_mode()

    def handle_click(self, item):
        if item == "Back":
            self.current_menu = "main"
            self.scroll_y = 0
        elif item == "Build":
            self.current_menu = "build"
            self.scroll_y = 0
        elif item == "Research":
            self.current_menu = "research"
            self.scroll_y = 0
        else:
            print(f"Ação executada: {item}")
            if self.current_menu == "build":
                # Informa ao HUD principal que uma construção foi selecionada
                self.hud.selection_action = Building(item, 0, 0)