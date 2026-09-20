import pyray as rl

from infos import resources, resources_flux, upgrades_buildings

class ResourceBar:
    def __init__(self, hud):
        self.hud = hud
        self.width = 200
        self.item_height = 40
        self.padding = 10
        self.scroll_y = 0.0
        self.scroll_speed = 30.0
        
        # Cache para a aba de estatísticas do mouse
        self.hover_cache = {}
        self.hover_timer = 0
        self.hovered_item_last = None

    def update(self):
        # Verifica rolagem do mouse apenas se o cursor estiver na área da barra esquerda
        if rl.get_mouse_x() < self.width:
            wheel = rl.get_mouse_wheel_move()
            if wheel != 0:
                self.scroll_y += wheel * self.scroll_speed

    def render(self):
        screen_h = rl.get_screen_height()
        rl.draw_rectangle(0, 0, self.width, screen_h, rl.fade(rl.BLACK, 0.2))
        
        owned_resources = {k: v for k, v in self.hud.resources.items() if (v > 0 or k in resources_flux)}
        items = list(owned_resources.items())
        
        total_height = len(items) * (self.item_height + self.padding) + self.padding
        min_scroll = min(0, screen_h - total_height)
        if self.scroll_y > 0: self.scroll_y = 0
        elif self.scroll_y < min_scroll: self.scroll_y = min_scroll

        rl.begin_scissor_mode(0, 0, self.width, screen_h)
        
        current_y = self.padding + self.scroll_y
        escala_sprite = self.hud.game_manager.camera.escala
        sprite_sheet = self.hud.game_manager.world.img_sprite_sheet_resources
        
        history = getattr(self.hud.game_manager, 'resources_history', [])
        hovered_res_name = None
        
        for name, count in items:
            if current_y + self.item_height > 0 and current_y < screen_h:
                rect = rl.Rectangle(self.padding, current_y, self.width - (self.padding * 2), self.item_height)
                
                rl.draw_rectangle_rec(rect, rl.LIGHTGRAY)
                rl.draw_rectangle_lines_ex(rect, 1, rl.DARKGRAY)
                
                idx = resources.get(name, 0)
                sy, sx = (idx, 0) if isinstance(idx, int) else (idx[0], idx[1])
                
                if sprite_sheet.id > 0:
                    rl.draw_texture_pro(
                        sprite_sheet, rl.Rectangle(sx * escala_sprite, sy * escala_sprite, escala_sprite, escala_sprite),
                        rl.Rectangle(rect.x + 4, rect.y + 4, 32, 32), rl.Vector2(0, 0), 0, rl.WHITE
                    )
                
                storage = self.hud.game_manager.resources_storage.get(name, 0)
                text_str = f": {int(count)} / {storage}"
                rl.draw_text(text_str.encode('utf-8'), int(rect.x + 42), int(rect.y + 10), 16, rl.DARKGRAY)
                
                # --- Setas (Tendência no último minuto) ---
                if history:
                    past_count = history[0].get(name, 0)
                    if count > past_count:
                        # Triângulo Verde apontando para cima
                        rl.draw_triangle(
                            rl.Vector2(rect.x + rect.width - 20, rect.y + 10),
                            rl.Vector2(rect.x + rect.width - 25, rect.y + 20),
                            rl.Vector2(rect.x + rect.width - 15, rect.y + 20),
                            rl.GREEN
                        )
                    elif count < past_count:
                        # Triângulo Vermelho apontando para baixo
                        rl.draw_triangle(
                            rl.Vector2(rect.x + rect.width - 25, rect.y + 10),
                            rl.Vector2(rect.x + rect.width - 20, rect.y + 20),
                            rl.Vector2(rect.x + rect.width - 15, rect.y + 10),
                            rl.RED
                        )

                # Verifica o mouse em cima da caixa de recurso
                if rl.check_collision_point_rec(rl.get_mouse_position(), rect):
                    hovered_res_name = name
                
            current_y += self.item_height + self.padding

        rl.end_scissor_mode()

        # --- Desenhando O Tooltip Flutuante ---
        if hovered_res_name:
            if hovered_res_name != self.hovered_item_last:
                self.hovered_item_last = hovered_res_name
                self.hover_cache[hovered_res_name] = self._get_resource_stats(hovered_res_name)
                self.hover_timer = 0
            
            # Recalcula a cada 1 segundo (60 frames) para não travar o jogo
            self.hover_timer += 1
            if self.hover_timer > 60:
                self.hover_timer = 0
                self.hover_cache[hovered_res_name] = self._get_resource_stats(hovered_res_name)
                
            prods, cons = self.hover_cache.get(hovered_res_name, ({}, {}))
            
            # Formata a janelinha
            tt_w = 230
            lines = 2 + len(prods) + (1 if prods else 0) + len(cons) + (1 if cons else 0)
            tt_h = lines * 20 + 10
            
            mx = rl.get_mouse_x() + 15
            my = rl.get_mouse_y()
            if my + tt_h > screen_h: my = screen_h - tt_h - 10 # Evita vazar da tela
                
            rl.draw_rectangle(int(mx), int(my), tt_w, tt_h, rl.fade(rl.BLACK, 0.9))
            rl.draw_rectangle_lines(int(mx), int(my), tt_w, tt_h, rl.WHITE)
            
            cy = my + 10
            rl.draw_text(f"Resource: {hovered_res_name.upper()}".encode(), int(mx + 10), int(cy), 16, rl.GOLD)
            cy += 25
            
            if prods:
                rl.draw_text(b"Produced by:", int(mx + 10), int(cy), 14, rl.GREEN)
                cy += 20
                for b_id, amt in prods.items():
                    rl.draw_text(f"- {b_id}: {amt}".encode(), int(mx + 20), int(cy), 14, rl.WHITE)
                    cy += 20
            
            if cons:
                rl.draw_text(b"Consumed by:", int(mx + 10), int(cy), 14, rl.RED)
                cy += 20
                for b_id, amt in cons.items():
                    rl.draw_text(f"- {b_id}: {amt}".encode(), int(mx + 20), int(cy), 14, rl.WHITE)
                    cy += 20
        else:
            self.hovered_item_last = None

    def _get_resource_stats(self, res_name):
        producers = {}
        consumers = {}
        world = self.hud.game_manager.world
        for y in range(world.height):
            for x in range(world.width):
                b = world.map[y][x]
                if b.id != "ground" and b.parent is None and b.is_working:
                    consumes = dict(b.info[b.id].get("consumes", {}))
                    produces = dict(b.info[b.id].get("produces", {}))
                    
                    if getattr(b, 'active_upgrade', None):
                        upg = upgrades_buildings.get(b.id, {}).get(b.active_upgrade, {})
                        for k, v in upg.get("consumes", {}).items(): consumes[k] = consumes.get(k, 0) + v
                        for k, v in upg.get("produces", {}).items(): produces[k] = produces.get(k, 0) + v
                    
                    if res_name in produces:
                        producers[b.id] = producers.get(b.id, 0) + produces[res_name]
                    if res_name in consumes:
                        consumers[b.id] = consumers.get(b.id, 0) + consumes[res_name]
        return producers, consumers