import pygame
import random
from settings import Settings
from bird import Bird
from pipe import Pipe
from button import Button

pygame.init()  # Initializes pygame


class Game:
    """ Overall class for managing game assets and behavior.
    """
    def __init__(self):
        self.s = Settings()
        self.screen = pygame.display.set_mode((self.s.screen_width, self.s.screen_height))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(self.s.caption)

        # END SCREEN
        self.end_screen_surface = pygame.Surface((self.s.end_screen_width, self.s.end_screen_height))
        self.end_screen_rect = self.end_screen_surface.get_rect()
        self.end_screen_rect.center = (self.s.screen_width / 2, self.s.screen_height / 2)

        self.end_screen_border = pygame.Surface(
            (self.s.end_screen_width + self.s.border_width, self.s.end_screen_height + self.s.border_width))
        self.end_screen_border_rect = self.end_screen_border.get_rect()
        self.end_screen_border_rect.center = (self.s.screen_width / 2, self.s.screen_height / 2)

        self.button = Button(self, "Restart")

        self.bird = Bird(self)
        self.clock = pygame.time.Clock()
        self.running = True
        self.start = False
        self.end = False

        self.score_count = 0

        self.pipes = pygame.sprite.Group()
        self.pipes_scoring = self.pipes.copy()  # Copy of the pipe group to track scoring

        self._find_pipe_spread()  # Finds where the spawn point for pipe should be

        self.font = self.s.ka1_font

    def run(self):
        # Main Game Loop
        while self.running:
            self._check_events()
            if self.start and not self.end:  # If player presses space bar in the beginning
                self._update_bird()
                self._update_pipe()
                self._detect_score()
                self._check_collisions()
                self._update_screen()
                self.clock.tick(self.s.fps)  # FPS
            self._update_screen()  # Shows first frame of the game

    def _check_events(self):
        for event in pygame.event.get():
            self.mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._key_down(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_down()
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_up()

    def _mouse_down(self):
        if self.button.hover(self.mouse_pos):
            self.button.highlight = True
        else:
            self.button.highlight = False

    def _mouse_up(self):
        if self.button.highlight and self.button.hover(self.mouse_pos) and self.end:
            self._restart()
        self.button.highlight = False

    def _key_down(self, event):
        if event.key == pygame.K_q:
            self.running = False
        elif event.key == pygame.K_SPACE and not self.end:
            self.start = True
            self._jump()
        elif event.key == pygame.K_r and self.end:
            self._restart()

    def _jump(self):
        """Allows bird to jump and plays audio file for flapping."""
        self.bird.dy = -self.s.jump_height
        self.bird.jump()
        self.s.wing_sfx.play()

    def _update_bird(self):
        self.bird.dy += self.s.fall_speed
        self._tilt_bird()
        self.bird.update()

    def _tilt_bird(self):
        self.rotation = int(abs(self.bird.dy))
        if self.bird.dy > 0:
            self.rotation *= -1  # if falling down
        else:
            self.rotation *= 3  # if going up
        self.bird.tilt(self.rotation * 3)

    def _check_collisions(self):
        if self.bird.rect.top < self.screen_rect.top:  # Checks collisions with top screen
            #self.bird.y = 0
            pass
        if self.bird.rect.bottom >= self.screen_rect.bottom:  # Checks collisions with bottom screen:
            self._end_game()
        if pygame.sprite.spritecollideany(self.bird, self.pipes):
            self._end_game()

    def _detect_score(self):
        for pipe in self.pipes.sprites():
            if self.bird.pos[0] >= pipe.rect.x + (self.s.pipe_width - self.s.bird_width) > \
                    self.bird.pos[0] - self.s.pipe_speed:
                self._count_score()
                break  # Breaks loop so that both top and btm pipes aren't added together and scored twice

    def _count_score(self):
        """Counts score, plays audio file of a point."""
        self.score_count += 1
        self.s.point_sfx.play()  # Audio of getting a point

    def _update_pipe(self):
        self._check_pipe()
        for pipe in self.pipes.sprites():
            pipe.update()

    def _find_pipe_spread(self):
        """Finds out where each pipe should be created.
        Used for the _check_pipe() function."""
        # Spawn point with the remainder added
        constant = 0.8
        self.pipe_spawn_point = int(self.s.screen_width / (1 + (self.s.pipe_speed/10)))
        self.pipe_spawn_point *= constant

    def _check_pipe(self):
        if len(self.pipes) == 0:
            self._create_pipe()
        else:
            for pipe in self.pipes.sprites():
                if self.pipe_spawn_point >= pipe.rect.x > self.pipe_spawn_point - self.s.pipe_speed:
                    self._create_pipe()
                    break  # Breaks loop so that new pipes aren't created more than once

                if pipe.rect.x < (0 - self.s.pipe_width):  # Pipe moves to the left of the screen
                    self.pipes.remove(pipe)  # Pipe is removed

    def _create_pipe(self):
        x_pos = self.s.screen_width
        # Gap
        gap_ypos = random.randint(0, self.s.screen_height - self.s.gap_height)

        # Top Pipe
        pipe_pos = x_pos, gap_ypos
        self.pipe = Pipe(self, pipe_pos)
        self.pipe.top_pipe = True
        self.pipes.add(self.pipe)
        self.pipe.start_pos(1)

        # Bottom Pipe                                                         
        pipe_pos = x_pos, gap_ypos + self.s.gap_height
        self.pipe = Pipe(self, pipe_pos)
        self.pipes.add(self.pipe)
        self.pipe.start_pos(2)

    def _end_game(self):
        """Deactivates game and stores score. Also plays audio file for dying"""
        self.start = False
        self.end = True
        self._store_score()

        self.s.punch_sfx.play()
        self.s.die_sfx.play()

    def _bird_fall(self):
        self.bird.dy = 5
        if self.bird.rect.y + self.s.bird_height < self.s.screen_height:
            self.bird.update()
            self.bird.tilt(290)

    def _store_score(self):
        """Compares current score to the best score and then stores current score."""
        with open('scores.txt', 'r') as file:
            score_list = file.read().strip().split('\n')  # Puts all the scores in a list

        score_list = [int(i) for i in score_list]
        self.og_high_score = max(score_list)

        with open('scores.txt', 'a') as file:  # Stores current score
            file.write(f"{self.score_count}\n")

        self.score_color = (0, 0, 0)
        if self.score_count > self.og_high_score:
            self.score_color = (100, 60, 5)
            self.og_high_score = self.score_count

    def _display_text(self, msg, pos, size, color):
        self.s.font_size = size
        self.msg_display = self.font.render(str(msg), True, color)
        self.msg_display_rect = self.msg_display.get_rect()
        self.msg_display_rect.midtop = pos
        self.screen.blit(self.msg_display, self.msg_display_rect)

    def _display_end_screen(self):
        # Draws title screen background
        pygame.draw.rect(self.screen, (0, 0, 0), self.end_screen_border_rect)  # Border

        pygame.draw.rect(self.screen, self.s.end_screen_color,  # Title screen
                         self.end_screen_rect)

        # Draws button
        self.button.blit()

        # Display Score
        self._display_text(self.score_count,
                           (self.s.screen_width / 2.9, self.s.screen_height / 2.5), 30, self.score_color)
        self._display_text('Score',
                           (self.s.screen_width / 2.9, self.s.screen_height / 1.85), 30, (0, 0, 0))

        # Display best score
        self._display_text(self.og_high_score,
                           (self.s.screen_width / 1.55, self.s.screen_height / 2.5), 30, self.score_color)
        self._display_text('Best',
                           (self.s.screen_width / 1.55, self.s.screen_height / 1.85), 30, (0, 0, 0))

    def _update_screen(self):
        self.screen.blit(self.s.bg, (0, 0))  # MUST ALWAYS BE FIRST IN THIS FUNCTION
        if not self.start and not self.end:  # If game hasn't started
            self._display_text("Press SPACE to start", (self.s.screen_width/2,
                                                        self.s.screen_height/5), self.s.font_size, (0, 0, 0))

        self.bird.blit()
        for pipe in self.pipes.sprites():
            pipe.blit()

        if self.start:
            # Displays score
            self._display_text(self.score_count, (self.s.screen_width/2,
                                                       self.s.screen_height/10), self.s.font_size, (0, 0, 0))

        if self.end:
            self._bird_fall()
            self._display_end_screen()

        pygame.display.flip()

    def _restart(self):
        """
        Restarts the game after clicking the button or typing 'r', resets variables
        """
        self.end = False
        self.pipes.empty()
        self.bird.rect.y = self.s.screen_height / 2
        self.bird.y = self.s.screen_height / 2
        self.bird.tilt(0)
        self.score_count = 0


if __name__ == '__main__':
    game = Game()
    game.run()
