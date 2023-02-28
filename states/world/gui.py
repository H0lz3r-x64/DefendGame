import pygame, os
from states.state import State
from states.world.player import Player
from states.world.pause_menu.pause_menu import PauseMenu
from states.world.inventory import Inventory


class Gui:
    def __init__(self, game):
        self.game = game
        self.player = Player(self.game)
        self.__load_sprites__()
        self.menu_opened = False

    def __load_sprites__(self):
        self.slot_img = pygame.image.load(os.path.join(self.game.gui_dir, "slot.png")).convert()
        self.selected_img = pygame.image.load(os.path.join(self.game.gui_dir, "selected.png")).convert()
        self.broken_sword_img = pygame.image.load(os.path.join(self.game.gui_dir, "broken_sword.png")).convert()

    def update(self, delta_time, actions):
        self.menu_opened = False
        if actions["back"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
            self.game.reset_keys()
            self.menu_opened = True
        if actions["i"]:
            new_state = Inventory(self.game)
            new_state.enter_state()
            self.game.reset_keys()
            self.menu_opened = True

    def render(self, display):
        if not self.menu_opened:
            self.draw_slots(display)

    def draw_slots(self, display):
        self.quickbar = self.player.quickbar
        self.quickbar_offset = 3 + self.slot_img.get_width()

        self.quickbar_x = self.game.screen_resolution[0] / 2 - self.quickbar_offset * len(self.quickbar) / 2
        self.quickbar_y = self.game.game_resolution[1] - 40

        for i in range(len(self.quickbar)):
            pos = (self.quickbar_x + self.quickbar_offset * i, self.quickbar_y)
            # generiert slots
            display.blit(self.slot_img, pos)
            # füllt die slots mit den ausgerüsteten items
            if self.quickbar[i] is not None:
                display.blit(self.quickbar[i], pos)
