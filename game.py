import pygame
from random import randint

pygame.init()

WIDTH = 500
HEIGHT = 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Handling Events")

CLOCK = pygame.time.Clock()

LANES = [93, 218, 343]

ROWS = [93, 218, 343]


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.surf = pygame.image.load(image).convert_alpha()
        self.x = float(x)
        self.y = float(y)

    def render(self, screen):
        screen.blit(self.surf, (self.x, self.y))

    @property
    def width(self):
        return self.surf.get_width()

    @property
    def height(self):
        return self.surf.get_height()


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
        self.x = LANES[randint(0, 2)]
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
        self.y = ROWS[randint(0, 2)]


class Player(GameObject):
    def __init__(self):
        super().__init__(0, 0, "player.png")
        self.col = 1  # middle lane
        self.row = 1  # middle row
        self.dx = 0
        self.dy = 0
        self.reset()

    def left(self):
        if self.col > 0:
            self.col -= 1
            self.dx = LANES[self.col]

    def right(self):
        if self.col < 2:
            self.col += 1
            self.dx = LANES[self.col]

    def up(self):
        if self.row > 0:
            self.row -= 1
            self.dy = ROWS[self.row]

    def down(self):
        if self.row < 2:
            self.row += 1
            self.dy = ROWS[self.row]

    def move(self):
        # easing movement toward target
        self.x -= (self.x - self.dx) * 0.25
        self.y -= (self.y - self.dy) * 0.25

        # extra protection so player never goes off screen
        max_x = WIDTH - self.width
        max_y = HEIGHT - self.height

        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))
        self.dx = max(0, min(self.dx, max_x))
        self.dy = max(0, min(self.dy, max_y))

    def reset(self):
        self.col = 1
        self.row = 1
        self.x = LANES[self.col]
        self.y = ROWS[self.row]
        self.dx = self.x
        self.dy = self.y


apples = [Apple(), Apple(), Apple()]
strawberries = [Strawberry(), Strawberry()]
player = Player()

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

    SCREEN.fill((0, 0, 0))

    for apple in apples:
        apple.move()
        apple.render(SCREEN)

    for strawberry in strawberries:
        strawberry.move()
        strawberry.render(SCREEN)

    player.move()
    player.render(SCREEN)

    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()