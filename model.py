import enum
import tkinter
import settings


class STAT(enum.Enum):
    WINS = "WINS"
    BATTLES = "BATTLES"
    WINRATE = "WINRATE"
    TIME_FIGHTER = "TIME_FIGHTER"
    TIME_ATTACKER = "TIME_ATTACKER"


def get_winrate_color(winrate: str) -> str:
    if winrate == 'N/A':
        return 'white'
    percents: int = int(winrate[:-1])
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


def get_fighter_time_color(fighter_time: str) -> str:
    if fighter_time == 'N/A':
        return 'white'
    index: int = fighter_time.find("д") if settings.lang == settings.Languages.RU else fighter_time.find("d")
    if index == -1:  # Less than a day
        return 'red'
    days: int = int(fighter_time[:index])
    if days < 5:
        return 'yellow'
    if days < 15:
        return 'green'
    if days < 50:
        return 'cyan'
    return 'purple'


class Player:
    def __init__(self, name, team):
        self.name: str = name
        self.team: str = team
        self.stat: dict = dict()
        self.stat[STAT.WINS] = self.stat[STAT.BATTLES] = self.stat[STAT.BATTLES] = self.stat[STAT.TIME_FIGHTER] = self.stat[STAT.TIME_ATTACKER] = self.stat[STAT.WINRATE] = "N/A"

    def set_stat(self, stat: STAT, value: str) -> None:
        self.stat[stat] = value

    def get_stat(self, stat: STAT) -> str:
        return self.stat[stat]


class Data:
    INDENTS = 930, 470, 700, 500
    INDENTS_BLUE = 930, 470, 350, 500
    INDENTS_RED = 1280, 470, 350, 500
    ROW_HEIGHT = 28
    BG_COLOR = 'black'

    def __init__(self):
        self.host_player = None
        self.team_1 = []
        self.team_2 = []
        self.diff_number = -1
        self.currently_in_tab = False
        self.blue_windows = dict()
        self.red_windows = dict()
        self.indicator_window = tkinter.Tk()
        self.indicator_window.geometry("5x40+2555+1400")
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

    def get_player(self, name: str) -> Player | None:
        for player in self.get_players():
            if player.name == name:
                return player
        return None

    def init_windows(self) -> None:
        self.delete_windows()
        self.blue_windows[STAT.WINRATE] = tkinter.Tk()
        self.blue_windows[STAT.WINRATE].geometry("40x" + str(self.INDENTS[3]) + "+600+" + str(self.INDENTS[1] - 20))
        self.blue_windows[STAT.WINRATE].resizable(False, False)
        self.blue_windows[STAT.WINRATE].overrideredirect(True)
        self.blue_windows[STAT.WINRATE].wait_visibility(self.blue_windows[STAT.WINRATE])
        self.blue_windows[STAT.WINRATE].wm_attributes("-alpha", 0.5)
        self.blue_windows[STAT.WINRATE].configure(background=self.BG_COLOR)
        tkinter.Label(self.blue_windows[STAT.WINRATE], text='WR', bg=self.BG_COLOR, fg='white').place(x=0, y=0)

        self.blue_windows[STAT.TIME_FIGHTER] = tkinter.Tk()
        self.blue_windows[STAT.TIME_FIGHTER].geometry("70x" + str(self.INDENTS[3]) + "+420+" + str(self.INDENTS[1] - 20))
        self.blue_windows[STAT.TIME_FIGHTER].resizable(False, False)
        self.blue_windows[STAT.TIME_FIGHTER].overrideredirect(True)
        self.blue_windows[STAT.TIME_FIGHTER].wait_visibility(self.blue_windows[STAT.TIME_FIGHTER])
        self.blue_windows[STAT.TIME_FIGHTER].wm_attributes("-alpha", 0.5)
        self.blue_windows[STAT.TIME_FIGHTER].configure(background=self.BG_COLOR)
        tkinter.Label(self.blue_windows[STAT.TIME_FIGHTER], text='Fighter', bg=self.BG_COLOR, fg='white').place(x=0, y=0)

        self.red_windows[STAT.WINRATE] = tkinter.Tk()
        self.red_windows[STAT.WINRATE].geometry("40x" + str(self.INDENTS[3]) + "+1740+" + str(self.INDENTS[1] - 20))
        self.red_windows[STAT.WINRATE].resizable(False, False)
        self.red_windows[STAT.WINRATE].overrideredirect(True)
        self.red_windows[STAT.WINRATE].wait_visibility(self.red_windows[STAT.WINRATE])
        self.red_windows[STAT.WINRATE].wm_attributes("-alpha", 0.5)
        self.red_windows[STAT.WINRATE].configure(background=self.BG_COLOR)
        tkinter.Label(self.red_windows[STAT.WINRATE], text='WR', bg=self.BG_COLOR, fg='white').place(x=0, y=0)

        self.red_windows[STAT.TIME_FIGHTER] = tkinter.Tk()
        self.red_windows[STAT.TIME_FIGHTER].geometry("70x" + str(self.INDENTS[3]) + "+1920+" + str(self.INDENTS[1] - 20))
        self.red_windows[STAT.TIME_FIGHTER].resizable(False, False)
        self.red_windows[STAT.TIME_FIGHTER].overrideredirect(True)
        self.red_windows[STAT.TIME_FIGHTER].wait_visibility(self.red_windows[STAT.TIME_FIGHTER])
        self.red_windows[STAT.TIME_FIGHTER].wm_attributes("-alpha", 0.5)
        self.red_windows[STAT.TIME_FIGHTER].configure(background=self.BG_COLOR)
        tkinter.Label(self.red_windows[STAT.TIME_FIGHTER], text='Fighter', bg=self.BG_COLOR, fg='white').place(x=0, y=0)

    def show_windows(self) -> None:
        self.blue_windows[STAT.WINRATE].update()
        self.blue_windows[STAT.TIME_FIGHTER].update()
        self.red_windows[STAT.WINRATE].update()
        self.red_windows[STAT.TIME_FIGHTER].update()

    def delete_windows(self) -> None:
        try:
            self.blue_windows[STAT.WINRATE].destroy()
            self.blue_windows[STAT.TIME_FIGHTER].destroy()
            self.red_windows[STAT.WINRATE].destroy()
            self.red_windows[STAT.TIME_FIGHTER].destroy()
        except:
            pass

    def set_state_color(self, color: str) -> None:
        self.indicator_window.configure(background=color)
        self.indicator_window.update()


DATA: Data = Data()
