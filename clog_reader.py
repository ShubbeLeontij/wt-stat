import os
import re
import pathlib
import model
import settings

new_match = re.compile(r"sessionId:(\S+)")
difficulty = re.compile(r"MISSION \S+ STARTED at difficulty (\w+)")
find_player = re.compile(r"onStateChanged\(\) MULP pid:(\d+) n:'(\S+)' \S+ t=(\d) c=\d f=\d+\(l=\d\) mid=65535 uid=(\d+)")
find_host = re.compile(r"onStateChanged\(\) MULP pid:(\d+) n:'(\S+)' \S+ t=(\d) c=\d f=\d+\(l=1\) mid=65535 uid=(\d+)")

with open("key.bin", "rb") as key_file:
    key = bytearray(key_file.read())


def dexor(data: bytearray) -> bytearray:
    d_data: bytearray = bytearray(len(data))
    key_length: int = len(key)
    for i, c in enumerate(data):
        d_data[i] = (c ^ key[i % key_length])
    return d_data


def find_host_information(text: str) -> None:
    for match in find_host.findall(text):
        name: str = match[1]
        team: str = match[2]
        uid: int = match[-1]
        if team != '0':
            model.data.host_player_id = uid
            model.data.host_player_team = team
            model.data.add_player(name, uid, team)
            break


def add_players(text: str, old_players: list[model.Player]) -> None:
    for match in find_player.findall(text):
        name: str = match[1]
        team: str = match[2]
        uid: int = match[-1]
        if uid != model.data.host_player_id:
            model.data.add_player(name, uid, team)
        for player in old_players:
            if player.name == name:  # If player was in previous search, copy it
                model.data.get_player(name).stat = player.stat
                model.data.get_player(name).loaded = True


def read() -> None:
    paths = sorted(pathlib.PosixPath(settings.clog_path).expanduser().iterdir(), key=os.path.getmtime)
    with open(paths[-1], "rb") as clog_file:
        data: bytearray = bytearray(clog_file.read())

    all_text: str = dexor(data).decode("utf-8", "ignore")
    current_text: str = all_text.split("Load mission")[-1]
    new_match_id: str = new_match.findall(current_text)[0]
    old_data: model.Data = model.data
    model.data = model.Data()
    model.data.difficulty = difficulty.search(current_text)[1]

    find_host_information(current_text)
    add_players(current_text, old_data.get_players())

    if __name__ == "__main__":
        print(current_text)
        print("allies: ")
        for cur in model.data.team_1 if model.data.host_player_team == '1' else model.data.team_2:
            print(cur.name)
        print("match id:", new_match_id, ", difficulty:", model.data.difficulty, ", players:", len(model.data.get_players()))
        with open("logs.txt", "w") as f:
            f.write("Load mission" + current_text)


if __name__ == "__main__":
    read()
