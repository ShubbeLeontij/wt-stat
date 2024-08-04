import time
import easyocr
import numpy as np
import pyautogui
import difflib
import tkinter
import model
import settings
import warnings
warnings.filterwarnings("ignore")


if settings.readers == settings.readers.READER_RU:
    readers: list = [easyocr.Reader(['ru', 'en'])]
elif settings.readers == settings.readers.READER_CN:
    readers: list = [easyocr.Reader(['ch_sim', 'en'])]
else:
    readers: list = [easyocr.Reader(['ch_sim', 'en']), easyocr.Reader(['ru', 'en'])]


def read() -> None:
    logstr: str = '\n' + str(time.time()) + '\n'
    model.DATA.init_windows()
    pyautogui.screenshot(region=model.DATA.INDENTS_BLUE).save("screen_blue.png")
    pyautogui.screenshot(region=model.DATA.INDENTS_RED).save("screen_red.png")
    result: list = []
    for reader in readers:
        result += reader.readtext("screen_blue.png")
    if len(result) != 0:
        for player in (model.DATA.team_1 if model.DATA.host_player.team == '1' else model.DATA.team_2):
            max_ratio = 0.0
            best_item = result[0]
            for item in result:
                ratio = difflib.SequenceMatcher(None, player.name.split('@')[0], item[1]).ratio()
                if max_ratio < ratio:
                    max_ratio = ratio
                    best_item = item
            view(player, best_item[0])
            logstr += player.name + ' ' + str(best_item[2]) + ' ' + str(max_ratio) + '\n'
    result: list = []
    for reader in readers:
        result += reader.readtext("screen_red.png")
    if len(result) != 0:
        for player in (model.DATA.team_2 if model.DATA.host_player.team == '1' else model.DATA.team_1):
            max_ratio = 0.0
            best_item = result[0]
            for item in result:
                ratio = difflib.SequenceMatcher(None, player.name.split('@')[0], item[1]).ratio()
                if max_ratio < ratio:
                    max_ratio = ratio
                    best_item = item
            view(player, best_item[0])
            logstr += player.name + ' ' + str(best_item[2]) + ' ' + str(max_ratio) + '\n'
    with open('logs.txt', 'a') as file:
        file.write(logstr)
    model.DATA.show_windows()


def view(player: model.Player, coords: np.array) -> None:
    row: int = int(coords[0][1]) // 28
    winrate: str = player.get_stat(model.STAT.WINRATE)
    fighter_time: str = player.get_stat(model.STAT.TIME_FIGHTER)
    if player.team == model.DATA.host_player.team:
        tkinter.Label(model.DATA.blue_windows[model.STAT.WINRATE], text=winrate, bg=model.DATA.BG_COLOR, fg=model.get_winrate_color(winrate)).place(x=0, y=30 + row * 28)
        tkinter.Label(model.DATA.blue_windows[model.STAT.TIME_FIGHTER], text=fighter_time, bg=model.DATA.BG_COLOR, fg=model.get_fighter_time_color(fighter_time)).place(x=0, y=30 + row * 28)
    else:
        tkinter.Label(model.DATA.red_windows[model.STAT.WINRATE], text=winrate, bg=model.DATA.BG_COLOR, fg=model.get_winrate_color(winrate)).place(x=0, y=30 + row * 28)
        tkinter.Label(model.DATA.red_windows[model.STAT.TIME_FIGHTER], text=fighter_time, bg=model.DATA.BG_COLOR, fg=model.get_fighter_time_color(fighter_time)).place(x=0, y=30 + row * 28)
