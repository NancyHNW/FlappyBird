import pygame


def draw_text(screen, text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))


def reset_game(pipe_group, flappy, screen_height):
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    return 0
