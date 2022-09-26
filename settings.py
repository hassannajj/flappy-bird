import pygame


class Settings:
    def __init__(self):
        # Pygame settings
        self.fps = 60
        # Screen settings
        # Full screen is 1450, 900
        self.screen_width = 1000
        self.screen_height = 750
        self.caption = "Flappy Bird"
        self.bg_color = (0, 100, 150)
        pygame.mixer.init()

        # Bird settings
        self.bird_width = int(self.screen_width * 0.06)
        self.bird_height = int(self.bird_width * 0.67)
        self.bird_color = (255, 255, 255)
        self.jump_height = int(self.screen_height * 0.008)  # screen height * 0.008
        self.fall_speed = float(self.screen_height * 0.0004)  # screen height * 0.0004

        # Pipe settings
        self.gap_height = int(self.screen_height * 0.3)
        self.pipe_width = int(self.screen_width * .15)  # screen width times .15
        self.pipe_height = self.screen_height
        self.pipe_color = (0, 0, 0)
        self.pipe_speed = self.screen_width * 0.004  # screen width times 0.004

        # End Screen Settings
        self.end_screen_color = (131,120,107)
        self.button_width = int(self.screen_width * 0.10)  # Screen width * 0.08
        self.button_height = int(self.button_width * 0.83)
        self.button_color = (0, 255, 0)
        self.end_screen_width = int(self.screen_width / 2)
        self.end_screen_height = int(self.screen_height / 2)
        self.border_width = 8

        # Images
        # Scaled up images for buttons
        self.button1_image = pygame.transform.scale(pygame.image.load('images/button1.png'),
                                                    (self.button_width, self.button_height))  # 12: 10
        self.button2_image = pygame.transform.scale(pygame.image.load('images/button2.png'),
                                                    (self.button_width, self.button_height))  # 12: 10
        self.bird_image = pygame.transform.scale(pygame.image.load('images/bird.png'),
                                                 (self.bird_width, self.bird_height))  # 68: 46
        self.pipe_image = pygame.transform.scale(pygame.image.load('images/pipe.png'),
                                                 (self.pipe_width, self.pipe_height))
        self.bg = pygame.transform.scale(pygame.image.load('images/bg.png'),
                                         (self.screen_width, self.screen_height))

        # Audio files
        self.wing_sfx = pygame.mixer.Sound('audio/wing_flap.mp3')
        self.point_sfx = pygame.mixer.Sound('audio/point.mp3')
        self.punch_sfx = pygame.mixer.Sound('audio/punch.mp3')
        self.die_sfx = pygame.mixer.Sound('audio/die.mp3')

        # Fonts
        self.font_color = (0, 0, 0)
        self.font_size = int(self.screen_width * 0.035)  # screen width * 0.035
        self.bebas_font = pygame.font.Font('fonts/bebas.ttf', self.font_size)
        self.ka1_font = pygame.font.Font('fonts/ka1.ttf', self.font_size)
