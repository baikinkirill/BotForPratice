import requests
import json
import random
import datetime
import api
import command
from threading import Thread
import dbinit

offset = 0
work = True


class Bot:

    def __init__(self):
        global offset
        dbinit.dbinitClass()
        offset = (
        api.query("getUpdates", params={"timeout": 20, "offset": offset, "count": 0, "limit": 1}).json()["result"][0][
            "update_id"])
        Bot.start(self)

    def start(self):
        global offset, work
        while (work):
            global offset
            o = (api.query("getUpdates", params={"timeout": 20, "offset": offset}).json()['result'])
            print(json.dumps(o))
            for i in range(0, len(o)):
                if ("message" in o[i]):
                    th = Thread(target=command.check, args=(o[i],))
                    th.start()
                elif ("callback_query" in o[i]):
                    th = Thread(target=command.checkCallback, args=(o[i],))
                    th.start()

                offset = o[i]['update_id']
            if(len(o)>0):
                offset += 1


Bot()
