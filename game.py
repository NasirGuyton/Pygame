import pygame
from random import randint

pygame.init()

WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Game")

clock = pygame.time.Clock()



class GameObject(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.surf = pygame.image.load(image).convert_alpha()
        self.x = x
        self.y = y

    def render(self, screen):
        screen.blit(self.surf, (self.x, self.y))



class Apple(GameObject):

    def __init__(self):
        super().__init__(0, 0, "apple.png")

        self.dx = 0
        self.dy = (randint(0, 200) / 100) + 1

        self.reset()

    def move(self):

        self.x += self.dx
        self.y += self.dy

        if self.y > HEIGHT:
            self.reset()

    def reset(self):

        lanes = [93, 218, 343]

        self.x = lanes[randint(0, 2)]
        self.y = -64



class Strawberry(GameObject):

    def __init__(self):
        super().__init__(0, 0, "strawberry.png")

        self.dx = (randint(0, 200) / 100) + 1
        self.dy = 0

        self.reset()

    def move(self):

        self.x += self.dx
        self.y += self.dy

        if self.x > WIDTH:
            self.reset()

    def reset(self):

        self.x = -64
        self.y = randint(50, 400)




apples = [Apple(), Apple(), Apple()]
strawberries = [Strawberry(), Strawberry()]



running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for apple in apples:
        apple.move()
        apple.render(screen)

    for strawberry in strawberries:
        strawberry.move()
        strawberry.render(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()