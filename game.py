import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Challenge 2")

clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    dark_gray = (80, 80, 80)

    radius = 40
    spacing = 120
    start_x = 130
    start_y = 130

    for row in range(3):
        for col in range(3):

            x = start_x + col * spacing
            y = start_y + row * spacing

            pygame.draw.circle(screen, dark_gray, (x, y), radius)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()