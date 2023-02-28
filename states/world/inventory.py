import os, pygame

from states.state import State
from states.world.player import Player


class Inventory(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        self.player = Player(self.game)
        self.inventory = self.player.inventory

        self.__load_sprites__()
        self.max_cols = 9
        self.y_offset = 3 + self.slot_img.get_height()
        self.x_offset = 3 + self.slot_img.get_width()

    def __load_sprites__(self):
        # temp
        self.inv = pygame.image.load("inv.png")
        self.inv = pygame.transform.scale(self.inv, (self.inv.get_width()*0.4, self.inv.get_height()*0.4))

        self.slot_img = pygame.image.load(os.path.join(self.game.gui_dir, "slot.png")).convert()
        self.selected_img = pygame.image.load(os.path.join(self.game.gui_dir, "selected.png")).convert()
        self.broken_sword_img = pygame.image.load(os.path.join(self.game.gui_dir, "broken_sword.png")).convert()

    def update(self, delta_time, actions):
        if actions["i"] or actions["back"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        self.previous_state.render(display)
        self.draw_headers(display)
        self.draw_inventory(display)
        # temp
        display.blit(self.inv, (self.game.game_resolution[0] / 2 - self.inv.get_width()/2, self.game.game_resolution[1] / 2 - self.inv.get_height()/2))

    def draw_background(self):
        pass

    def draw_headers(self, display):
        text = "Inventory"
        self.game.draw_text(display, text, "black", self.game.game_resolution[0] / 2, self.y_offset, 2, alignment="midbottom")

    def draw_inventory(self, display):
        rows = (len(self.inventory) // self.max_cols) + 1

        x = self.game.game_resolution[0] / 2 - self.x_offset * (self.max_cols / 2)
        y = self.game.game_resolution[1] / 2 - self.y_offset * (rows / 2)

        i = 0  # Keeps track of how many slots have been drawn
        for r in range(rows):  # iterates through rows
            for c in range(self.max_cols):  # iterates through max columns per row
                if i < len(self.inventory):
                    display.blit(self.slot_img, (x + self.x_offset * c, y + self.y_offset * r))
                    # füllt die slots mit den ausgerüsteten items
                    if self.inventory[i] is not None:
                        display.blit(self.inventory[i], (x + self.x_offset * c, y + self.y_offset * r))
                i += 1
