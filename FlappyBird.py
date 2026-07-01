#INSTALAR O PYGAME, no terminal
#pip install pygame-ce

import pygame
import sys
import random

# inicializa o pygame
pygame.init()

# Definindo o tamanho da janela
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome da janela
pygame.display.set_caption('Flappy Bird ORT')

# Relógio para controlar o FPS do jogo
clock = pygame.time.Clock()

# Propriedades do personagem
posicao_inicial_x = 50
posicao_inicial_y = 300

posicao_x = posicao_inicial_x
posicao_y = posicao_inicial_y
tamanho = 30
velocidade = 0
gravidade = 0.5
pulo = -8

# Propriedades do cano
cano_largura = 60
cano_distancia = 150
cano_velocidade = 3
canos = []

# Propriedades do jogo
game_over = False
placar = 0
recorde = 0

fonte_placar = pygame.font.SysFont('Arial', 32)

# Funcao para criar um novo cano
def criar_cano():
    cano_superior = random.randint(100, 350) # Ajustado para o cano de baixo não sumir no chão
    cano_inferior = cano_superior + cano_distancia

    return {
        'x': WIDTH,
        'cano_superior': cano_superior,
        'cano_inferior': cano_inferior,
        'passou': False
    }

# Cria apenas um cano antes Loop principal
canos.append(criar_cano())

# Parametros do botão reiniciar
fonte_botao = pygame.font.SysFont('Arial', 30)
botao_desenho = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50) # Ajustado o tamanho para ficar centralizado e bonito
botao_texto = fonte_botao.render('Reiniciar', True, (255, 255, 255))
botao_rect = botao_texto.get_rect(center=botao_desenho.center)

def resetar_jogo():
    global placar, game_over, posicao_x, posicao_y, velocidade
    canos.clear()
    canos.append(criar_cano())
    velocidade = 0
    game_over = False
    posicao_x = posicao_inicial_x
    posicao_y = posicao_inicial_y
    placar = 0

# Game Loop
while True:
    # 1. Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Só permite pular se o jogo NÃO estiver em Game Over
        if not game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                velocidade = pulo
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                velocidade = pulo
        else:
            # Se estiver em Game Over, o clique serve APENAS para o botão
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botao_desenho.collidepoint(event.pos):
                    resetar_jogo()
    
    if not game_over:
        # 2. Controle de estados
        # Fisica do passaro
        velocidade += gravidade
        posicao_y += velocidade

        # Controle do cano
        for cano in canos:
            cano['x'] -= cano_velocidade

            # Controle Placar
            if not cano['passou'] and cano['x'] + cano_largura < posicao_x:
                placar += 1
                cano['passou'] = True
                if placar > recorde: # Atualiza o recorde em tempo real
                    recorde = placar

        # Adiciona novos canos
        if len(canos) > 0 and canos[-1]['x'] < WIDTH - 200:
            canos.append(criar_cano())
        
        # Remove os canos que já sairam da tela
        if len(canos) > 0 and canos[0]['x'] < -cano_largura:
            canos.pop(0)

        # Condição de derrota: Bateu no teto ou no chão
        if posicao_y <= 0 or posicao_y + tamanho > HEIGHT:
            game_over = True 

    # 3. Desenhos (Deixados fora do "if not game_over" para a tela não congelar ou sumir no game over)
    screen.fill((135, 206, 235))
    
    # Desenho o passaro
    passaro = pygame.Rect(posicao_x, posicao_y, tamanho, tamanho)
    pygame.draw.rect(screen, (255, 230, 0), passaro)

    # Desenho do cano
    for cano in canos:
        cano_superior = pygame.Rect(cano['x'], 0, cano_largura, cano['cano_superior'])
        pygame.draw.rect(screen, (34, 139, 34), cano_superior)

        cano_inferior = pygame.Rect(cano['x'], cano['cano_inferior'], cano_largura, HEIGHT - cano['cano_inferior'])
        pygame.draw.rect(screen, (34, 139, 34), cano_inferior)

        # Colisão com o cano
        if passaro.colliderect(cano_superior) or passaro.colliderect(cano_inferior):
            game_over = True
    
    # Desenhando o placar
    placar_texto = fonte_placar.render(f'Pontos: {placar}', True, (0, 0, 0))
    screen.blit(placar_texto, (10, 10))

    recorde_texto = fonte_placar.render(f'Recorde: {recorde}', True, (0, 0, 0))
    screen.blit(recorde_texto, (WIDTH - 160, 10))

    if game_over:
        # Desenha o retângulo maior de fundo e depois o texto centralizado nele
        pygame.draw.rect(screen, (200, 0, 0), botao_desenho, border_radius=10)  
        screen.blit(botao_texto, botao_rect)

    # 4. Atualização da tela
    pygame.display.flip() 
    clock.tick(60)