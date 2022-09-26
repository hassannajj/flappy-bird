import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.s = self.game.s
        self.screen = self.game.screen

        self.pos = (self.s.screen_width / 3, self.s.screen_height / 2)

        # Image and rect of bird
        self.image = self.s.bird_image
        self.rot_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # Store a decimal value for the planet's position
        self.y = float(self.rect.y)

        # Speed
        self.dy = 0

    def tilt(self, rotation):
        self.rot_image = pygame.transform.rotate(self.image, rotation)

    def blit(self):
        self.screen.blit(self.rot_image, self.rect)

    def jump(self):
        self.y -= 30

        self.rect.y = self.y

    def update(self):
        self.y += self.dy

        self.rect.y = self.y
