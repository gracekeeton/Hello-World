import pygame, sys, time, random

class Player:
    def __init__(self, screen, x, y, purdue_pete):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load(purdue_pete)
        self.image = pygame.transform.scale(self.image, (83, 144))
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
    def move(self, x):
        self.x += x


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1100, 540))
    player = Player(screen, 100, 100, "purdue_pete.jpg")
    ian = pygame.image.load("ian.jpg")
    ian = pygame.transform.scale(ian, (1100, 540))

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a]:
            player.x -= 5
        if pressed_keys[pygame.K_d]:
            player.x += 5

        screen.fill(pygame.Color("White"))

        screen.blit(ian, (0,0))

        player.draw()

        pygame.display.update()

main()
