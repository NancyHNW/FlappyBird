import pygame
from pygame.locals import *
import random
from classes import Bird, Pipe, Button
from functions import draw_text, reset_game

pygame.init()

# Define game variables
ground_scroll = 0
scroll_speed = 4
clock = pygame.time.Clock()
fps = 60
flying = False
game_over = False
game_started = False
pipe_gap = 150
pipe_frequency = 1500  # ms
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# Create game window
screen_width = 864
screen_height = 936
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Define game font
font = pygame.font.SysFont("Bauhaus 93", 60)
start_font = pygame.font.SysFont("Victor Mono", 50)

# Define colours
white = (255, 255, 255)
black = (0, 0, 0)

# Load images
bg = pygame.image.load("assets/bg.png")
ground = pygame.image.load("assets/ground.png")

restart = pygame.image.load("assets/restart.png")
restart_img = pygame.transform.scale(restart, (restart.get_width() * 2, restart.get_height() * 2))
hover = pygame.image.load("assets/hover_restart.png")
hover_img = pygame.transform.scale(hover, (hover.get_width() * 2, hover.get_height() * 2))

menu = pygame.image.load("assets/menu.png")
menu_img = pygame.transform.scale(menu, (menu.get_width() * 1.4, menu.get_height() * 1.4))
hover_menu = pygame.image.load("assets/hover_menu.png")
hover_menu_img = pygame.transform.scale(hover_menu, (hover_menu.get_width() * 1.4, hover_menu.get_height() * 1.4))

flappy = Bird(100, int(screen_height / 2))

bird_group = pygame.sprite.Group()
bird_group.add(flappy)

pipe_group = pygame.sprite.Group()

button = Button(screen_width // 2 - 120, screen_height // 2 - 100, restart_img, hover_img)
menu_btn = Button(40, 30, menu_img, hover_menu_img)

# Create game loop
run = True
while run:
    clock.tick(fps)

    # Add background image
    screen.blit(bg, (0, 0))

    if not game_started:
        draw_text(screen, "Press SPACE to start", start_font, white, int(screen_width / 2)-170, int(screen_height / 2)-160)
        menu_click = menu_btn.draw(screen)


    bird_group.draw(screen)
    bird_group.update(flying, game_over)
    pipe_group.draw(screen)

    # Draw the ground
    screen.blit(ground, (ground_scroll, 768))

    # Check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe is False:
            pass_pipe = True
        if pass_pipe is True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    # Show score
    draw_text(screen, str(score), font, white, int(screen_width / 2), 30)

    # Check if bird has hit ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    # Check if bird hit pipe and if bird flies out of screen (top)
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # If game isn't over, keep scrolling the ground
    if not game_over and flying:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        # Create pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1, pipe_gap)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1, pipe_gap)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)

            last_pipe = time_now

        # Only update pipe if game not over
        pipe_group.update()

    # Reset game if game over
    if game_over:
        if button.draw(screen):
            score = reset_game(pipe_group, flappy, screen_height)
            game_over = False
            game_started = False

    # Stop loop when user exits out of window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not flying and not game_over:
                flying = True
                game_started = True

    pygame.display.update()

pygame.quit()
