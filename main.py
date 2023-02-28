import ctypes, platform
import time, os, psutil, pygame

import functions
from InputEvents import InputEvents
import config.startup_config as startup_Config
import config.settings_config as settings_Config

# from states.start_menu.title import Title
from states.start_menu.title import Title


def set_dpi_awareness():
    if platform.system() == "Windows":
        # Query DPI Awareness (Windows 10 and 8)
        awareness = ctypes.c_int()
        errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

        if awareness.value == 0 or awareness.value == 1:
            release = platform.release()
            if release == "11" or release == "10" or release == "8":
                # Set DPI Awareness  (Windows 10 and 8)
                errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
                # the argument is the awareness level, which can be 0, 1 or 2:
                # for 1-to-1 pixel control I seem to need it to be non-zero
            elif release == "7" or release == "Vista":
                # Set DPI Awareness  (Windows 7 and Vista)
                success = ctypes.windll.user32.SetProcessDPIAware()


class Game:
    def __init__(self):
        pygame.init()
        set_dpi_awareness()  # to disable windows ui scaling

        self.startup_conf = startup_Config.__init__()
        print(self.startup_conf.settings_config_path)
        self.settings_conf = settings_Config.__init__(self.startup_conf)
        print(self.settings_conf.title)

        # general variables
        self.clock = pygame.time.Clock()
        self.mwheel = pygame.Vector2()
        self.dt, self.previous_time = 0, 0
        self.running, self.playing = True, True
        self.state_stack = []

        # debug variables
        self.pid = psutil.Process(os.getpid())
        self.ram = None
        self.cpu = None
        self.frames_passed = 0

        # Game Variables
        self.framerate = 120
        self.gui_scale = 1
        self.fullscreen = False

        # keybindings
        self.actions = {
            "up": False, "left": False, "down": False, "right": False, "main": False, "secondary": False, "use": False,
            "reload": False, "inventory": False, "pause_close": False}

        # Surfaces
        # -----------------------------------------------------------------------------------------------
        self.__set_supported_resolutions__()
        # Screen
        #    Values from Settings
        self.screen_asp_val = "16:9"
        self.screen_res_val = "FHD"
        #    Gets actual values from dictionary
        self.screen_aspect = self.supported_resolutions[self.screen_asp_val]  # Aspect Ratio
        self.screen_resolution = self.screen_aspect[self.screen_res_val]  # Resolution
        # ------------------------------
        # Game#
        self.game_asp_val = "16:9"
        self.game_res_val = "FHD"
        self.game_asp_val = self.game_asp_val  # not manually changeable (at least for now)
        #    Gets actual values from dictionary
        self.game_aspect = self.supported_resolutions[self.game_asp_val]  # Aspect Ratio
        self.game_resolution = self.game_aspect[self.game_res_val]  # Game Quality
        # ------------------------------
        # Gui
        self.gui_scaling = 100
        # ------------------------------
        # initialize surfaces
        self.screen = pygame.display.set_mode(self.screen_resolution)
        self.game_canvas = pygame.Surface(self.game_resolution)
        # -----------------------------------------------------------------------------------------------

        self.__load_assets__()
        self.load_states()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.previous_time
        self.previous_time = now

    # Function to help with drawing text
    def draw_text(self, surface, text, color, x, y, font_type="", aa=False, background=None, colorkey=False,
                  keycolor=(0, 0, 0), alignment="midtop"):
        text_surface = self.font[font_type].render(text, aa, color, background)
        if colorkey:
            text_surface.set_colorkey(keycolor)

        align = (
            "topleft", "bottomleft", "topright", "bottomright", "midtop", "midleft", "midbottom", "midright", "center")
        text_rect = text_surface.get_rect()
        for item in align:
            if alignment == item:
                setattr(text_rect, item, (x, y))
        surface.blit(text_surface, text_rect)

    def display_stats(self, surface):
        fps = " FPS: " + str(round(self.clock.get_fps(), 1))
        g_res = " Game: " + str(int(self.game_resolution[0])) + "×" + str(int(self.game_resolution[1]))
        s_res = " Screen: " + str(int(self.screen_resolution[0])) + "×" + str(int(self.screen_resolution[1]))
        # do every 3 seconds for performance reasons
        if self.frames_passed == self.framerate * 3 or self.frames_passed == 0:
            self.cpu = " CPU: " + str(round(self.pid.cpu_percent() / psutil.cpu_count(False), 1)) + " %"
            self.ram = " RAM: " + str(round((self.pid.memory_full_info()[12] - 1000000) * 10 ** -6, 1)) + " MB"
            # reset frames_passed
            self.frames_passed = 1
        self.draw_text(surface, fps, "white", self.game_resolution[0], 5, "arial 30", background="darkgreen",
                       alignment="topright")
        self.draw_text(surface, self.cpu, "white", self.game_resolution[0], 45, "arial 30", background="orange",
                       alignment="topright")
        self.draw_text(surface, self.ram, "white", self.game_resolution[0], 85, "arial 30", background="red",
                       alignment="topright")
        self.draw_text(surface, g_res, "white", self.game_resolution[0], 125, "arial 30", background="blue",
                       alignment="topright")
        self.draw_text(surface, s_res, "white", self.game_resolution[0], 165, "arial 30", background="blue",
                       alignment="topright")
        # iterate frames_passed
        self.frames_passed += 1

    def __load_assets__(self):
        # Create pointers and directories
        self.assets_dir = os.path.join("assets")
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "font")
        self.gui_dir = os.path.join(self.assets_dir, "gui")

        self.font = {
            # Menu
            "arial 10": pygame.font.SysFont('Arial', 10),
            "arial 20": pygame.font.SysFont('Arial', 20),
            "arial 30": pygame.font.SysFont('Arial', 30),
            "arial 40": pygame.font.SysFont('Arial', 40),
            "arial 50": pygame.font.SysFont('Arial', 50),
            "arial 60": pygame.font.SysFont('Arial', 60),
            "arial 70": pygame.font.SysFont('Arial', 70),
            "arial 80": pygame.font.SysFont('Arial', 80),
            "arial bold 10": pygame.font.SysFont('Arial', 10, True),
            "arial bold 20": pygame.font.SysFont('Arial', 20, True),
            "arial bold 30": pygame.font.SysFont('Arial', 30, True),
            "arial bold 40": pygame.font.SysFont('Arial', 40, True),
            "arial bold 50": pygame.font.SysFont('Arial', 50, True),
            "arial bold 60": pygame.font.SysFont('Arial', 60, True),
            "arial bold 70": pygame.font.SysFont('Arial', 70, True),
            "arial bold 80": pygame.font.SysFont('Arial', 80, True),
            "arial italic 10": pygame.font.SysFont('Arial', 10),
            "arial italic 20": pygame.font.SysFont('Arial', 20),
            "arial italic 30": pygame.font.SysFont('Arial', 30),
            "arial italic 40": pygame.font.SysFont('Arial', 40),
            "arial italic 50": pygame.font.SysFont('Arial', 50),
            "arial italic 60": pygame.font.SysFont('Arial', 60),
            "arial italic 70": pygame.font.SysFont('Arial', 70),
            "arial italic 80": pygame.font.SysFont('Arial', 80),
            # Game
            "custom1 10": pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 10),
            "custom1 20": pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 20),
            "custom1 30": pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 30),
            "custom1 40": pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 40),
            "custom1 50": pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 50),
            "custom1 60": pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 60),
            "custom1 70": pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 70),
            "custom1 80": pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 80),
        }

    def load_states(self):
        title_screen = Title(self)
        self.state_stack.append(title_screen)

    def __set_supported_resolutions__(self):
        self.r_16_10 = {"HD": (1440, 900), "HD+": (1680, 1050), "FHD": (1920, 1200),
                        "QHD": (2560, 1600), "4k": (3840, 2400)}
        self.r_16_9 = {"HD": (1280, 720), "HD+": (1600, 900), "FHD": (1920, 1080),
                       "QHD": (2560, 1440), "4k": (3840, 2160)}
        self.r_21_9 = {"HD": (1720, 720), "FHD": (2560, 1080), "QHD": (3440, 1440), "4k": (5120, 2160)}
        self.r_32_9 = {"FHD": (3840, 1080), "QHD": (5120, 1440), "4k": (7680, 2160)}

        self.supported_resolutions = {"16:10": self.r_16_10, "16:9": self.r_16_9,
                                      "21:9": self.r_21_9, "32:9": self.r_32_9}

    # --------------------------------------------------------------------------------------------------

    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

            self.clock.tick(self.framerate)  # by this it caps at the target frame rate

    # Update the topmost state
    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)

    # Render the topmost state
    def render(self):
        self.state_stack[-1].render(self.game_canvas)

        self.display_stats(self.game_canvas)
        self.screen.blit(
            pygame.transform.scale(self.game_canvas, (self.screen.get_width(), self.screen.get_height())), (0, 0))
        pygame.display.flip()

    def get_events(self):
        InputEvents.get_events(self)

    def reset_keys(self):
        InputEvents.reset_keys(self)


if __name__ == '__main__':
    g = Game()
    while g.running:
        g.game_loop()
