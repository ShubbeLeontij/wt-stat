import requests

import clog_reader
import model
import settings
import json

ranking: list[dict[str, int]] | None = None


def get_level(exp: int) -> int:
    for rank in ranking[::-1]:
        if rank["experience"] < exp:
            return rank["rank"]
    return 0


def parse_stat(player: model.Player, exp: int, stats) -> None:
    player.set_stat(settings.STAT.LEVEL, get_level(exp))
    player.set_stat(settings.STAT.WINS, stats["victories"])
    player.set_stat(settings.STAT.BATTLES, stats["missionsComplete"])
    player.set_stat(settings.STAT.WINRATE, round(100 * int(player.get_stat(settings.STAT.WINS)) / int(player.get_stat(settings.STAT.BATTLES))))
    player.set_stat(settings.STAT.TIME_FIGHTER, stats["fighter"]["timePlayed"])
    player.set_stat(settings.STAT.TIME_ATTACKER, stats["assault"]["timePlayed"])
    player.set_stat(settings.STAT.TIME_TANKS, stats["tank"]["timePlayed"])
    player.set_stat(settings.STAT.TIME_ANTI_AIR, stats["SPAA"]["timePlayed"])
    player.loaded = True


def findstat() -> None:
    global ranking
    if ranking is None:
        res = requests.get("https://api.thunderinsights.dk/v1/general/rank/")
        try:
            ranking = json.loads(res.content)
        except json.JSONDecodeError:
            print("Wrong answer for ranking with code", res.status_code)
            return

    for player in model.data.get_players_to_load():
        res = requests.get("https://api.thunderinsights.dk/v1/users/direct/" + str(player.uid))
        try:
            json_obj = json.loads(res.content)
            if json_obj["nick"] != player.name:
                print(player.name, "can be replaced by", json_obj["nick"])
            player.slots = json_obj["slots"]
            parse_stat(player, json_obj["exp"], json_obj["summary"]["pvp_played"][model.data.difficulty])
            print("Got data for", player.name)
        except json.JSONDecodeError:
            print("Wrong answer for", player.name, "with code", res.status_code)


if __name__ == "__main__":
    # model.DATA.difficulty = "hardcore"
    # model.DATA.add_player("AQ55", 27668790, "1")
    clog_reader.read()
    findstat()
    for cur in model.data.get_players():
        print(cur.name, cur.uid, cur.team)
        print(cur.get_stat(settings.STAT.WINS))
        print(cur.get_stat(settings.STAT.BATTLES))
        print(cur.get_stat(settings.STAT.WINRATE))
        print(cur.get_stat(settings.STAT.TIME_FIGHTER))
        print(cur.get_stat(settings.STAT.TIME_ATTACKER))
        print(cur.get_stat(settings.STAT.TIME_TANKS))
        print(cur.get_stat(settings.STAT.TIME_ANTI_AIR))
        print()

