import pygame
from pygame.locals import *
import random

pygame.init()

# define game variables
ground_scroll = 0
scroll_speed = 4
clock = pygame.time.Clock()
fps = 60
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  #ms
last_pipe = pygame.time.get_ticks() - pipe_frequency

# create game window
screen_width = 864
screen_height = 936
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# load background
bg = pygame.image.load("assets/bg.png")
ground = pygame.image.load("assets/ground.png")


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"assets/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        # handle the animation
        self.counter += 1
        flat_cooldown = 5

        # only apply gravity when bird is flying
        if flying is True:
            # adding gravity
            self.vel += 0.5
            if self.vel > 8:  # adding a cap for vel
                self.vel = 8
            if self.rect.bottom < 768:  # keeping the bird above ground
                self.rect.y += int(self.vel)

        if game_over is False:

            # rotate through images for animation
            if self.counter > flat_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # adding jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] == 1 and self.clicked is False:
                self.vel = -10
                self.clicked = True
            if keys[pygame.K_SPACE] == 0:
                self.clicked = False

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel*-2)

        else:  # game is over, turn bird 90 degree clockwise (face ground)
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/pipe.png")
        self.rect = self.image.get_rect()

        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        # delete the pipe when it's off the screen
        if self.rect.right < 0:
            self.kill()


flappy = Bird(100, int(screen_height/2))

bird_group = pygame.sprite.Group()
bird_group.add(flappy)


pipe_group = pygame.sprite.Group()


# create game loop
run = True
while run:
    clock.tick(fps)

    # add background image
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # draw the ground
    screen.blit(ground, (ground_scroll, 768))

    # check if bird has hit ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    # check if bird hit pipe and check if bird fies out of screen (top)
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # if game isn't over, keep scrolling the ground
    if game_over is False and flying is True:
        # scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        # create pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)

            last_pipe = time_now

        # only update pipe if game not over
        pipe_group.update()

    # stop loop when user exits out of window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not flying and game_over == False:
                flying = True
    pygame.display.update()

pygame.quit()
