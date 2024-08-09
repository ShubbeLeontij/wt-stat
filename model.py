import tkinter
import settings

ROW_HEIGHT = 28
BG_COLOR = 'black'
INDENTS = \
{
    settings.ScreenResolutions.r1920x1080:
    {
        "Y_DEFAULT": 470,
        "SCREENSHOT_WIDTH": 350,
        "SCREENSHOT_HEIGHT": 500,
        "SCREENSHOT_BLUE_X": 930,
        "SCREENSHOT_RED_X": 1280,
        "X_BY_STAT_BLUE":
        {
            settings.STAT.LEVEL: 930,
            settings.STAT.WINS: 0,
            settings.STAT.BATTLES: 0,
            settings.STAT.WINRATE: 570,
            settings.STAT.TIME_FIGHTER: 420,
            settings.STAT.TIME_ATTACKER: 320,
            settings.STAT.TIME_TANKS: 240,
            settings.STAT.TIME_ANTI_AIR: 160
        },
        "X_BY_STAT_RED":
        {
            settings.STAT.LEVEL: 1570,
            settings.STAT.WINS: 0,
            settings.STAT.BATTLES: 0,
            settings.STAT.WINRATE: 1730,
            settings.STAT.TIME_FIGHTER: 1900,
            settings.STAT.TIME_ATTACKER: 2060,
            settings.STAT.TIME_TANKS: 2170,
            settings.STAT.TIME_ANTI_AIR: 2280
        },
        "WIDTH_BY_STAT":
        {
            settings.STAT.LEVEL: 50,
            settings.STAT.WINS: 50,
            settings.STAT.BATTLES: 50,
            settings.STAT.WINRATE: 50,
            settings.STAT.TIME_FIGHTER: 50,
            settings.STAT.TIME_ATTACKER: 50,
            settings.STAT.TIME_TANKS: 50,
            settings.STAT.TIME_ANTI_AIR: 50
        }
    },
    settings.ScreenResolutions.r2560x1440:
    {
        "Y_DEFAULT": 470,
        "SCREENSHOT_WIDTH": 350,
        "SCREENSHOT_HEIGHT": 500,
        "SCREENSHOT_BLUE_X": 930,
        "SCREENSHOT_RED_X": 1280,
        "X_BY_STAT_BLUE":
        {
            settings.STAT.LEVEL: 930,
            settings.STAT.WINS: 0,
            settings.STAT.BATTLES: 0,
            settings.STAT.WINRATE: 570,
            settings.STAT.TIME_FIGHTER: 420,
            settings.STAT.TIME_ATTACKER: 320,
            settings.STAT.TIME_TANKS: 240,
            settings.STAT.TIME_ANTI_AIR: 160
        },
        "X_BY_STAT_RED":
        {
            settings.STAT.LEVEL: 1570,
            settings.STAT.WINS: 0,
            settings.STAT.BATTLES: 0,
            settings.STAT.WINRATE: 1730,
            settings.STAT.TIME_FIGHTER: 1900,
            settings.STAT.TIME_ATTACKER: 2060,
            settings.STAT.TIME_TANKS: 2170,
            settings.STAT.TIME_ANTI_AIR: 2280
        },
        "WIDTH_BY_STAT":
        {
            settings.STAT.LEVEL: 50,
            settings.STAT.WINS: 50,
            settings.STAT.BATTLES: 50,
            settings.STAT.WINRATE: 50,
            settings.STAT.TIME_FIGHTER: 50,
            settings.STAT.TIME_ATTACKER: 50,
            settings.STAT.TIME_TANKS: 50,
            settings.STAT.TIME_ANTI_AIR: 50
        }
    }
}


def get_stat_color(stat: settings.STAT, value: str) -> str:
    if stat == settings.STAT.WINRATE:
        if value == 'N/A':
            return 'white'
        percents: int = int(value[:-1])
        if percents < 45:
            return 'red'
        if percents < 48:
            return 'orange'
        if percents < 52:
            return 'yellow'
        if percents < 55:
            return 'green'
        if percents < 60:
            return 'cyan'
        return 'purple'
    if stat == settings.STAT.LEVEL:
        if value == 'N/A' or value == "":
            return 'white'
        percents: int = int(value)
        if percents < 5:
            return 'red'
        if percents < 20:
            return 'orange'
        if percents < 40:
            return 'yellow'
        if percents < 60:
            return 'green'
        if percents < 100:
            return 'cyan'
        return 'purple'
    if stat == settings.STAT.TIME_FIGHTER or stat == settings.STAT.TIME_ATTACKER or stat == settings.STAT.TIME_TANKS or stat == settings.STAT.TIME_ANTI_AIR:
        if value == 'N/A':
            return 'white'
        index: int = value.find("д" if settings.lang == settings.Languages.RU else "d")
        if index == -1:  # Less than a day
            if value[:value.find("ч" if settings.lang == settings.Languages.RU else "h")] == "0":  # Less than an hour
                return 'red'
            return 'orange'
        days: int = int(value[:index])
        if days < 5:
            return 'yellow'
        if days < 15:
            return 'green'
        if days < 50:
            return 'cyan'
        return 'purple'
    return 'white'


