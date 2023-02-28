import pygame
from pygame.locals import *


class InputEvents:
    @staticmethod
    # Reset key inputs
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    @staticmethod
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == MOUSEWHEEL:
                self.mwheel.xy = event.x, event.y

            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    self.actions['mouse left'] = True
                if event.button == BUTTON_RIGHT:
                    self.actions['mouse right'] = True

            if event.type == MOUSEBUTTONUP:
                if event.button == BUTTON_LEFT:
                    self.actions['mouse left'] = False
                if event.button == BUTTON_RIGHT:
                    self.actions['mouse right'] = False

            if event.type == pygame.KEYDOWN:
                if event.unicode == 'a' or event.unicode == 'A':
                    self.actions['left'] = True
                if event.unicode == 'd' or event.unicode == 'D':
                    self.actions['right'] = True
                if event.unicode == 'w' or event.unicode == 'W':
                    self.actions['up'] = True
                if event.unicode == 's' or event.unicode == 'S':
                    self.actions['down'] = True
                if event.unicode == 'i' or event.unicode == 'I':
                    self.actions['i'] = True
                if event.unicode == 'e' or event.unicode == 'E':
                    self.actions['start'] = True

                if event.key == K_UP:
                    self.actions['arrow up'] = True
                if event.key == K_DOWN:
                    self.actions['arrow down'] = True
                if event.key == K_LEFT:
                    self.actions['arrow left'] = True
                if event.key == K_RIGHT:
                    self.actions['arrow right'] = True

                if event.key == K_LSHIFT:
                    self.actions['shift'] = True
                if event.key == K_ESCAPE:
                    self.actions['back'] = True

                if event.unicode == '+':
                    print('+')
                    self.gui_scale += 0.1
                if event.unicode == '-':
                    print('-')
                    self.gui_scale -= 0.1

                if event.key == K_F11:
                    self.fullscreen = not self.fullscreen
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode((0, 0), FULLSCREEN)
                        self.game_aspect = self.screen_aspect
                        self.screen_resolution = self.screen.get_width(), self.screen.get_height()
                    else:
                        # load non fullscreen res and aspect
                        self.screen = pygame.display.set_mode((self.screen_resolution[0], self.screen_resolution[1]))
                        self.game_aspect = self.screen_aspect
                        self.screen_resolution = self.screen.get_width(), self.screen.get_height()



                    # self.game_canvas = pygame.display.set_mode(self.game_resolution)
                    # self.gui_resolution = self.game_resolution
                    # print(self.game_resolution)

            if event.type == KEYUP:
                if event.unicode == 'a' or event.unicode == 'A':
                    self.actions['left'] = False
                if event.unicode == 'd' or event.unicode == 'D':
                    self.actions['right'] = False
                if event.unicode == 'w' or event.unicode == 'W':
                    self.actions['up'] = False
                if event.unicode == 's' or event.unicode == 'S':
                    self.actions['down'] = False
                if event.unicode == 'i' or event.unicode == 'I':
                    self.actions['i'] = False
                if event.unicode == 'e' or event.unicode == 'E':
                    self.actions['start'] = False

                if event.key == K_UP:
                    self.actions['arrow up'] = False
                if event.key == K_DOWN:
                    self.actions['arrow down'] = False
                if event.key == K_LEFT:
                    self.actions['arrow left'] = False
                if event.key == K_RIGHT:
                    self.actions['arrow right'] = False

                if event.key == K_LSHIFT:
                    self.actions['shift'] = False
                if event.key == K_ESCAPE:
                    self.actions['back'] = False