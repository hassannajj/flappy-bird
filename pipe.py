import pygame


class Pipe(pygame.sprite.Sprite):
    def __init__(self, game, position):
        super().__init__()
        self.game = game
        self.s = self.game.s
        self.screen = self.game.screen

        self.pos = (position)

        # Image and rect
        self.image = self.s.pipe_image
        self.rot_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = self.s.screen_width

        # Store a decimal value for the pipe's position
        self.x = float(self.rect.x)

        # Speed
        self.dx = self.s.pipe_speed

    def start_pos(self, pipe):
        if pipe == 1:  # Top pipe
            self.rect.bottomleft = self.pos
            self.rot_image = pygame.transform.rotate(self.image, 180)
            self.rot_image = pygame.transform.flip(self.rot_image, True, False)  # Flip pipe for lighting

        if pipe == 2:  # Bottom pipe
            self.rect.topleft = self.pos

    def blit(self):
        self.screen.blit(self.rot_image, self.rect)

    def update(self):
        self.x -= self.dx

        self.rect.x = self.x
