import pygame
from random import randint, choice

pygame.init()

WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collisions")

clock = pygame.time.Clock()

lanes = [93, 218, 343]
SPEED_BOOST = 0.15


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.surf = pygame.image.load(image).convert_alpha()
        self.x = float(x)
        self.y = float(y)
        self.rect = self.surf.get_rect()

    def render(self, screen):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        screen.blit(self.surf, (self.x, self.y))

    def move(self):
        pass

    def increase_speed(self, amount):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__(0, 0, "apple.png")
        self.dx = 0
        self.dy = 0
        self.reset()

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.dy > 0 and self.y > HEIGHT:
            self.reset()
        elif self.dy < 0 and self.y < -64:
            self.reset()

    def reset(self):
        self.x = choice(lanes)
        direction = choice(["down", "up"])

        if direction == "down":
            self.y = -64
            self.dx = 0
            self.dy = (randint(0, 200) / 100) + 1
        else:
            self.y = HEIGHT
            self.dx = 0
            self.dy = -((randint(0, 200) / 100) + 1)

    def increase_speed(self, amount):
        if self.dy > 0:
            self.dy += amount
        else:
            self.dy -= amount


class Strawberry(GameObject):
    def __init__(self):
        super().__init__(0, 0, "strawberry.png")
        self.dx = 0
        self.dy = 0
        self.reset()

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.dx > 0 and self.x > WIDTH:
            self.reset()
        elif self.dx < 0 and self.x < -64:
            self.reset()

    def reset(self):
        self.y = choice(lanes)
        direction = choice(["right", "left"])

        if direction == "right":
            self.x = -64
            self.dx = (randint(0, 200) / 100) + 1
            self.dy = 0
        else:
            self.x = WIDTH
            self.dx = -((randint(0, 200) / 100) + 1)
            self.dy = 0

    def increase_speed(self, amount):
        if self.dx > 0:
            self.dx += amount
        else:
            self.dx -= amount


class Bomb(GameObject):
    def __init__(self):
        super().__init__(0, 0, "bomb.png")
        self.dx = 0
        self.dy = 0
        self.reset()

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.dx > 0 and self.x > WIDTH:
            self.reset()
        elif self.dx < 0 and self.x < -64:
            self.reset()
        elif self.dy > 0 and self.y > HEIGHT:
            self.reset()
        elif self.dy < 0 and self.y < -64:
            self.reset()

    def reset(self):
        direction = choice(["down", "up", "right", "left"])
        speed = (randint(0, 200) / 100) + 1

        if direction == "down":
            self.x = choice(lanes)
            self.y = -64
            self.dx = 0
            self.dy = speed

        elif direction == "up":
            self.x = choice(lanes)
            self.y = HEIGHT
            self.dx = 0
            self.dy = -speed

        elif direction == "right":
            self.x = -64
            self.y = choice(lanes)
            self.dx = speed
            self.dy = 0

        elif direction == "left":
            self.x = WIDTH
            self.y = choice(lanes)
            self.dx = -speed
            self.dy = 0

    def increase_speed(self, amount):
        if self.dx > 0:
            self.dx += amount
        elif self.dx < 0:
            self.dx -= amount
        elif self.dy > 0:
            self.dy += amount
        elif self.dy < 0:
            self.dy -= amount


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
        self.pos_x = 1
        self.pos_y = 1
        self.x = lanes[self.pos_x]
        self.y = lanes[self.pos_y]
        self.dx = self.x
        self.dy = self.y


def reset_game(player, fruits, bomb):
    player.reset()
    for fruit in fruits:
        fruit.reset()
    bomb.reset()


def speed_up_entities(group, amount):
    for entity in group:
        entity.increase_speed(amount)


player = Player()

apple = Apple()
strawberry = Strawberry()
bomb = Bomb()

all_sprites = pygame.sprite.Group()
fruit_sprites = pygame.sprite.Group()
danger_sprites = pygame.sprite.Group()

all_sprites.add(player, apple, strawberry, bomb)
fruit_sprites.add(apple, strawberry)
danger_sprites.add(bomb)

score = 0
font = pygame.font.SysFont(None, 36)

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

    fruit = pygame.sprite.spritecollideany(player, fruit_sprites)
    if fruit:
        fruit.reset()
        score += 1
        speed_up_entities(fruit_sprites, SPEED_BOOST)
        speed_up_entities(danger_sprites, SPEED_BOOST)

    if pygame.sprite.collide_rect(player, bomb):
        reset_game(player, fruit_sprites, bomb)
        score = 0

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()