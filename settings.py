import enum
from pynput import keyboard


class STAT(enum.Enum):
    LEVEL = "LVL"
    WINS = "Wins"
    BATTLES = "Battles"
    WINRATE = "WR"
    TIME_FIGHTER = "Fighter"
    TIME_ATTACKER = "CAS"
    TIME_TANKS = "Tank"
    TIME_ANTI_AIR = "AA"


class Readers(enum.Enum):
    READER_CN = 0
    READER_RU = 1
    READER_CN_AND_RU = 2  # Recommended but will take double time


class Languages(enum.Enum):
    RU = "ru"
    EN = "en"


class ScreenResolutions(enum.Enum):
    r2560x1440 = "2560x1440"
    r1920x1080 = "1920x1080"


# HERE SETTINGS START

chrome_version: int = 133
readers: Readers = Readers.READER_CN_AND_RU
lang: Languages = Languages.EN
resolution: ScreenResolutions = ScreenResolutions.r2560x1440
clog_path: str = "~/.config/WarThunder/.game_logs/"  # "~/.config/WarThunder/.game_logs/" is default for Linux
viewed_stat: list = [STAT.WINRATE, STAT.TIME_FIGHTER, STAT.TIME_ATTACKER, STAT.TIME_TANKS, STAT.TIME_ANTI_AIR, STAT.LEVEL]
load_button: keyboard.Key = keyboard.Key.down
show_button: keyboard.Key = keyboard.Key.up
ocr_logging_enabled: bool = True
retry_to_get_all_stats: bool = True
