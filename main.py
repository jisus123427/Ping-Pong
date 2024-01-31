import random
import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


pygame.init()

font20 = pygame.font.Font('freesansbold.ttf', 20)

GRAVITY = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
all_sprites = pygame.sprite.Group()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

clock = pygame.time.Clock()
FPS = 30
pause = False


class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.geekRect = pygame.Rect(posx, posy, width, height)
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yline):
        self.posy = self.posy + self.speed * yline

        if self.posy <= 0:
            self.posy = 0

        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        self.geekRect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect


class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.px, self.py = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xLine, self.yLine = 1, -1
        self.ball = pygame.draw.circle(screen, self.color, (self.px, self.py), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(screen, self.color, (self.px, self.py), self.radius)

    def update(self):
        self.px += self.speed * self.xLine
        self.py += self.speed * self.yLine

        if self.py <= 0 or self.py >= HEIGHT:
            self.yLine *= -1

        if self.px <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.px >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.px = WIDTH // 2
        self.py = HEIGHT // 2
        self.xLine *= -1
        self.firstTime = 1

    def hit(self):
        self.xLine *= -1

    def getRect(self):
        return self.ball


screen_rect = (0, 0, WIDTH, HEIGHT)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def switch_pause():
    global pause
    if pause:
        pause = False
    else:
        pause = True


def start_screen():
    intro_text = ["Пинг-Понг", "",
                  "Правила игры",
                  "Игрок 1 - WS, Игрок 2 - Стрелки",
                  "Пауза P"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('Black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def main():
    global event
    all_sprites = pygame.sprite.Group()
    running = True
    gamer1 = Striker(20, 0, 10, 100, 10, GREEN)
    gamer2 = Striker(WIDTH - 30, 0, 10, 100, 10, GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, WHITE)

    listgamer = [gamer1, gamer2]

    score1, score2 = 0, 0
    y1, y2 = 0, 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    switch_pause()
                    print(pause)
                    continue
                if event.key == pygame.K_UP:
                    y2 = -1
                if event.key == pygame.K_DOWN:
                    y2 = 1
                if event.key == pygame.K_w:
                    y1 = -1
                if event.key == pygame.K_s:
                    y1 = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y2 = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    y1 = 0
        if pause:
            continue
        for gamer in listgamer:
            if pygame.Rect.colliderect(ball.getRect(), gamer.getRect()):
                ball.hit()
        gamer1.update(y1)
        gamer2.update(y2)
        point = ball.update()
        if point == -1:
            score1 += 1
        elif point == 1:
            score2 += 1
        if point:
            create_particles((450, 250))
            ball.reset()
        all_sprites.update()
        all_sprites.draw(screen)
        gamer1.display()
        gamer2.display()
        ball.display()

        # Очки игроков
        gamer1.displayScore("Игрок 1 : ",
                            score1, 100, 20, WHITE)
        gamer2.displayScore("Игрок 2 : ",
                            score2, WIDTH - 100, 20, WHITE)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    start_screen()
    main()
    pygame.quit()
