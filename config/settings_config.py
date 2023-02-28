import datetime
from dataclasses import dataclass

import functions, config.startup_config as startup_config


'''
Graphics ----------------------------------------------------------
Hierarchy:
                 Video
                   ↓    
                Display
'''


@dataclass
class _Display:
    aspect: str
    resolution_w: int
    resolution_h: int


@dataclass
class _Video:
    screen: _Display
    game: _Display
    fullscreen: bool
    max_framerate: int
    gui_scale: int


'''
Keybindings ----------------------------------------------------------
Hierarchy:
              Keybindings
                   ↓    
                Controls
                   ↓    
        Movement, Ability, MenusEtc

'''


@dataclass
class _Movement:
    up: str = None
    left: str = None
    down: str = None
    right: str = None
    sprint: str = None


@dataclass
class _Ability:
    main: str = None
    secondary: str = None
    use: str = None
    reload: str = None


@dataclass
class _MenusEtc:
    inventory: str = None
    pause_close: str = None


@dataclass
class _Controls:
    movement: _Movement
    ability: _Ability
    menusEtc: _MenusEtc


@dataclass
class _Keybindings:
    keyboard: _Controls
    mouse: _Controls
    # Joystick: Controls


'''
Top Layer Config ----------------------------------------------------------
Hierarchy:
                Settings
                   ↓    
        Video, Audio, Keybindings

'''


@dataclass
class Settings:
    title: str
    last_edited: str
    video: _Video
    # Audio: Audio TODO
    keybindings: _Keybindings


# FUNCTIONS --------------------------------------------------------

def __init__(startup_conf: startup_config.Startup):
    config_list = functions.Files.index_files(".\config\settings", ".json")
    print(config_list)

    # No Config file -> create new DEFAULT file
    if len(config_list) < 1:
        cfg = new_python_config("new_config", config_list)

    # Load config
    else:
        data = functions.Files.CVTjson2python(startup_conf.settings_config_path)
        cfg = write2Python(new_python_config("new_config", config_list), data)
    return cfg


def write2Python(cfg: Settings, data: dict):
    for key, value in data.items():
        recurse = (
            "video", "screen", "game", "audio", "keybindings", "keyboard", "mouse", "movement", "ability", "menusEtc")
        if key in recurse:
            write2Python(cfg, value)
        else:
            match key:
                case "title":
                    cfg.title = value
                case "last_edited":
                    cfg.last_edited = value
                # Video
                case "aspect":
                    cfg.aspect = value
                case "resolution_w":
                    cfg.resolution_w = value
                case "resolution_h":
                    cfg.resolution_h = value
                case "fullscreen":
                    cfg.fullscreen = value
                case "max_framerate":
                    cfg.max_framerate = value
                case "gui_scale":
                    cfg.gui_scale = value
                # Movement
                case "up":
                    cfg.up = value
                case "left":
                    cfg.left = value
                case "down":
                    cfg.down = value
                case "right":
                    cfg.right = value
                case "sprint":
                    cfg.sprint = value
                # Ability
                case "main":
                    cfg.main = value
                case "secondary":
                    cfg.secondary = value
                case "use":
                    cfg.use = value
                case "reload":
                    cfg.reload = value
                case "inventory":
                    cfg.inventory = value
                case "pause_close":
                    cfg.pause_close = value
    return cfg


def new_python_config(title: str, config_list: []):
    title = f"SETTINGS_{title}"

    if len(config_list) < 1:
        cfg_vid = _Video(_Display("", 0, 0), _Display("", 0, 0), False, 0, 0)
        cfg_controls = _Controls(_Movement(), _Ability(), _MenusEtc())
        cfg_binds = _Keybindings(cfg_controls, cfg_controls)
        cfg = Settings(title, str(datetime.datetime.now()), cfg_vid, cfg_binds)
        return cfg

    i = 0
    found = False
    while True:
        for item in config_list:
            if item["name"] == title:
                i = i + 1
                title = title + f"_{i}"
                found = True

        if found is False:
            cfg_vid = _Video(_Display("", 0, 0), _Display("", 0, 0), False, 0, 0)
            cfg_controls = _Controls(_Movement(), _Ability(), _MenusEtc())
            cfg_binds = _Keybindings(cfg_controls, cfg_controls)
            cfg = Settings(title, str(datetime.datetime.now()), cfg_vid, cfg_binds)
            return cfg
