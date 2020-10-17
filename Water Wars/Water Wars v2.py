import pygame, sys, time, random

class Platform:
    def __init__(self, screen, color, x, y, height, width):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.height = height
        self.width = width
    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.height, self.width))

class Player:
    def __init__(self, screen, x, y, original_y_velocity, balloon_filename, no_balloon_filename, platforms):
        self.screen = screen
        self.x = x
        self.y = y
        self.original_y_velocity = original_y_velocity
        self.current_y_velocity = original_y_velocity
        self.jumping = False
        self.gravity = -1
        self.balloons = []
        self.no_balloon_image = pygame.image.load(no_balloon_filename)
        self.no_balloon_image = pygame.transform.scale(self.no_balloon_image, (75, 148))
        self.no_balloon_image.set_colorkey((255,255,255))
        self.no_balloon = False
        self.balloon_image = pygame.image.load(balloon_filename)
        self.balloon_image = pygame.transform.scale(self.balloon_image, (83, 144))
        self.balloon_image.set_colorkey((255,255,255))
        self.balloon = True
        self.jump_time = 0
        self.fire_time = 0
        self.firing = False
        self.platforms = platforms
    def draw(self):
        if self.firing == True:
            self.screen.blit(self.no_balloon_image, (self.x, self.y))
            self.balloon= False
            self.no_balloon = True
            if time.time() > self.fire_time + 3:
                self.screen.blit(self.balloon_image, (self.x, self.y))
                self.firing = False
                self.balloon = True
                self.no_balloon = False
        else:
            self.balloon = True
            self.no_balloon = False
            self.screen.blit(self.balloon_image, (self.x, self.y))
    def land_plat_below(self):
        y_below = 384
        for i in range(len(self.platforms)):
            platform = self.platforms[i]
            if self.x >= platform.x - 45 and self.x <= platform.height + platform.x - 40:
                y_below = platform.y - 145
                break
        if self.current_y_velocity < 0 and self.jumping:
            if self.y + 146 >= platform.y:
                self.y = y_below
                self.jumping = False
                self.current_y_velocity = self.original_y_velocity
        if not self.jumping:
            if y_below < self.y:
                y_below = 384
            if y_below > self.y:
                self.move(0, 10)
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    def jump(self):
        if self.jumping == True:
            self.current_y_velocity += self.gravity
            self.move(0, -self.current_y_velocity)
        self.land_plat_below()
    def hit_by(self, balloon):
        balloon_rect = pygame.Rect(self.x, self.y, self.balloon_image.get_width(), self.balloon_image.get_height())
        return balloon_rect.collidepoint(balloon.x, balloon.y)
    def fire(self, direction):
        if self.balloon == True:
            self.balloons.append(Balloon(self.screen, self.x, self.y, direction))
            self.fire_time = time.time()
    def remove_exploded_balloons(self):
        for j in range(len(self.balloons) -1, -1, -1):
            if self.balloons[j].exploded or self.balloons[j].y < 0 or self.balloons[j].y < 1100:
                del self.balloons[j]

class Balloon:
    def __init__(self, screen, x, y, direction):
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load('balloon.png')
        self.image = pygame.transform.scale(self.image, (21, 34))
        self.direction = direction
        self.exploded = False
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y + 20))
    def move(self):
        self.x = self.x + (10 * self.direction)

class Health:
    def __init__(self, screen, player_number, x, y, value):
        self.screen = screen
        self.player_number = player_number
        self.x = x
        self.y = y
        self.value = value
    def draw(self):
        health_text = str(self.player_number) + ' Health: ' + str(self.value)
        font = pygame.font.Font(None, 25)
        font_image = font.render(health_text, True, (0, 0, 0))
        self.screen.blit(font_image, (self.x, self.y))
    def damage(self):
        self.value = self.value - 1000

class Display:
    def __init__(self, screen, color, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
    def draw(self):
        #pygame.draw.rect(screen, color, (x, y, width, height), thickness)
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0)
    def damage(self):
        self.width = self.width - 60

