import json
import os
import time
from dataclasses import dataclass, asdict
from datetime import time

import psutil


class Files:
    @staticmethod
    def index_files(path: str, suffix="*"):
        # path = r".\config\settings"
        configList = []

        for item in os.listdir(path):
            if suffix == "*":
                configList.append({"name": item, "path": os.path.abspath(os.path.join(path, item))})
            else:
                # Correct suffix
                if suffix.find(".") == -1:
                    suffix = f".{suffix}"
                    print(suffix)
                # find matching files
                if item.find(suffix) != -1:
                    configList.append({"name": item, "path": os.path.abspath(os.path.join(path, item))})
        return configList

    @staticmethod
    def CVTpython2json(config: dataclass()):
        # config py -> config json
        return str(asdict(config)).replace("'", "\"").replace("True", "true").replace("False", "false").replace("None",
                                                                                                                "null")

    @staticmethod
    def write2Json(json_string: str, json_file_name: str):
        file = open(json_file_name, "w")
        file.write(json_string)
        file.close()

    @staticmethod
    def CVTjson2python(path: str):
        # config json -> config py
        file = open(path)
        data = json.load(file)
        file.close()
        return data


class Pygame:
    @staticmethod
    def draw_text(surface, text: str, font_dir: dir, color, x, y, font_type="", aa=False, background=None,
                  colorkey=False,
                  keycolor=(0, 0, 0), alignment="midtop"):
        text_surface = font_dir[font_type].render(text, aa, color, background)
        if colorkey:
            text_surface.set_colorkey(keycolor)

        align = (
            "topleft", "bottomleft", "topright", "bottomright", "midtop", "midleft", "midbottom", "midright", "center")
        text_rect = text_surface.get_rect()
        for item in align:
            if alignment == item:
                setattr(text_rect, item, (x, y))
        surface.blit(text_surface, text_rect)

    @staticmethod
    def display_stats(surface, fps: float, gres, sres, pid, max_framerate, frames_passed):
        fps = " FPS: " + str(round(fps, 1))
        g_res = " Game: " + str(int(gres[0])) + "×" + str(int(gres[1]))
        s_res = " Screen: " + str(int(sres[0])) + "×" + str(int(sres[1]))
        # do every 3 seconds for performance reasons
        if frames_passed == max_framerate * 3 or frames_passed == 0:
            cpu = " CPU: " + str(round(pid.cpu_percent() / psutil.cpu_count(False), 1)) + " %"
            ram = " RAM: " + str(round((pid.memory_full_info()[12] - 1000000) * 10 ** -6, 1)) + " MB"
            Pygame.draw_text(surface, cpu, "white", gres[0], 45, "arial 30", background="orange", alignment="topright")
            Pygame.draw_text(surface, ram, "white", gres[0], 85, "arial 30", background="red", alignment="topright")
            # reset frames_passed
            frames_passed = 1

        Pygame.draw_text(surface, fps, "white", gres[0], 5, "arial 30", background="darkgreen", alignment="topright")
        Pygame.draw_text(surface, g_res, "white", gres[0], 125, "arial 30", background="blue", alignment="topright")
        Pygame.draw_text(surface, s_res, "white", gres[0], 165, "arial 30", background="blue", alignment="topright")
        # iterate frames_passed
        frames_passed += 1
        return frames_passed


class Calculate:
    @staticmethod
    def get_dt(previous_time):
        now = time.time()
        dt = now - previous_time
        previous_time = now
        return {"dt": dt, "previous_time": previous_time}
