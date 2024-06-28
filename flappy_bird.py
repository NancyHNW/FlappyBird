import pygame
from pygame.locals import *
import random

pygame.init()

# define game variables
ground_scroll = 0
scroll_speed = 4
clock = pygame.time.Clock()
fps = 60

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

    def update(self):
        # handle the animation
        self.counter += 1
        flat_cooldown = 5

        if self.counter > flat_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


flappy = Bird(100, int(screen_height/2))

bird_group = pygame.sprite.Group()
bird_group.add(flappy)


# create game loop
run = True
while run:
    clock.tick(fps)

    # add background image
    screen.blit(bg, (0, 0))

    # scroll background
    screen.blit(ground, (ground_scroll, 768))
    ground_scroll -= scroll_speed

    bird_group.draw(screen)
    bird_group.update()

    if abs(ground_scroll) > 35:
        ground_scroll = 0

    # stop loop when user exits out of window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
