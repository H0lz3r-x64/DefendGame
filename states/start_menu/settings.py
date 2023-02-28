import time

import pygame, os

from states.state import State
from states.start_menu.advanced_settings.display import Display
# from states.start_menu.advanced_settings.audio import Audio
# from states.start_menu.advanced_settings.keybindings import Keybindings


class Settings(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.play_animation = True
        self.animation = []
        self.frame = 0
        self.debug_time = time.time()
        self.scroll_offset = self.game.mwheel.y
        self.index = 0
        self.item_index = 0
        self.save_hover = False
        self.happened_last_frame = False
        self.click = False
        self.menu_type = 2  # unnötig

        # get variables from main class
        self.aspect = self.game.game_asp_val
        self.screen_resolution = pygame.Vector2(self.game.screen_resolution)
        self.game_resolution = pygame.Vector2(self.game.game_resolution)
        self.gui_scale = self.game.gui_scale
        self.gui_quality = self.game_resolution * self.gui_scale

        self.fullscreen = self.game.fullscreen
        self.FPS = self.game.framerate
        # --------

        self.menu_options = {0: "Display Settings", 1: "Audio", 2: "Keybindings", 3: "Back"}

        self.element_options = {0: self.aspect, 1: self.screen_resolution, 2: self.game_resolution, 3: self.gui_scale,
                                4: self.fullscreen, 5: self.FPS}

        self.load_animation()

        self.__create_menu_options__()
        if self.menu_type == 1:
            self.buttons()
        self.text_n_animation()
        self.rescale_n_draw_surfaces()

    # METHODS ---------------------------------

    def __create_menu_options__(self):
        """
        Description:
        Draws the all Surfaces in self.HUD_quality and scales them down to the desired resolution (screen resolution)
        By this we could achieve crispy clean and sharp text on resolutions up to 4k
        gui_resolution is adjustable to suit weaker hardware
        """

        title_height = self.gui_quality.y / 6  # Menu title height

        self.spacing = -4  # Change to adjust the height of each menu option

        # Menu options surface height
        options_height = (self.gui_quality.y / len(self.menu_options) + self.spacing) * (len(self.menu_options) - 1)
        # Variables for the cursor
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "cursor.png")).convert()
        self.cursor_pos_x, self.cursor_pos_y = self.gui_quality[0] / 4, self.gui_quality[1] / 4 * 1 + 7
        self.cursor_rect = self.cursor_img.get_rect(center=(self.cursor_pos_x, self.cursor_pos_y))

        # Set background
        self.background_surf = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png")).convert()
        self.background_surf = pygame.transform.scale(self.background_surf, self.gui_quality)
        self.background_rect = self.background_surf.get_rect()
        self.background_surf.set_alpha(100)  # change opacity

        # Set Footer
        self.footer_surf = pygame.Surface((self.gui_quality[0], self.gui_quality[1] / 10 * self.gui_scale))
        pos = (self.gui_quality[0] / 2, self.gui_quality[1])
        self.footer_rect = self.footer_surf.get_rect(midbottom=pos)
        self.footer_surf.fill("grey")  # debug fill

        # -----------------------------------------------------------------
        # Create Main Surface (on which other surfaces get blitted on to achieve gui scaling)
        self.surface_size = (self.gui_quality[0], title_height + options_height)
        self.surface = pygame.Surface(self.surface_size)
        self.surface.fill("green")  # debug fill

        # Create the title surface
        self.title_surf = pygame.Surface((self.surface_size[0], title_height))
        pos = (0, 0)  # stands for top left corner
        self.title_rect = self.title_surf.get_rect(topleft=pos)
        self.title_surf.fill("blue")  # debug fill

        if self.menu_type == 1:  # Menu with sliders to change settings
            # Create the label surface
            self.label_surf = pygame.Surface((((self.surface_size[0] / 2) / 3) * 2, options_height))
            pos = ((self.surface_size[0] / 2) / 3, title_height)  # stands for top left corner
            self.label_rect = self.label_surf.get_rect(topleft=pos)
            self.label_surf.fill("orange")  # debug fill

            # Create the elements surface
            self.elements_surf = pygame.Surface((((self.surface_size[0] / 2) / 3) * 2, options_height))
            pos = (self.surface_size[0] / 2, title_height)  # stands for top left corner
            self.elements_rect = self.elements_surf.get_rect(topleft=pos)
            self.elements_surf.fill("yellow")  # debug fill

        elif self.menu_type == 2:  # Menu to change into other menus
            self.label_surf = pygame.Surface(((((self.surface_size[0] / 2) / 3) * 2) * 2, options_height))
            pos = (((self.surface_size[0] / 2) / 3) * 1, title_height)  # stands for top left corner
            self.label_rect = self.label_surf.get_rect(topleft=pos)
            self.label_surf.fill("orange")  # debug fill

    def text_n_animation(self):
        # ---------------- Draw Text and option switches ----------------
        # Draw Title Text
        x = self.title_rect.width / 2
        y = self.title_rect.height / 3
        self.game.draw_text(self.title_surf, "Settings", "white", x, y, "arial 60")

        #   Draw Menu Options
        for index in self.menu_options:
            element_width = self.animation[0].get_width()
            element_height = self.gui_quality.y / len(self.menu_options) + self.spacing
            x = self.label_rect.width / 2
            y = 35 + (element_height * index)
            self.game.draw_text(self.label_surf, str(self.menu_options[index]), "white", x, y, "arial 40")

            if self.menu_type == 1:
                self.game.draw_text(self.elements_surf, str(self.element_options[index]), "white", x, y, "arial 40")
                # Draws the extended sliders when the animation is not running
                if self.play_animation:
                    frame = self.frame
                else:
                    frame = -1
                self.elements_surf.blit(self.animation[frame], (x - element_width / 2, y - 14))

    def buttons(self, click=False):
        # Create Footer elements (Buttons)

        # Create Button Surface and Rect
        self.save_btn_surf = pygame.Surface((self.footer_rect.w / 6, self.footer_rect.h / 2))
        pos = (self.footer_rect.w / 5 * 4, self.footer_rect.h / 2)
        self.save_btn_rect = self.save_btn_surf.get_rect(center=pos)

        #   Draw outline when buttons get hovered and flash on klick
        if click:
            # Create actual Button graphics
            self.game.draw_text(
                self.save_btn_surf, "Speichern", "yellow",
                self.save_btn_rect.w / 2, self.save_btn_rect.h / 2,
                "arial 30", alignment="center")

            #   Blit on footer surface
            self.footer_surf.blit(self.save_btn_surf, self.save_btn_rect)

            click_surf = pygame.Surface(self.save_btn_rect.size)
            click_surf.fill("white")
            click_surf.set_alpha(50)
            self.footer_surf.blit(click_surf, self.save_btn_rect)
        else:
            # Create actual Button graphics
            self.game.draw_text(
                self.save_btn_surf, "Speichern", "white",
                self.save_btn_rect.w / 2, self.save_btn_rect.h / 2,
                "arial 30", alignment="center")

            #   Blit on footer surface
            self.footer_surf.blit(self.save_btn_surf, self.save_btn_rect)

        if self.save_hover:
            pygame.draw.rect(self.footer_surf, "yellow", self.save_btn_rect, 4)

        # ---------------- Footer Buttons ----------------

        # Rescale Save Button Surface (we do this here since if we rescale it with the footer surface together,
        # it gets rescaled in the height only because the footer keeps its width at all times, other than the button.
        self.save_btn_surf = pygame.transform.scale(
            self.save_btn_surf,
            (self.save_btn_rect.w * self.gui_scale,
             self.save_btn_rect.h * self.gui_scale)
        )

        # Get real save btn rect to check mouse collision later
        # This is necessary since the original save btn surface is blitted on the footer surface
        self.save_btn_rect = pygame.Rect(
            self.footer_rect.x + self.save_btn_rect.x,
            self.footer_rect.y + self.save_btn_rect.y,
            self.save_btn_rect.w,
            self.save_btn_rect.h
        )

    def rescale_n_draw_surfaces(self):
        # ---------------- Main Surfaces ----------------
        # Render surfaces on main surface
        self.surface.blit(self.title_surf, self.title_rect)  # menu title on top of the screen
        self.surface.blit(self.label_surf, self.label_rect)  # label on left half of the screen
        if self.menu_type == 1:
            self.surface.blit(self.elements_surf, self.elements_rect)  # elements on right half of the screen

        # Rescale Main Surface
        pos = (self.gui_quality[0] / 2, 0 + self.scroll_offset)  # stands for game canvas center
        self.surface = pygame.transform.scale(
            self.surface,
            (self.surface.get_width() * self.gui_scale,
             self.surface.get_height() * self.gui_scale)
        )
        # Get new surface rect
        self.surface_rect = self.surface.get_rect(midtop=pos)

    def load_animation(self):
        path = os.path.join(self.game.gui_dir, "switch_element", "frame")
        for i in range(0, 34):
            image = pygame.image.load(path + str(i) + ".png").convert_alpha()
            image = pygame.transform.scale2x(image)
            self.animation.append(image)

    def update_cursor(self, actions):
        # Switches through menu
        if actions["down"]:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions["up"]:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + (self.index * 35)

    def save(self):
        # Save settings to main class
        self.game.game_asp_val = self.aspect

        self.game.screen_resolution = self.screen_resolution
        self.game.game_resolution = self.game_resolution

        self.game.gui_scale = self.gui_scale

        self.game.fullscreen = self.fullscreen
        self.game.framerate = self.FPS

    # -----------------------------------------------------------------------------------------------

    def update(self, delta_time, actions):
        if actions['mouse left']:
            self.click = True
        else:
            self.click = False

        if self.menu_type == 1:
            if self.save_btn_rect.collidepoint(pygame.mouse.get_pos()):
                self.save_hover = True
                self.happened_last_frame = True

        # Scroll wheel
        if self.surface_rect.h + self.footer_rect.h >= self.screen_resolution.y:
            if self.game.mwheel.y:
                self.scroll_offset += self.game.mwheel.y * 20
                print(self.scroll_offset)
                if self.scroll_offset > 0:
                    self.scroll_offset = 0
                if self.scroll_offset < -self.surface_rect.h + self.screen_resolution.y - self.footer_rect.h:
                    self.scroll_offset = -self.surface_rect.h + self.screen_resolution.y - self.footer_rect.h

        # update frame index
        if self.menu_type == 1:
            if self.play_animation:
                animation_speed = 0.8
                self.frame += int(round(animation_speed * 100) * delta_time)
                print("frame: ", self.frame)
                # reset frame index
                if self.frame >= len(self.animation) - 1:
                    self.frame = 0
                    self.play_animation = False
                    print(time.time() - self.debug_time)

            self.gui_scale = self.game.gui_scale  # temp
            self.save()

        # Key inputs
        if actions["up"]:  # temp
            self.play_animation = True
        if actions["start"]:
            self.transition_state()
        if actions["back"]:
            self.exit_state()
            self.game.reset_keys()

        self.update_cursor(actions)

    def render(self, display):
        # do if conditions are met
        if self.play_animation or self.game.mwheel.y or self.save_hover or self.happened_last_frame:
            self.__create_menu_options__()
            self.text_n_animation()
            if self.menu_type == 1:
                self.buttons(self.click)
            self.rescale_n_draw_surfaces()

            # reset conditions
            if self.game.mwheel.y:
                self.game.mwheel.y = 0

            if self.happened_last_frame and not self.save_hover:
                self.happened_last_frame = False

            if self.save_hover:
                self.save_hover = False

        # Blit background
        display.blit(self.background_surf, self.background_rect)  # background doesn't change by scale
        # Blit Main Surface
        display.blit(self.surface, self.surface_rect)
        # Blit Footer
        display.blit(self.footer_surf, self.footer_rect)

    def transition_state(self):
        if self.menu_options[self.index] == "Display Settings":
            new_state = Display(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Audio":
            print("NotImplemented")
            pass
            new_state = Audio(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Keybindings":
            print("NotImplemented")
            pass
            new_state = Keybindings(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == "Back":
            self.exit_state()
            self.game.reset_keys()
