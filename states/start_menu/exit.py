import pygame, os

from states.state import State


class Exit(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.menu_options = {0: "Yes", 1: "No"}
        self.index = 0

        self.__create_menu_options__()
        self.draw_menu_options()

    def __create_menu_options__(self):
        # Set background
        self.background_surf = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png"))
        self.background_rect = self.background_surf.get_rect()
        self.background_surf.set_alpha(100)
        # Set the menu title
        self.title_surf = pygame.surface.Surface((self.game.game_resolution[0], self.game.game_resolution[1] / 4 * 1))
        self.title_surf.fill("black")
        self.title_surf.set_colorkey("black")
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.topleft = (0, 0)  # center title on top of options
        # Set the menu options
        self.menu_surf = pygame.surface.Surface((self.game.game_resolution[0], self.game.game_resolution[1] / 4 * 2))
        self.menu_surf.fill("black")
        self.menu_surf.set_colorkey("black")
        self.menu_rect = self.menu_surf.get_rect()
        self.menu_rect.topleft = (0, self.game.game_resolution[1] / 4 * 1)  # center menu on screen
        # Variables for the cursor
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "cursor.png"))
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_x, self.cursor_pos_y = self.game.game_resolution[0]/4, self.game.game_resolution[1]/4*1 + 45 + 7
        self.cursor_rect.center = self.cursor_pos_x, self.cursor_pos_y

    def draw_menu_options(self):
        x = self.menu_rect.width / 2
        y = 15
        self.game.draw_text(self.title_surf, "Do you really want", "white", x, y, "custom1 60")
        self.game.draw_text(self.title_surf, "to exit the game?", "white", x, y+80, "custom1 60")
        for index in self.menu_options:
            x = self.menu_rect.width/2
            y = 45 + (35 * index)
            self.game.draw_text(self.menu_surf, str(self.menu_options[index]), "white", x, y, "custom1 40")

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions["start"]:
            self.transition_state()
        if actions["back"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        display.fill((0, 0, 0))
        display.blit(self.background_surf, self.background_rect)
        display.blit(self.menu_surf, self.menu_rect)
        display.blit(self.title_surf, self.title_rect)
        display.blit(self.cursor_img, self.cursor_rect)

    def update_cursor(self, actions):
        # Switches through menu
        if actions["down"]:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions["up"]:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + (self.index * 35)

    def transition_state(self):
        if self.menu_options[self.index] == "Yes":
            # close the game entirely
            self.game.playing = False
            self.game.running = False
        elif self.menu_options[self.index] == "No":
            self.exit_state()
            self.game.reset_keys()
