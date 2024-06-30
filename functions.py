import pygame


def draw_text(screen, text, font, colour, x, y, outline_color=(0, 0, 0), outline_thickness=2):
    outline = font.render(text, True, outline_color)

    # draw text outline
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            # Skip the center
            if dx != 0 or dy != 0:
                screen.blit(outline, (x + dx, y + dy))

    img = font.render(text, True, colour)
    screen.blit(img, (x, y))


def reset_game(pipe_group, flappy, screen_height):
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    return 0
