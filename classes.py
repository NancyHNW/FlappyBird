import pygame
from functions import draw_text, reset_game


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, colour="red"):
        pygame.sprite.Sprite.__init__(self)
        self.images = []  # list for the bird images for animation
        self.index = 0
        self.counter = 0  # for animation speed control
        self.colour = colour

        # load bird images qnd add to list
        for num in range(1, 4):
            img = pygame.image.load(f"assets/bird{self.colour}{num}.png")
            self.images.append(img)

        # set initial image and rectangle for the bird
        self.image = self.images[self.index]
        self.image = pygame.transform.rotate(self.image, 0)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self, flying, game_over):

        # load bird images qnd add to list
        for num in range(1, 4):
            img = pygame.image.load(f"assets/bird{self.colour}{num}.png")
            self.images.append(img)

        # handle animation
        self.counter += 1
        flat_cooldown = 5  # speed control

        # only apply gravity when bird is flying
        if flying:
            # apply gravity
            self.vel += 0.5
            if self.vel > 8:  # adding cap for vel
                self.vel = 8
            if self.rect.bottom < 768:  # keep bird above ground
                self.rect.y += int(self.vel)

        if not game_over:

            # rotate through images for animation
            if self.counter > flat_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # handle bird jump (fly)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] == 1 and not self.clicked:
                self.vel = -10
                self.clicked = True
            if keys[pygame.K_SPACE] == 0:
                self.clicked = False

            # rotate the bird based on velocity (going up or down)
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:  # if game is over, turn the bird 90 degree clockwise (face down)
            self.image = pygame.transform.rotate(self.images[self.index], -90)

    def update_colour(self, new_colour):
        self.colour = new_colour
        self.update()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, pipe_gap):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/pipe.png")  # load pipe image
        self.rect = self.image.get_rect()

        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        # move pipe to the left
        self.rect.x -= 4

        # delete the pipe when it's off the screen
        if self.rect.right < 0:
            self.kill()


class Button:
    def __init__(self, x, y, image, hover_image=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hover_image = hover_image
        self.clicked = False

    def draw(self, screen):

        # get mouse position & click
        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # check if mouse is hovered over the button & left mouse btn clicked
        if self.rect.collidepoint(pos):
            if self.hover_image is not None:
                screen.blit(self.hover_image, (self.rect.x, self.rect.y))
            if mouse_pressed and not self.clicked:
                self.clicked = True
                return True
        else:
            # draw button
            screen.blit(self.image, (self.rect.x, self.rect.y))

        if not mouse_pressed:
            self.clicked = False

        return False


class Menu:
    def __init__(self):
        self.bird_colour = "red"
        self.colour_btns = {
            'red': Button(200, 200, pygame.image.load("assets/birdred2.png")),
            'yellow': Button(100, 200, pygame.image.load("assets/birdyellow2.png")),
        }
        back = pygame.transform.scale(pygame.image.load("assets/back.png"), (85 * 1.4, 42 * 1.4))
        back_hover = pygame.transform.scale(pygame.image.load("assets/hover_back.png"), (85 * 1.4, 42 * 1.4))
        self.back_btn = Button(700, 30, back, back_hover)

    def draw(self, screen):
        draw_text(screen, "Select Bird Color", pygame.font.SysFont("Victor Mono", 50), (255, 255, 255), 250, 100)
        for color, button in self.colour_btns.items():
            button.draw(screen)
        self.back_btn.draw(screen)

    def update(self, bird):
        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for colour, button in self.colour_btns.items():
            if button.rect.collidepoint(pos) and mouse_pressed[0]:
                self.bird_colour = colour
                bird.update_colour(colour)
        if self.back_btn.rect.collidepoint(pos) and mouse_pressed[0]:
            return True
        return False