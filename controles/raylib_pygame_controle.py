from pyray import *
import pygame
import sys

# --- Inicialização do Pygame (Apenas para Input) ---
pygame.init()
pygame.joystick.init()

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Pygame detectou: {joystick.get_name()}")
else:
    print("Nenhum controle detectado pelo Pygame!")

# --- Inicialização da Raylib (Para Gráficos) ---
init_window(500, 400, "Raylib + Pygame Input Hybrid")
set_target_fps(60)

while not window_should_close():
    # 1. ATUALIZAÇÃO DE INPUT (Pygame)
    # É crucial chamar pump() para o Pygame processar os sinais do hardware
    pygame.event.pump()
    
    # 2. DESENHO (Raylib)
    begin_drawing()
    clear_background(RAYWHITE)
    
    if joystick:
        draw_text(f"Controle: {joystick.get_name()}", 10, 10, 20, DARKGRAY)
        draw_text("Aperte botões para testar:", 10, 40, 20, MAROON)

        # Escaneia Botões
        for i in range(joystick.get_numbuttons()):
            if joystick.get_button(i):
                draw_text(f"Botão {i} pressionado!", 10, 80, 30, RED)
                # print(f"Botão {i}") # Opcional: ver no console
        
        # Escaneia Eixos (Analógicos)
        for i in range(joystick.get_numaxes()):
            val = joystick.get_axis(i)
            if abs(val) > 0.1: # Deadzone simples
                draw_text(f"Eixo {i}: {val:.2f}", 10, 120 + (i * 25), 20, BLUE)

        # Escaneia D-Pad (Hat)
        for i in range(joystick.get_numhats()):
            hat = joystick.get_hat(i)
            if hat != (0, 0):
                draw_text(f"D-Pad {i}: {hat}", 10, 300, 20, DARKGREEN)
    else:
        draw_text("Nenhum controle conectado!", 10, 10, 20, RED)
        
    end_drawing()

# --- Finalização ---
close_window()
pygame.quit()
sys.exit()