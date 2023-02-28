import pygame, os
from states.state import State


class PartyMenu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)

    def update(self, delta_time, actions):
        if actions["back"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        display.fill((255, 255, 255))
        self.game.draw_text(display, "PartyMenu here", "black", self.game.game_resolution[0] / 2,
                            self.game.game_resolution[1] / 2, "custom1 60")