def get_stat_window_geometry(stat: settings.STAT, blue_team: bool) -> str:
    return str(INDENTS[settings.resolution]["WIDTH_BY_STAT"][stat]) + 'x' + \
           str(INDENTS[settings.resolution]["SCREENSHOT_HEIGHT"]) + '+' + \
           str(INDENTS[settings.resolution]["X_BY_STAT_BLUE" if blue_team else "X_BY_STAT_RED"][stat]) + '+' + \
           str(INDENTS[settings.resolution]["Y_DEFAULT"] - 20)


class Player:
    def __init__(self, name: str, team: str):
        self.name: str = name
        self.team: str = team
        self.loaded: bool = False
        self.stat: dict = dict()
        for stat in settings.viewed_stat:
            self.stat[stat] = "N/A"

    def set_stat(self, stat: settings.STAT, value: str) -> None:
        self.stat[stat] = value

    def get_stat(self, stat: settings.STAT) -> str:
        return self.stat[stat]

    def show_stat(self, row: int) -> None:
        root_dict: dict = DATA.blue_windows if self.team == DATA.host_player.team else DATA.red_windows
        for stat in settings.viewed_stat:
            value = self.get_stat(stat)
            color = get_stat_color(stat, value)
            value.replace("мин", "м")
            tkinter.Label(root_dict[stat], text=value, bg=BG_COLOR, fg=color).place(x=0, y=30 + row * ROW_HEIGHT)


class Data:
    def __init__(self):
        self.host_player = None
        self.team_1 = []
        self.team_2 = []
        self.diff_number = -1
        self.currently_in_tab = False
        self.blue_windows = dict()
        self.red_windows = dict()
        self.indicator_window = tkinter.Tk()
        width, height = tuple(map(int, settings.resolution.value.split('x')))
        self.indicator_window.geometry("5x40+" + str(width - 5) + "+" + str(height - 40))
        self.indicator_window.resizable(False, False)
        self.indicator_window.overrideredirect(True)
        self.indicator_window.configure(background='red')
        self.indicator_window.update()

    def add_player(self, name: str, team: str) -> None:
        if name == self.host_player.name:
            self.host_player.team = team
        for player in self.get_players():
            if player.name == name:
                return
        if team == '1':
            self.team_1.append(Player(name, team))
        else:
            self.team_2.append(Player(name, team))

    def get_players(self) -> list:
        return self.team_1 + self.team_2

    def get_players_to_load(self) -> list:
        result: list = []
        for player in self.get_players():
            if not player.loaded:
                result.append(player)
        return result

    def get_player(self, name: str) -> Player | None:
        for player in self.get_players():
            if player.name == name:
                return player
        return None

    def init_windows(self) -> None:
        self.delete_windows()
        for stat in settings.viewed_stat:
            self.blue_windows[stat] = tkinter.Tk()
            self.blue_windows[stat].geometry(get_stat_window_geometry(stat, True))
            self.blue_windows[stat].resizable(False, False)
            self.blue_windows[stat].overrideredirect(True)
            self.blue_windows[stat].wait_visibility(self.blue_windows[stat])
            self.blue_windows[stat].wm_attributes("-alpha", 0.5)
            self.blue_windows[stat].configure(background=BG_COLOR)
            tkinter.Label(self.blue_windows[stat], text=stat.value, bg=BG_COLOR, fg='white').place(x=0, y=0)

            self.red_windows[stat] = tkinter.Tk()
            self.red_windows[stat].geometry(get_stat_window_geometry(stat, False))
            self.red_windows[stat].resizable(False, False)
            self.red_windows[stat].overrideredirect(True)
            self.red_windows[stat].wait_visibility(self.red_windows[stat])
            self.red_windows[stat].wm_attributes("-alpha", 0.5)
            self.red_windows[stat].configure(background=BG_COLOR)
            tkinter.Label(self.red_windows[stat], text=stat.value, bg=BG_COLOR, fg='white').place(x=0, y=0)

    def show_windows(self) -> None:
        for stat in settings.viewed_stat:
            try:
                self.blue_windows[stat].update()
                self.red_windows[stat].update()
            except:
                pass

    def delete_windows(self) -> None:
        for stat in settings.viewed_stat:
            try:
                self.blue_windows[stat].destroy()
                self.red_windows[stat].destroy()
            except:
                pass

    def set_state_color(self, color: str) -> None:
        try:
            self.indicator_window.configure(background=color)
            self.indicator_window.update()
        except:
            pass


DATA: Data = Data()
