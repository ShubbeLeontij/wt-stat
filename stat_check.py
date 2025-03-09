print("Configuring")
import settings
import model
import clog_reader
import stat_getter
import stat_viewer
import pynput


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


threads = [pynput.keyboard.Listener(on_press=on_press, on_release=on_release)]
for thread in threads:
    thread.start()
print("Running")
model.data.set_state_color("orange")
for thread in threads:
    thread.join()
