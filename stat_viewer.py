import time
import easyocr
import pyautogui
import difflib
import model
import settings
import warnings
warnings.filterwarnings("ignore")


if settings.readers == settings.readers.READER_RU:
    readers = [easyocr.Reader(["ru", "en"])]
elif settings.readers == settings.readers.READER_CN:
    readers = [easyocr.Reader(["ch_sim", "en"])]
else:
    readers = [easyocr.Reader(["ch_sim", "en"]), easyocr.Reader(["ru", "en"])]


def read() -> None:
    if settings.ocr_logging_enabled:
        with open("logs.txt", 'a') as file:
            file.write('\n' + str(time.time()) + '\n')
    pyautogui.screenshot(region=(model.INDENTS[settings.resolution]["SCREENSHOT_BLUE_X"], model.INDENTS[settings.resolution]["Y_DEFAULT"],
                                 model.INDENTS[settings.resolution]["SCREENSHOT_WIDTH"], model.INDENTS[settings.resolution]["SCREENSHOT_HEIGHT"])).save("screen_blue.png")
    pyautogui.screenshot(region=(model.INDENTS[settings.resolution]["SCREENSHOT_RED_X"], model.INDENTS[settings.resolution]["Y_DEFAULT"],
                         model.INDENTS[settings.resolution]["SCREENSHOT_WIDTH"], model.INDENTS[settings.resolution]["SCREENSHOT_HEIGHT"])).save("screen_red.png")
    model.data.init_windows()
    result = []
    for reader in readers:
        result += reader.readtext("screen_blue.png")
    if len(result) != 0:
        for player in (model.data.team_1 if model.data.host_player_team == '1' else model.data.team_2):
            find_best(player, result)
    result = []
    for reader in readers:
        result += reader.readtext("screen_red.png")
    if len(result) != 0:
        for player in (model.data.team_2 if model.data.host_player_team == '1' else model.data.team_1):
            find_best(player, result)
    model.data.show_windows()


def find_best(player: model.Player, result) -> None:
    max_ratio = 0.0
    best_item = result[0]
    for item in result:
        ratio = difflib.SequenceMatcher(None, player.name.split('@')[0], item[1]).ratio()  # this cuts @psn suffix
        if max_ratio < ratio:
            max_ratio = ratio
            best_item = item
    player.show_stat(row=int(best_item[0][0][1]) // model.ROW_HEIGHT)
    if settings.ocr_logging_enabled:
        with open("logs.txt", 'a') as file:
            file.write(player.name + ' ' + str(best_item[2]) + ' ' + str(max_ratio) + '\n')


