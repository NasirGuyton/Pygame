import pygame
from random import randint, choice

pygame.init()

WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Using Groups")

clock = pygame.time.Clock()

lanes = [93, 218, 343]


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.surf = pygame.image.load(image).convert_alpha()
        self.x = float(x)
        self.y = float(y)

    def render(self, screen):
        screen.blit(self.surf, (self.x, self.y))

    def move(self):
        pass


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
        self.x = choice(lanes)
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
        self.y = choice(lanes)


class Player(GameObject):
    def __init__(self):
        super().__init__(0, 0, "player.png")
        self.dx = 0
        self.dy = 0
        self.pos_x = 1
        self.pos_y = 1
        self.reset()

    def update_dx_dy(self):
        self.dx = lanes[self.pos_x]
        self.dy = lanes[self.pos_y]

    def left(self):
        if self.pos_x > 0:
            self.pos_x -= 1
            self.update_dx_dy()

    def right(self):
        if self.pos_x < len(lanes) - 1:
            self.pos_x += 1
            self.update_dx_dy()

    def up(self):
        if self.pos_y > 0:
            self.pos_y -= 1
            self.update_dx_dy()

    def down(self):
        if self.pos_y < len(lanes) - 1:
            self.pos_y += 1
            self.update_dx_dy()

    def move(self):
        self.x -= (self.x - self.dx) * 0.25
        self.y -= (self.y - self.dy) * 0.25

    def reset(self):
        self.x = lanes[self.pos_x]
        self.y = lanes[self.pos_y]
        self.dx = self.x
        self.dy = self.y


player = Player()
apple = Apple()
strawberry = Strawberry()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(apple)
all_sprites.add(strawberry)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        entity.move()
        entity.render(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()