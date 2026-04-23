import pygame

pygame.init()
pygame.joystick.init()

print("--- Scanner de Controle (Pygame) ---")

# Verifica se há controles
if pygame.joystick.get_count() == 0:
    print("Nenhum controle encontrado!")
    exit()

# Inicializa o primeiro controle encontrado
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Monitorando: {joystick.get_name()}\n")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Detecta Botões (X, Bola, Quadrado, Triângulo, etc)
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Botão Pressionado: {event.button}")

        
        # Detecta Eixos (Analógicos e Gatilhos L2/R2)
        if event.type == pygame.JOYAXISMOTION:
            # Filtro de 'deadzone' para não poluir o console com movimentos minúsculos
            if abs(event.value) > 0.1:
                print(f"Eixo {event.axis} movido para: {event.value:.2f}")

        # Detecta o D-Pad (Setas)
        if event.type == pygame.JOYHATMOTION:
            print(f"D-Pad (Hat): {event.value}")

pygame.quit()