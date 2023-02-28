import datetime
from dataclasses import dataclass

import functions


@dataclass
class Startup:
    last_edited: str
    settings_config_path: str


def __init__():
    # Search folder for configs
    configList = functions.Files.index_files(".\config", ".json")
    print(configList)
    # No Config file -> create new file
    if len(configList) < 1:
        return new_python_config()
    # Load config
    else:
        for item in configList:
            if item["name"] == "STARTUP_CONF.json":
                data = functions.Files.CVTjson2python(item["path"])
                cfg = write2Python(new_python_config(), data)
            else:
                cfg = new_python_config()
            functions.Files.write2Json(functions.Files.CVTpython2json(cfg), ".\config\STARTUP_CONF.json")
            return cfg


def write2Python(cfg: Startup, data: dict) -> object:
    for key, value in data.items():
        match key:
            case "last_edited":
                cfg.last_edited = value
            case "settings_config_path":
                cfg.settings_config_path = value
    return cfg


def new_python_config():
    cfg = Startup(str(datetime.datetime.now()), "E:\Coding\Python\pygame\defendGame\config\settings\DEFAULT.json")
    return cfg
