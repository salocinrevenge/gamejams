import pygame

# Define as cores
preto = (0, 0, 0)
branco = (255, 255, 255)
azul = (0, 0, 255)

# Inicialize Pygame
pygame.init()

# Crie uma tela
tela = pygame.display.set_mode((600, 400))

# Crie um retângulo para o controle deslizante
controle_deslizante = pygame.Rect(200, 200, 200, 20)

# Crie um círculo para o controle deslizante
controle_deslizante_circulo = pygame.Rect(200, 200, 20, 20)

# Defina o valor inicial do controle deslizante
valor_controle_deslizante = 1

# Loop principal
while True:
    # Atualize o estado do controle deslizante
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verifique se o botão do mouse está dentro do controle deslizante
            if controle_deslizante.collidepoint(event.pos):
                # Mova o controle deslizante para a posição do mouse
                controle_deslizante_circulo.centerx = event.pos[0]
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Desenhe a tela
    tela.fill(branco)

    # Desenhe o controle deslizante
    pygame.draw.rect(tela, preto, controle_deslizante)
    pygame.draw.rect(tela, azul, controle_deslizante_circulo)

    # Desenhe o valor do controle deslizante
    tela.blit(
        pygame.font.SysFont("Arial", 20).render(str(valor_controle_deslizante), True, preto),
        (200, 250),
    )

    # Atualize a tela
    pygame.display.update()

    # Atualize o valor do controle deslizante
    valor_controle_deslizante = controle_deslizante_circulo.centerx - controle_deslizante.x
    valor_controle_deslizante = valor_controle_deslizante / controle_deslizante.width
    valor_controle_deslizante = round(valor_controle_deslizante, 2)

