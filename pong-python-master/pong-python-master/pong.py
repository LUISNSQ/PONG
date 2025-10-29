import pygame
from controlo import ControloVisao

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()

# Janela
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong - Controlado pela cor vermelha")

# Barra
rect_x, rect_y = 400, 580
ball_x, ball_y = 50, 50
ball_change_x, ball_change_y = 5, 5
score = 0

# CV
cv = ControloVisao()

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Lê posição do cartão vermelho
    pos = cv.detetor()
    if pos is not None:
        rect_x = int(pos * 800) - 50  # centra a barra

    # Bola
    ball_x += ball_change_x
    ball_y += ball_change_y

    if ball_x < 0 or ball_x > 785:
        ball_change_x *= -1
    if ball_y < 0:
        ball_change_y *= -1
    elif rect_y - 15 <= ball_y <= rect_y and rect_x < ball_x < rect_x + 100:
        ball_change_y *= -1
        score += 1
    elif ball_y > 600:
        ball_change_y *= -1
        score = 0

    # Desenhar
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, [ball_x, ball_y, 15, 15])
    pygame.draw.rect(screen, RED, [rect_x, rect_y, 100, 20])

    font = pygame.font.SysFont('Calibri', 20)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, [600, 100])

    pygame.display.flip()
    clock.tick(60)

cv.release()
pygame.quit()
