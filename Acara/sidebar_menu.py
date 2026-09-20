import pyray as rl
from building import Building
from ui_button import UIButton
from infos import resources, buildings, technologies

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
            return ["Build", "Move", "Destroy", "Research", "Save", "Load" ,"Pause"]
            
        elif self.current_menu == "build":
            items = ["Back"]
            # Pega as tecnologias já desbloqueadas pelo jogador
            unlocked = self.hud.game_manager.technologies
            
            # Percorre todas as construções disponíveis no arquivo infos
            for b_name, b_data in buildings.items():
                if b_name == "ground":  # Não queremos mostrar o chão na loja
                    continue
                
                # Verifica se o jogador tem todas as tecnologias necessárias para essa construção
                reqs = b_data.get("technology", [])
                if all(req in unlocked for req in reqs):
                    items.append(b_name)
                    
            return items
            
        elif self.current_menu == "research":
            items = ["Back"]
            unlocked = self.hud.game_manager.technologies
            
            for tech_name, tech_data in technologies.items():
                # 1. Se já tem a tecnologia, não mostra
                if tech_name in unlocked:
                    continue
                
                # 2. Verifica se todas as dependências foram cumpridas
                reqs = tech_data.get("technology", [])
                if all(req in unlocked for req in reqs):
                    items.append(tech_name)
                    
            return items
            
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
        hovered_item = None
        for item in items:
            if current_y + self.btn_height > 0 and current_y < screen_h:
                btn = UIButton(item, menu_x + self.btn_padding, current_y, self.width - (self.btn_padding * 2), self.btn_height)
                clicked, is_hover = btn.update_and_draw()
                if is_hover and item != "Back":
                    if self.current_menu in ["build", "research"]:
                        hovered_item = item
                if clicked:
                    self.handle_click(item)

            current_y += self.btn_height + self.btn_padding

        rl.end_scissor_mode()

        if hovered_item:
            self.render_info_panel(hovered_item, screen_h)

    def render_info_panel(self, hovered_item, screen_h):
        # Decide de onde puxar a informação do painel
        if self.current_menu == "build":
            info = buildings.get(hovered_item, {})
        elif self.current_menu == "research":
            info = technologies.get(hovered_item, {})
        else:
            return
            
        mouse_pos = rl.get_mouse_position()
        
        # Configurações visuais do painel
        tt_width = 160
        padding = 10
        line_height = 24
        icon_size = 20
        
        # Mapeia as seções do dicionário para títulos legíveis
        sections = [
            ("Cost", info.get("cost", {})),
            ("Consumes", info.get("consumes", {})),
            ("Generates", info.get("produces", {})),
            ("Storage", info.get("storage", {})) # Adicionado caso a construção guarde algo
        ]
        
        # Calcula a altura necessária para o painel dependendo de quantas seções ele tem
        total_lines = sum(1 + len(data) for title, data in sections if data)
        tt_height = (padding * 2) + (total_lines * line_height)
        
        # Posiciona à esquerda do mouse (para não sair da tela) e ajusta a altura
        tt_x = mouse_pos.x - tt_width - 15
        tt_y = mouse_pos.y
        if tt_y + tt_height > screen_h:
            tt_y = screen_h - tt_height - 10
            
        # Desenha o fundo e a borda do painel
        tt_rect = rl.Rectangle(tt_x, tt_y, tt_width, tt_height)
        rl.draw_rectangle_rec(tt_rect, rl.fade(rl.BLACK, 0.9))
        rl.draw_rectangle_lines_ex(tt_rect, 1, rl.DARKGRAY)
        
        current_y = tt_y + padding
        sprite_sheet = self.hud.game_manager.world.img_sprite_sheet_resources
        escala_sprite = self.hud.game_manager.camera.escala
        
        # Renderiza as categorias
        for title, data in sections:
            if not data:
                continue
                
            # Título da seção (Cost, Consumes...)
            rl.draw_text(title.encode('utf-8'), int(tt_x + padding), int(current_y), 16, rl.GOLD)
            current_y += line_height
            
            # Itens da seção
            for res_name, amount in data.items():
                # Coleta a posição do sprite (mesma lógica da barra de recursos)
                idx = resources.get(res_name, 0)
                sy = idx if isinstance(idx, int) else idx[0]
                sx = 0 if isinstance(idx, int) else idx[1]
                
                # Desenha o ícone
                if sprite_sheet.id > 0:
                    rl.draw_texture_pro(
                        sprite_sheet,
                        rl.Rectangle(sx * escala_sprite, sy * escala_sprite, escala_sprite, escala_sprite),
                        rl.Rectangle(tt_x + padding + 5, current_y, icon_size, icon_size),
                        rl.Vector2(0, 0),
                        0,
                        rl.WHITE
                    )
                
                
                # Verifica se tem essa quantidade de recurso
                has_enough = self.hud.resources.get(res_name, 0) >= amount
                text_color = rl.RAYWHITE if (has_enough or title != "Cost") else rl.RED

                #Desenha a quantidade e nome do recurso
                # text = f"{amount} {res_name.strip()}"
                text = f"x{amount}"
                rl.draw_text(
                    text.encode('utf-8'), 
                    int(tt_x + padding + icon_size + 10), 
                    int(current_y + 2), 
                    16, 
                    text_color
                )
                
                current_y += line_height

            
    def handle_click(self, item):
        # Limpa seleções passadas ao trocar de menu ou de botão
        self.hud.selection_action = None
        self.hud.current_tool = None
        self.hud.is_moving = False

        if item == "Back":
            self.current_menu = "main"
            self.scroll_y = 0
        elif item == "Build":
            self.current_menu = "build"
            self.scroll_y = 0
        elif item == "Move":
            self.hud.current_tool = "move"
        elif item == "Destroy":
            self.hud.current_tool = "destroy"
        elif item == "Research":
            self.current_menu = "research"
            self.scroll_y = 0
        elif item == "Save":
            self.hud.game_manager.save_game()
        elif item == "Load":
            self.hud.game_manager.load_game()
        elif item == "Pause":
            self.hud.game_manager.pause_toggle()
        else:
            if self.current_menu == "build":
                self.hud.selection_action = Building(item, 0, 0)
            elif self.current_menu == "research":
                tech_info = technologies.get(item, {})
                costs = tech_info.get("cost", {})
                
                # Verifica se o jogador tem recursos suficientes
                can_afford = True
                for res_name, amount in costs.items():
                    if self.hud.resources.get(res_name, 0) < amount:
                        can_afford = False
                        break
                
                if can_afford:
                    # Desconta os recursos do inventário
                    for res_name, amount in costs.items():
                        self.hud.resources[res_name] -= amount
                    
                    # Adiciona a tecnologia ao Set do GameManager (desbloqueia)
                    self.hud.game_manager.technologies.add(item)
                    print(f"Tecnologia '{item}' pesquisada com sucesso!")