def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("WATER WARS!")
    screen = pygame.display.set_mode((1100, 540))

    # number_of_platforms = 5
    platforms_color = [(180, 79, 57), (170, 69, 47), (180, 79, 57), (170, 69, 47), (190, 89, 67), (190, 89, 67), (20, 180, 20)]
    platforms_x = [110, 530, 900, 690, 0, 320, 0]
    platforms_y = [400, 350, 450, 100, 130, 200, 530]
    platforms_height = [200, 150, 200, 200, 100, 150, 1100]
    platforms_width = [30, 30, 30, 30, 30, 30, 10]
    platforms = []

    for i in range(len(platforms_color)):
        platforms.append(Platform(screen, platforms_color[i], platforms_x[i], platforms_y[i], platforms_height[i],
                                  platforms_width[i]))

    player1 = Player(screen, 75, 384, 25, 'player_balloon.png', 'player_no_balloon.png', platforms)
    player2 = Player(screen, 950, 384, 25, 'player_balloon.png', 'player_no_balloon.png', platforms)

    # health bar
    player1_health = Health(screen, 'Player1', 30, 30, 3000)
    player2_health = Health(screen, 'Player2', 900, 30, 3000)
    player1_display = Display(screen, (20, 180, 20), 30, 7, 180, 20)
    player2_display = Display(screen, (20, 180, 20), 900, 7, 180, 20)

    start_image = pygame.image.load('start_screen.png')
    start_image = pygame.transform.scale(start_image, (1100, 540))
    start_screen = True

    end_player1 = pygame.image.load('player1_win.png')
    end_player1 = pygame.transform.scale(end_player1, (1100, 540))
    end_player2 = pygame.image.load('player2_win.png')
    end_player2 = pygame.transform.scale(end_player2, (1100, 540))

    while True:
        clock.tick(60)
        if start_screen == True:
            screen.blit(start_image, (0, 0))
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE]:
                start_screen = False

        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # One click at a time
            if pressed_keys[pygame.K_e]:
                player1.firing = True
                player1.fire(1)
            if pressed_keys[pygame.K_q]:
                player1.firing = True
                player1.fire(-1)
            if pressed_keys[pygame.K_o]:
                player2.firing = True
                player2.fire(1)
            if pressed_keys[pygame.K_u]:
                player2.firing = True
                player2.fire(-1)
            if pressed_keys[pygame.K_w]:
                player1.jumping = True
            if pressed_keys[pygame.K_i]:
                player2.jumping = True
        # Continuous Motion
        if pressed_keys[pygame.K_d]:
            if player1.x < 1050:
                player1.move(5, 0)
        if pressed_keys[pygame.K_a]:
            if player1.x > -40:
                player1.move(-5, 0)
        if pressed_keys[pygame.K_l]:
            if player2.x < 1050:
                player2.move(5, 0)
        if pressed_keys[pygame.K_j]:
            if player2.x > -40:
                player2.move(-5, 0)

        if start_screen == False:
            screen.fill((135, 206, 250))
            for i in range(len(platforms_color)):
                platforms[i].draw()
            player1.draw()
            player2.draw()
            player1.jump()
            player2.jump()

            for balloon in player1.balloons:
                balloon.draw()
                balloon.move()
                if player2.hit_by(balloon):
                    player2_display.damage()
                    player2_health.damage()
                    player1.remove_exploded_balloons()
                elif balloon.x < 0 or balloon.x > 1100:
                    player1.remove_exploded_balloons()

            for balloon in player2.balloons:
                balloon.draw()
                balloon.move()
                if player1.hit_by(balloon):
                    player1_display.damage()
                    player1_health.damage()
                    player2.remove_exploded_balloons()
                elif balloon.x < 0 or balloon.x > 1100:
                    player2.remove_exploded_balloons()

            player1_health.draw()
            player1_display.draw()
            player2_health.draw()
            player2_display.draw()

            pygame.draw.rect(screen, (0, 0, 0), (30, 7, 180, 20), 3)
            pygame.draw.rect(screen, (0, 0, 0), (900, 7, 180, 20), 3)

            if player1_health.value == 2000:
                player1_display.color = (255, 255, 0)
            if player1_health.value == 1000:
                player1_display.color = (255, 0, 0)
            if player1_health.value == 0:
                screen.blit(end_player2, (0,0))
            if player2_health.value == 2000:
                player2_display.color = (255, 255, 0)
            if player2_health.value == 1000:
                player2_display.color = (255, 0, 0)
            if player2_health.value == 0:
                screen.blit(end_player1, (0,0))

            #   caption1 = font.render()

        pygame.display.update()

main()