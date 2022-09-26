import pygame.font


class Button(pygame.sprite.Sprite):
    def __init__(self, game, message):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.s = game.s
        self.end_screen_rect = game.end_screen_rect
        #text = pygame.font.Font.render()

        # Image and rect of button
        self.image = self.s.button1_image
        self.image_2 = self.s.button2_image  # Highlighted version of button
        self.rect = self.image.get_rect()
        self.rect.midtop = self.end_screen_rect.center

        self.highlight = False

    def blit(self):
        # Draws blank button and then draw message
        if not self.highlight:
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.image_2, self.rect)

    def hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True


