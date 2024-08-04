import enum


class Readers(enum.Enum):
    READER_CN = 0
    READER_RU = 1
    READER_CN_AND_RU = 2


class Languages(enum.Enum):
    RU = "RU"
    EN = "EN"


class ScreenResolutions(enum.Enum):
    r2560x1440 = "2560x1440"
    r1920x1080 = "1920x1080"


# HERE SETTINGS START

chrome_version: int = 126
readers: Readers = Readers.READER_CN_AND_RU
lang: Languages = Languages.RU
resolution: ScreenResolutions = ScreenResolutions.r2560x1440
clog_path: str = "~/.config/WarThunder/.game_logs/"  # "~/.config/WarThunder/.game_logs/" is default for Linux
