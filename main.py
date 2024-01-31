import pygame

pygame.init()

font20 = pygame.font.Font('freesansbold.ttf', 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

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


def switch_pause():
    global pause
    if pause:
        pause = False
    else:
        pause = True


def main():
    global event
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
            ball.reset()
        gamer1.display()
        gamer2.display()
        ball.display()

        # Очки игроков
        gamer1.displayScore("Игрок 1 : ",
                            score1, 100, 20, WHITE)
        gamer2.displayScore("Игрок 2 : ",
                            score2, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
