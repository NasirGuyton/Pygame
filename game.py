import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Challenge 2 - Apples & Strawberries")

clock = pygame.time.Clock()


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.surf = pygame.image.load(image_path).convert_alpha()
        self.x = x
        self.y = y

    def render(self, screen):
        screen.blit(self.surf, (self.x, self.y))


# Grid layout from the screenshot: Apple, Strawberry, Apple / Strawberry, Apple, Strawberry / Apple, Strawberry, Apple
layout = [
    ["apple.png", "strawberry.png", "apple.png"],
    ["strawberry.png", "apple.png", "strawberry.png"],
    ["apple.png", "strawberry.png", "apple.png"],
]

# These values make a centered 3x3 grid for 64x64 sprites in a 500x500 window
start_x, start_y = 93, 68      # top-left sprite position
spacing_x, spacing_y = 125, 150 # distance between sprite top-left corners

objects = []
for row in range(3):
    for col in range(3):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        objects.append(GameObject(x, y, layout[row][col]))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for obj in objects:
        obj.render(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()