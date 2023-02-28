import pygame, os
from states.state import State
from states.world.player import Player
from states.world.gui import Gui


class GameWorld(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.grass_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png")).convert()
        self.grass_img = pygame.transform.scale(self.grass_img, (self.game.game_resolution[0], self.game.game_resolution[1]))
        self.player = Player(self.game)
        self.gui = Gui(self.game)

    def update(self, delta_time, actions):
        self.player.update(delta_time, actions)
        self.gui.update(delta_time, actions)

    def render(self, display):
        display.blit(self.grass_img, (0, 0))
        self.player.render(display)
        self.gui.render(display)
