import os
import re
import pathlib
import model
import settings


with open("key.bin", "rb") as key_file:
    key = bytearray(key_file.read())
diff_obj = {"arcade": 1, "realistic": 2, "hardcore": 3}


def dexor(data: bytearray) -> bytearray:
    d_data: bytearray = bytearray(len(data))
    key_length: int = len(key)
    for i, c in enumerate(data):
        d_data[i] = (c ^ key[i % key_length])
    return d_data


def read() -> None:
    paths: list = sorted(pathlib.PosixPath(settings.clog_path).expanduser().iterdir(), key=os.path.getmtime)
    with open(paths[-1], "rb") as clog_file:
        data: bytearray = bytearray(clog_file.read())

    all_text: str = dexor(data).decode("utf-8", "ignore")
    current_text: str = all_text.split("Load mission")[-1]
    new_match_id: str = re.findall(r"sessionId:(\S+)", current_text)[0]
    model.DATA = model.Data()
    model.DATA.diff_number = diff_obj[re.search(r"MISSION \S+ STARTED at difficulty (\w+)", current_text)[1]]
    for match in re.findall(r"onStateChanged\(\) MULP p\d+ n='(\S+)' \S+ t=(\d)", current_text):
        if match[1] == '0':
            model.DATA.host_player = model.Player(match[0], match[1])
        else:
            model.DATA.add_player(match[0], match[1])
    if __name__ == "__main__":
        print("match id:", new_match_id, "difficulty:", model.DATA.diff_number)
        with open("logs.txt", "w") as f:
            f.write("Load mission" + current_text)


if __name__ == "__main__":
    read()
