import tkinter
import settings

ROW_HEIGHT = 28
BG_COLOR = "black"
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


def get_stat_color(stat: settings.STAT, value: int) -> str:
    if stat == settings.STAT.WINRATE:
        if value == -1:
            return "white"
        if value < 45:
            return "red"
        if value < 48:
            return "orange"
        if value < 52:
            return "yellow"
        if value < 55:
            return "green"
        if value < 60:
            return "cyan"
        return "purple"
    if stat == settings.STAT.LEVEL:
        if value == -1:
            return "white"
        if value < 5:
            return "red"
        if value < 20:
            return "orange"
        if value < 40:
            return "yellow"
        if value < 60:
            return "green"
        if value < 100:
            return "cyan"
        return "purple"
    if stat == settings.STAT.TIME_FIGHTER or stat == settings.STAT.TIME_ATTACKER or stat == settings.STAT.TIME_TANKS or stat == settings.STAT.TIME_ANTI_AIR:
        if value == -1:
            return "white"
        if value < 3600:
            return "red"
        if value < 3600 * 24:
            return "orange"
        if value < 3600 * 24 * 5:
            return "yellow"
        if value < 3600 * 24 * 15:
            return "green"
        if value < 3600 * 24 * 50:
            return "cyan"
        return "purple"
    return "white"


def format_time(value: int) -> str:
    if value == -1:
        return "N/A"
    if value < 3600:
        return str(round(value / 60)) + "m"
    if value < 3600 * 24:
        return str(round(value / 3600)) + "h"
    return str(round(value / 3600 / 24)) + "d"


def get_stat_window_geometry(stat: settings.STAT, blue_team: bool) -> str:
    return str(INDENTS[settings.resolution]["WIDTH_BY_STAT"][stat]) + 'x' + \
           str(INDENTS[settings.resolution]["SCREENSHOT_HEIGHT"]) + '+' + \
           str(INDENTS[settings.resolution]["X_BY_STAT_BLUE" if blue_team else "X_BY_STAT_RED"][stat]) + '+' + \
           str(INDENTS[settings.resolution]["Y_DEFAULT"] - 20)


class Player:
    def __init__(self, name: str, uid: int, team: str):
        self.name: str = name
        self.uid: int = uid
        self.team: str = team
        self.slots: dict[str, dict[str, int]] = dict()
        self.cur_row: int = -1
        self.loaded: bool = False
        self.stat: dict[settings.STAT, int] = dict()
        for stat in settings.viewed_stat:
            self.stat[stat] = -1

    def set_stat(self, stat: settings.STAT, value: int) -> None:
        self.stat[stat] = value

    def get_stat(self, stat: settings.STAT) -> int:
        return self.stat[stat]

    def show_stat(self, row: int) -> None:
        self.cur_row = row
        root_dict: dict = data.blue_windows if self.team == data.host_player_team else data.red_windows
        for stat in settings.viewed_stat:
            value = self.get_stat(stat)
            color = get_stat_color(stat, value)
            if stat == settings.STAT.TIME_FIGHTER or stat == settings.STAT.TIME_ATTACKER or stat == settings.STAT.TIME_TANKS or stat == settings.STAT.TIME_ANTI_AIR:
                label: str = format_time(value)
            else:
                label: str = str(value)
            tkinter.Label(root_dict[stat], text=label, bg=BG_COLOR, fg=color).place(x=0, y=30 + row * ROW_HEIGHT)


class Data:
    def __init__(self):
        self.host_player_id: int = -1
        self.host_player_team: int = -1
        self.team_1: list[Player | None] = []
        self.team_2: list[Player | None] = []
        self.difficulty: str = ""
        self.currently_in_tab: bool = False
        self.blue_windows: dict[settings.STAT, tkinter.Tk] = dict()
        self.red_windows: dict[settings.STAT, tkinter.Tk] = dict()
        self.indicator_window: tkinter.Tk = tkinter.Tk()
        width, height = tuple(map(int, settings.resolution.value.split('x')))
        self.indicator_window.geometry("5x40+" + str(width - 5) + "+" + str(height - 40))
        self.indicator_window.resizable(False, False)
        self.indicator_window.overrideredirect(True)
        self.indicator_window.configure(background="red")
        self.indicator_window.update()

    def add_player(self, name: str, uid: int, team: str) -> None:
        for player in self.get_players():
            if player.uid == uid:
                return
        if team == '1':
            self.team_1.append(Player(name, uid, team))
        else:
            self.team_2.append(Player(name, uid, team))

    def get_players(self) -> list[Player]:
        return self.team_1 + self.team_2

    def get_players_to_load(self) -> list[Player]:
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
            tkinter.Label(self.blue_windows[stat], text=stat.value, bg=BG_COLOR, fg="white").place(x=0, y=0)

            self.red_windows[stat] = tkinter.Tk()
            self.red_windows[stat].geometry(get_stat_window_geometry(stat, False))
            self.red_windows[stat].resizable(False, False)
            self.red_windows[stat].overrideredirect(True)
            self.red_windows[stat].wait_visibility(self.red_windows[stat])
            self.red_windows[stat].wm_attributes("-alpha", 0.5)
            self.red_windows[stat].configure(background=BG_COLOR)
            tkinter.Label(self.red_windows[stat], text=stat.value, bg=BG_COLOR, fg="white").place(x=0, y=0)

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


data: Data = Data()
