print("Configuring")
import threading
import settings
import model
import clog_reader
import stat_getter
import stat_viewer
import pynput
import tkinter


def on_press(key: pynput.keyboard.Key) -> None:
    if key == settings.load_button:
        try:
            clog_reader.read()
        except:
            print("Failed to parse clog file")
            return
        print("New battle, getting stat for " + str(len(model.data.get_players())) + " players")
        model.data.set_state_color("yellow")
        # try:
        stat_getter.findstat()
        # except:
        # print("Failed to get stat")
        print("Found stat for " + str(len(model.data.get_players())) + " players")
        model.data.set_state_color("green")
    if key == settings.show_button:
        if model.data.currently_in_tab:
            model.data.set_state_color("green")
            model.data.delete_windows()
            model.data.currently_in_tab = False
        else:
            model.data.set_state_color("cyan")
            stat_viewer.read()
            model.data.currently_in_tab = True
            model.data.set_state_color("purple")


def on_release(key: pynput.keyboard.Key) -> None:
    return


def on_click(x: int, y: int, button: pynput.mouse.Button, clicked: bool) -> None:
    global root
    if button != pynput.mouse.Button.left or clicked:
        return
    if not model.data.currently_in_tab:
        return
    if root is not None:
        root.destroy()
        root = None
        return
    same_team: bool = x < model.INDENTS[settings.resolution]["SCREENSHOT_RED_X"]
    if same_team and model.data.host_player_team == '1':
        players: list[model.Player] = model.data.team_1
    elif not same_team and model.data.host_player_team != '1':
        players: list[model.Player] = model.data.team_1
    else:
        players: list[model.Player] = model.data.team_2
    row: int = (y - model.INDENTS[settings.resolution]["Y_DEFAULT"] - 20) // model.ROW_HEIGHT
    if row < 0:
        return
    for cur in players:
        if cur.cur_row == row:
            slots: list[str] = [cur.name]
            if "country_usa" not in cur.slots:
                slots.append("has no usa setup")
            else:
                for vehicle in list(cur.slots["country_usa"].keys()):
                    slots.append(vehicle)
            root = tkinter.Tk()
            root.geometry("200x200+" + str(x) + "+" + str(y))
            root.resizable(False, False)
            root.overrideredirect(True)
            for i in range(len(slots)):
                tkinter.Label(root, text=slots[i]).place(x=0, y=i * model.ROW_HEIGHT)
            root.update()
            return


root: tkinter.Tk | None = None
threads: list[threading.Thread] = [pynput.keyboard.Listener(on_press=on_press, on_release=on_release), pynput.mouse.Listener(on_click=on_click)]
for thread in threads:
    thread.start()
print("Running")
model.data.set_state_color("orange")
for thread in threads:
    thread.join()
