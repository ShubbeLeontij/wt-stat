print("Configuring")
import model
import time
import threading
import clog_reader
import stat_getter
import stat_viewer
import pynput


def on_press(key):
    if key == pynput.keyboard.Key.up:
        if model.DATA.currently_in_tab:
            model.DATA.set_state_color('green')
            model.DATA.delete_windows()
            model.DATA.currently_in_tab = False
        else:
            model.DATA.set_state_color('cyan')
            stat_viewer.read()
            model.DATA.currently_in_tab = True
            model.DATA.set_state_color('purple')
    if key == pynput.keyboard.Key.down:
        load()


def on_release(key):
    return


def load():
    try:
        clog_reader.read()
    except:
        print("Failed to parse clog file")
    print("New battle, getting stat for " + str(len(model.DATA.get_players())) + " players")
    model.DATA.set_state_color('yellow')
    #try:
    stat_getter.findstat()
    #except:
    #print("Failed to get stat")
    print("Found stat for " + str(len(model.DATA.get_players())) + " players")
    model.DATA.set_state_color('green')


threads = [pynput.keyboard.Listener(on_press=on_press, on_release=on_release)]
for thread in threads:
    thread.start()
print("Running")
model.DATA.set_state_color('orange')
for thread in threads:
    thread.join()
