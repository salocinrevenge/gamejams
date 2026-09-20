import pyray as rl
import math
from sidebar_menu import SidebarMenu
from resource_bar import ResourceBar

from infos import resources, buildings, technologies, upgrades_buildings

class HUD:
    def __init__(self, game_manager, resources):
        self.game_manager = game_manager
        self.resources = resources
        self.sidebar = SidebarMenu(self)
        self.resource_bar = ResourceBar(self)
        self.selection_action = None
        
        # Variáveis novas de estado de ferramenta
        self.current_tool = None # Pode ser "move" ou "destroy"
        self.is_moving = False # Para não cobrar custo quando soltar
        self.selected_building = None
        self.show_upgrades = False

    def tick(self):
        self.sidebar.update()
        self.resource_bar.update()
        
        # Se ESC, limpa tudo
        if rl.is_key_pressed(rl.KEY_ESCAPE):
            self.selected_building = None
            self.selection_action = None
            self.current_tool = None
            self.is_moving = False

        # Verifica se o mouse está em cima de alguma UI dos balões flutuantes!
        mouse_pos = rl.get_mouse_position()
        mouse_on_ui = False
        if hasattr(self, 'ui_rects') and self.selected_building:
            for rect in self.ui_rects:
                if rl.check_collision_point_rec(mouse_pos, rect):
                    mouse_on_ui = True
                    break

        # Verifica cliques e ações do mouse fora da sidebar
        if rl.get_mouse_x() < rl.get_screen_width() - self.sidebar.width and not mouse_on_ui:
            cam = self.game_manager.camera
            exact_x = (rl.get_mouse_x() / (cam.escala * cam.zoom)) - cam.pos.x
            exact_y = (rl.get_mouse_y() / (cam.escala * cam.zoom)) - cam.pos.y
            grid_x = math.floor(exact_x)
            grid_y = math.floor(exact_y)

            # Tem uma construção na mão para colocar (Build ou soltando o Move)
            if self.selection_action:
                self.selection_action.x = grid_x
                self.selection_action.y = grid_y

                if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                    # Passa o is_moving pra saber se cobra ou não (free=True)
                    if self.game_manager.world.place_building(self.selection_action, free=self.is_moving):
                        self.selection_action = None
                        self.is_moving = False # Finalizou o move

            # Não tem construção na mão, mas clicou com a ferramenta de Mover ou Destruir selecionada
            elif rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                if 0 <= grid_x < self.game_manager.world.width and 0 <= grid_y < self.game_manager.world.height:
                    if self.current_tool == "destroy":
                        self.game_manager.world.destroy_building(grid_x, grid_y)
                    
                    elif self.current_tool == "move":
                        picked = self.game_manager.world.pick_up_building(grid_x, grid_y)
                        if picked:
                            self.selection_action = picked
                            self.is_moving = True

                    elif not self.current_tool:
                        parent = self.game_manager.world.get_parent_building(grid_x, grid_y)
                        if parent and parent.id != "ground":
                            self.selected_building = parent
                            self.show_upgrades = False
                        else:
                            self.selected_building = None
                            self.show_upgrades = False

    def render(self):
        self.sidebar.render()
        self.resource_bar.render()

        if self.game_manager.paused:
            rl.draw_text("PAUSED".encode(), rl.get_screen_width() // 2 - 50, rl.get_screen_height() // 2 - 10, 30, rl.YELLOW)
        
        # Feedback visual para as ferramentas
        if not self.selection_action and self.current_tool in ["destroy", "move"]:
            if rl.get_mouse_x() < rl.get_screen_width() - self.sidebar.width:
                cam = self.game_manager.camera
                exact_x = (rl.get_mouse_x() / (cam.escala * cam.zoom)) - cam.pos.x
                exact_y = (rl.get_mouse_y() / (cam.escala * cam.zoom)) - cam.pos.y
                
                # Se estiver no mapa, desenha um bloco colorido vermelho (destroy) ou azul (move) no bloco apontado
                if 0 <= math.floor(exact_x) < self.game_manager.world.width and 0 <= math.floor(exact_y) < self.game_manager.world.height:
                    color = rl.RED if self.current_tool == "destroy" else rl.BLUE
                    
                    parent = self.game_manager.world.get_parent_building(math.floor(exact_x), math.floor(exact_y))
                    if parent:
                        # Pinta a construção inteira alvo
                        cam.draw_rect(rl.Rectangle(parent.x, parent.y, parent.width, parent.height), rl.fade(color, 0.5))

        if self.selection_action:
            self.game_manager.camera.draw_building(
                self.game_manager.world.img_sprite_sheet_buildings, 
                self.selection_action, 
                highlight=True
            )

        if hasattr(self, 'selected_building') and self.selected_building:
            self.render_building_balloon()

    def render_building_balloon(self):
        b = self.selected_building
        if not b: return
        
        self.ui_rects = [] # Reinicia a lista de UIs seguras do frame
        
        cam = self.game_manager.camera
        escala = cam.escala * cam.zoom
        bx = (cam.pos.x + b.x) * escala
        by = (cam.pos.y + b.y) * escala
        
        box_w, box_h = 170, 190
        rx, ry = bx, by - box_h - 10
        
        # Adiciona a caixa principal como uma zona segura de clique
        self.ui_rects.append(rl.Rectangle(rx, ry, box_w, box_h))
        
        rl.draw_rectangle(int(rx), int(ry), box_w, box_h, rl.fade(rl.BLACK, 0.9))
        rl.draw_rectangle_lines(int(rx), int(ry), box_w, box_h, rl.WHITE)
        
        rl.draw_text(b.id.upper().encode(), int(rx + 5), int(ry + 5), 18, rl.WHITE)
        
        sprite_sheet = self.game_manager.world.img_sprite_sheet_resources
        
        if b.active_upgrade:
            upg_prod = upgrades_buildings.get(b.id, {}).get(b.active_upgrade, {}).get("produces", {})
            if upg_prod:
                res_name = list(upg_prod.keys())[0]
                idx = resources.get(res_name, 0)
                sy, sx = (idx, 0) if isinstance(idx, int) else (idx[0], idx[1])
                escala_sprite = cam.escala
                rl.draw_texture_pro(
                    sprite_sheet,
                    rl.Rectangle(sx * escala_sprite, sy * escala_sprite, escala_sprite, escala_sprite),
                    rl.Rectangle(rx + box_w - 30, ry + 5, 24, 24),
                    rl.Vector2(0, 0), 0, rl.WHITE
                )
                
        delay = b.info[b.id].get("delay", 1)
        prog = b.timer / delay
        rl.draw_rectangle(int(rx + 5), int(ry + 30), box_w - 10, 10, rl.DARKGRAY)
        rl.draw_rectangle(int(rx + 5), int(ry + 30), int((box_w - 10) * prog), 10, rl.GREEN if b.is_working else rl.RED)
        
        status_txt = "Status: OK" if b.is_working else "Falta Recursos!"
        status_color = rl.GREEN if b.is_working else rl.RED
        rl.draw_text(status_txt.encode(), int(rx + 5), int(ry + 45), 12, status_color)
        
        consumes = dict(b.info[b.id].get("consumes", {}))
        produces = dict(b.info[b.id].get("produces", {}))
        if b.active_upgrade:
            upg = upgrades_buildings.get(b.id, {}).get(b.active_upgrade, {})
            for k, v in upg.get("consumes", {}).items(): consumes[k] = consumes.get(k, 0) + v
            for k, v in upg.get("produces", {}).items(): produces[k] = produces.get(k, 0) + v
            
        cy = ry + 65
        rl.draw_text(b"Consumes:", int(rx + 5), int(cy), 12, rl.WHITE)
        cy += 14
        for res, amt in consumes.items():
            # Aqui fazemos a verificação individual se este item específico está faltando
            is_missing = res in getattr(b, 'missing_resources', [])
            color = rl.RED if is_missing else rl.WHITE
            val = amt if b.is_working else 0
            
            rl.draw_text(f"{res}: {val}/{amt}".encode(), int(rx + 10), int(cy), 12, color)
            cy += 14
            
        cy += 5
        rl.draw_text(b"Produces:", int(rx + 5), int(cy), 12, rl.WHITE)
        cy += 14
        for res, amt in produces.items():
            val = amt if b.is_working else 0
            rl.draw_text(f"{res}: {val}".encode(), int(rx + 10), int(cy), 12, rl.GREEN if b.is_working else rl.DARKGRAY)
            cy += 14
            
        if b.id in upgrades_buildings:
            btn_upg = rl.Rectangle(rx + box_w - 30, ry + box_h - 30, 24, 24)
            rl.draw_rectangle_rec(btn_upg, rl.DARKGREEN)
            rl.draw_text(b"^", int(btn_upg.x + 7), int(btn_upg.y + 7), 20, rl.WHITE)
            
            if rl.check_collision_point_rec(rl.get_mouse_position(), btn_upg) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                self.show_upgrades = not self.show_upgrades
                
            if self.show_upgrades:
                ux = rx + box_w + 5
                uy = ry
                unlocked = self.game_manager.technologies
                
                for upg_name, upg_data in upgrades_buildings[b.id].items():
                    if upg_name in unlocked:
                        upg_rect = rl.Rectangle(ux, uy, 150, 45)
                        
                        # Adiciona o menu do upgrade como zona segura também
                        self.ui_rects.append(upg_rect)
                        
                        rl.draw_rectangle_rec(upg_rect, rl.fade(rl.DARKGRAY, 0.9))
                        rl.draw_rectangle_lines_ex(upg_rect, 1, rl.WHITE if b.active_upgrade != upg_name else rl.GREEN)
                        rl.draw_text(upg_name.encode(), int(ux + 5), int(uy + 5), 12, rl.WHITE)
                        
                        cost_txt = " ".join([f"{k}:{v}" for k,v in upg_data.get("cost", {}).items()])
                        rl.draw_text(cost_txt.encode(), int(ux + 5), int(uy + 25), 10, rl.GOLD)
                        
                        if rl.check_collision_point_rec(rl.get_mouse_position(), upg_rect) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                            if b.active_upgrade != upg_name:
                                can_afford = all(self.resources.get(k, 0) >= v for k, v in upg_data.get("cost", {}).items())
                                if can_afford:
                                    for k, v in upg_data.get("cost", {}).items():
                                        self.resources[k] -= v
                                    b.active_upgrade = upg_name
                                    self.show_upgrades = False
                        uy += 50