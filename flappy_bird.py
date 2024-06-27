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
bg = pygame.image.load("bg.png")
ground = pygame.image.load("ground.png")

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

# create game loop
run = True
while run:
    clock.tick(fps)

    # add background image
    screen.blit(bg, (0, 0))

    # scroll background
    screen.blit(ground, (ground_scroll, 768))
    ground_scroll -= scroll_speed

    if abs(ground_scroll) > 35:
        ground_scroll = 0

    # stop loop when user exits out of window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
