import requests
import json
import random
import datetime


token="1081acb04c065120ef3b79df3258ad38352218c93a8f792d70d8d8c529e4eb9a5fde50cb39aabfc10da1b"
group_id="199474622"

key=""
server=""
ts="1"

class Bot:

    def __init__(self):
        global token,group_id,key,server,ts
        response=requests.get("https://api.vk.com/method/groups.getLongPollServer?access_token="+token+"&v=5.124&group_id="+group_id).text
        response=json.loads(response)
        key=response['response']['key']
        server=response['response']['server']
        ts=response['response']['ts']
        Bot.start(self)

    def start(self):
        global token,group_id,key,server,ts
        while(True):
            print(server + "?act=a_check&key=" + key + "&wait=25&mode=2&ts=" + str(ts))
            response = requests.get(server + "?act=a_check&key=" + key + "&wait=25&mode=2&ts=" + str(ts)).text
            response = json.loads(response)
            if ("failed" in response):
                if (response['failed'] != None):
                    Bot()
                    return

            ts = response['ts']

            for i in range(0, len(response['updates'])):
                obj = response['updates'][i]
                if (obj['type'] == "message_new"):
                    obj = response['updates'][i]['object']['message']
                    from_id = obj['from_id']
                    payload = ""
                    if ("payload" in obj):
                        payload = obj['payload']
                    text = obj['text']
                    if (payload == "{\"command\":\"start\"}"):
                        Bot.sendMessage(from_id, "Привет, отправь мне название любого города.")
                    else:
                        rt=requests.get("https://api.openweathermap.org/data/2.5/weather?q="+text+"&APPID=2aceb0c178695a1a6aa807e21ba6acb9").text
                        rt=json.loads(rt)

                        if(rt['cod']=="404"):
                            Bot.sendMessage(from_id,"Город не найден.")
                        else:
                            Bot.sendMessage(from_id,"🏣Город: " + rt['name'] + "\n\n⚡Температура: " + str(int(rt['main']['temp']-273.15)) + "\n💦Влажность: " +
                                  str(rt['main']['humidity'])+"%" +
                                  "\n🌬Скорость ветра: " + str(rt['wind']['speed'])+" м/с" + "\n☁Облачность: " + str(rt['clouds']['all'])+"%" +
                                  "\n🌞Восход: " + datetime.datetime.fromtimestamp(rt['sys']['sunrise']).strftime("%H:%M") + "\n🌚Закат: " + datetime.datetime.fromtimestamp(rt['sys']['sunset']).strftime("%H:%M"))


    def sendMessage(peer_id, text):
        global token
        data = {
            "v": "5.124",
            "access_token": token,
            "peer_id": peer_id,
            "message": text,
            "random_id":random.randint(0,9999999)
        }
        r = requests.post(
            url="https://api.vk.com/method/messages.send",
            data=data).text
        print(r)



Bot()