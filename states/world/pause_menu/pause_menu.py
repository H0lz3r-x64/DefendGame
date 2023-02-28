import os, pygame

from states.state import State
from states.world.pause_menu.party import PartyMenu


class PauseMenu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        # Set the menu
        self.menu_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "menu.png")).convert()
        self.menu_rect = self.menu_img.get_rect()
        self.menu_rect.center = (self.game.game_resolution[0] * .85, self.game.game_resolution[1] * .4)  # center menu on wanted screen position
        # Set the cursor and menu states
        self.menu_options = {0: "Party", 1: "Items", 2: "Magic", 3: "Exit"}
        self.index = 0
        # Variables for the cursor
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "cursor.png")).convert()
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_x = self.menu_rect.x + 10
        self.cursor_pos_y = self.menu_rect.y + 38
        self.cursor_rect.x, self.cursor_rect.y = self.cursor_pos_x, self.cursor_pos_y

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions["start"]:
            self.transition_state()
        if actions["back"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        self.previous_state.render(display)
        display.blit(self.menu_img, self.menu_rect)
        display.blit(self.cursor_img, self.cursor_rect)

    def update_cursor(self, actions):
        # Switches through menu
        if actions["down"]:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions["up"]:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + (self.index * 32)

    def transition_state(self):
        if self.menu_options[self.index] == "Party":
            new_state = PartyMenu(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Items":
            pass  # TODO
        elif self.menu_options[self.index] == "Magic":
            pass  # TODO
        elif self.menu_options[self.index] == "Exit":
            # pop every element until the stack is empty. Now the start state (title scree) will appear
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()
