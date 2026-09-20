import pyray as rl
import random
import math

class MeteorEvent:
    def __init__(self, game_manager):
        self.gm = game_manager
        self.active = False
        self.x = 0
        self.y = 0
        self.ticks_passed = 0
        self.max_ticks = 3600  # 1 minuto a 60 FPS
        self.flash_timer = 0
        self.flash_state = None

    def tick(self):
        # Gerencia o clarão de defesa
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer == 30:  # Após meio segundo (30 frames), muda pra vermelho
                self.flash_state = 'red'
            elif self.flash_timer <= 0:
                self.flash_state = None
            return

        if not self.active:
            # 0.1% de chance por tick
            if random.random() < 0.00001:
                self.start_event()
        else:
            self.ticks_passed += 1
            if self.ticks_passed >= self.max_ticks:
                self.trigger_impact()

    def start_event(self):
        self.active = True
        self.ticks_passed = 0
        # Sorteia um local no mapa para o meteoro cair
        self.x = random.randint(0, self.gm.world.width - 1)
        self.y = random.randint(0, self.gm.world.height - 1)

    def trigger_impact(self):
        self.active = False
        
        # Verifica se o centro do meteoro caiu na área de alguma defensive nuke
        if self.is_defended():
            self.flash_timer = 60  # Pelo menos 1 segundo de clarão (60 frames a 60 FPS)
            self.flash_state = 'white'
        else:
            # Destrói todas as construções na área 41x41
            for dy in range(-20, 21):
                for dx in range(-20, 21):
                    wx, wy = self.x + dx, self.y + dy
                    if 0 <= wx < self.gm.world.width and 0 <= wy < self.gm.world.height:
                        self.gm.world.destroy_building(wx, wy)
            
            # Tremer a tela (1 segundo de duração, intensidade 0.5 blocos)
            self.gm.camera.start_shake(60, 0.5)

    def is_defended(self):
        for y in range(self.gm.world.height):
            for x in range(self.gm.world.width):
                b = self.gm.world.map[y][x]
                if b.id == "defensive nuke" and b.parent is None:
                    # Centro da nuke é (+1, +1)
                    nx, ny = b.x + 1, b.y + 1
                    # Checa se o centro do evento (self.x, self.y) está na área 41x41 da nuke
                    if abs(self.x - nx) <= 20 and abs(self.y - ny) <= 20:
                        return True
        return False

    def render(self):
        # Renderiza o clarão se foi defendido
        if self.flash_timer > 0:
            color = rl.WHITE if self.flash_state == 'white' else rl.RED
            # Desenha um clarão sobre a tela inteira
            rl.draw_rectangle(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.fade(color, 0.8))
            return

        # Renderiza o indicador de área ficando mais vermelho
        if self.active:
            cam = self.gm.camera
            intensity = self.ticks_passed / self.max_ticks
            
            # Converte a coordenada do evento para o espaço da tela
            cx = int((cam.pos.x + self.x + 0.5) * cam.escala * cam.zoom)
            cy = int((cam.pos.y + self.y + 0.5) * cam.escala * cam.zoom)
            radius = (20.5 * cam.escala * cam.zoom)
            
            # Círculo vermelho pulsante/crescente
            rl.draw_circle(cx, cy, radius, rl.fade(rl.RED, intensity * 0.7))