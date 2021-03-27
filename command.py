import datetime
import re

import requests

import api
import json
import keyboards
import image
import sqlite3 as sl

from_id = 0


def check(obj):
    global from_id
    from_id = obj['message']["from"]['id']
    con = sl.connect('bd.db')
    cur = con.cursor()
    cr = cur.execute("SELECT * FROM users WHERE id=?", (from_id,)).fetchall()[0]
    if (len(cr) == 0):
        cur.execute("INSERT INTO users (id) VALUES (?)", (from_id,))
        con.commit()

    command = []
    if ("text" in obj['message']):
        command = obj['message']['text']

    if ("reply_to_message" in obj['message']):
        image.create(obj["message"]["reply_to_message"]["text"], obj["message"]["reply_to_message"]["from"]["id"],
                     obj["message"]["reply_to_message"]["date"], from_id,
                     obj["message"]["reply_to_message"]["from"]["first_name"])
        return

    elif ("forward_from_chat" in obj['message']):
        image.create(obj["message"]["caption"], obj["message"]["forward_from_chat"]["id"],
                     obj["message"]["forward_date"], from_id,
                     obj["message"]["forward_from_chat"]["title"])
        return

    elif ("forward_date" in obj['message']):
        image.create(obj["message"]["text"], obj["message"]["forward_from"]["id"],
                     obj["message"]["forward_date"], from_id,
                     obj["message"]["forward_from"]["first_name"])
        return

    reg = "^\/([a-z]*)[\s]*"
    for i in range(0, len(command.split(" ")) - 1):
        reg = reg + "([^\s]*)\s*"
    command = re.findall(reg, command)
    if (len(command) == 0):
        command.append("NULL")
    if (command[0] == "cancel"):
        cancel()
    else:
        if ((cr[2]) != None and str(cr[2]) != ""):
            if (cr[2] == "weather"):
                sendWeather(obj)

        else:
            if (command[0] == "start"):
                sendHello(obj)
            elif (command[0] == "weather" or obj['message']['text'] == "⛅ Узнать погоду 🌧"):
                setWT()
            elif (command[0] == "weather" or obj['message']['text'] == "🔢 КаЛьКуЛяТоР 🔢"):
                calculator()
            elif (command[0] == "quote" or obj['message']['text'] == "✍ Создать цитату 💬"):
                api.query("sendMessage", params = {"chat_id": obj['message']["from"]['id'],
                                                   "text": "Чтобы создать цитату, просто перешлите мне сообщение",
                                                   "reply_markup": (keyboards.home_keyboard())})
            else:
                api.query("sendMessage", params = {"chat_id": obj['message']["from"]['id'],
                                                   "text": "Я не понимаю :(",
                                                   "reply_markup": (keyboards.home_keyboard())})



def calculator():
    (api.query("sendMessage", params = {"chat_id": from_id,
                                       "text": "Введите...",
                                       "reply_markup": (keyboards.calc())}).json())


def checkCallback(obj):
    global from_id
    from_id = obj['callback_query']["from"]['id']
    con = sl.connect('bd.db')
    cur = con.cursor()
    cr = cur.execute("SELECT id FROM users WHERE id=?", (from_id,)).fetchall()[0]
    if (len(cr) == 0):
        cur.execute("INSERT INTO users (id) VALUES (?)", (from_id,))
    con.commit()
    command = obj['callback_query']['data']

    calc=["c1","c2","c3","c4","c5","c6","c7","c8","c9","c0","c+","c-","c*","c/","c=","cC"]

    if (command == "cancel"):
        cancel()
    elif(command in calc):
        callbackCalc(obj)



def callbackCalc(obj):

    operation=obj['callback_query']['data']
    id=obj['callback_query']['message']['message_id']
    text=obj['callback_query']['message']['text']
    te=""
    if(text=="Введите..."):
        text=""
    else:
        te=text[len(text)-1]
    if(te=="+" or te=="-" or te=="*" or te=="/"):
        text=text+" "


    if(operation=="c1"):text=text+"1"
    elif(operation=="c2"):text=text+"2"
    elif(operation=="c3"):text=text+"3"
    elif(operation=="c4"):text=text+"4"
    elif(operation=="c5"):text=text+"5"
    elif(operation=="c6"):text=text+"6"
    elif(operation=="c7"):text=text+"7"
    elif(operation=="c8"):text=text+"8"
    elif(operation=="c9"):text=text+"9"
    elif(operation=="c0"):text=text+"0"
    elif(operation=="c+"):
        text=correct(text)
        text=str(text)+" + "
    elif(operation=="c-"):
        text=correct(text)
        text=text+" - "
    elif(operation=="c*"):
        text=correct(text)
        text=text+" * "
    elif(operation=="c/"):
        text=correct(text)
        text=text+" / "
    elif(operation=="c="):
        ol = re.findall("([\-]*\d*)\s([+\-*\/])\s([\-]*\d{1,})", text)
        if (len(ol) > 0):
            ol = ol[0]
            if (ol[1] == "+"):
                text = int(ol[0]) + int(ol[2])
            if (ol[1] == "-"):
                text = int(ol[0]) - int(ol[2])
            if (ol[1] == "*"):
                text = int(ol[0]) * int(ol[2])
            if (ol[1] == "/"):
                text = int(ol[0]) / int(ol[2])
        text=str(text)
    elif(operation=="cC"):
        print("F")
        text="Введите..."

    api.query("editMessageText",params = {"chat_id":obj['callback_query']["from"]['id'],"message_id":id,
                                          "text":text,"reply_markup":keyboards.calc()})


def correct(text):
    if ("+" in text or "-" in text or "*" in text or "/" in text):
        ol = re.findall("([\-]*\d*)\s([+\-*\/])\s([\-]*\d{1,})", text)
        ol1 = re.findall("([\-]*\d*)\s([+\-*\/])", text)
        if (len(ol) > 0):
            ol=ol[0]
            if (ol[1] == "+"):
                text = int(ol[0]) + int(ol[2])
            if (ol[1] == "-"):
                text = int(ol[0]) - int(ol[2])
            if (ol[1] == "*"):
                text = int(ol[0]) * int(ol[2])
            if (ol[1] == "/"):
                text = int(ol[0]) / int(ol[2])
        elif (len(ol1) > 0):
            text = str(ol1[0][0])

    return str(text)

def sendHello(obj):
    api.query("sendSticker", params = {"chat_id": obj['message']["from"]['id'],
                                       "sticker": "CAACAgIAAxkBAAMTYFiUvJSGrXxlu2A4QLoKuolxF3IAAjQmAAKezgsAAZB_E_57PPMdHgQ"
                                       })
    api.query("sendMessage", params = {"chat_id": obj['message']["from"]['id'],
                                       "text": "Пользуйтесь ботом, используя кнопки.",
                                       "reply_markup": (keyboards.home_keyboard())})
    return 1


def setWT():
    con = sl.connect('bd.db')
    cur = con.cursor()
    cur.execute("UPDATE users SET action=? WHERE id=?", ("weather", from_id))
    con.commit()
    con.close()
    api.query("sendMessage", params = {"chat_id": from_id,
                                       "text": "В каком городе вы ходите узнать погоду?"})


def sendWeather(obj):
    global from_id

    rt = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=" + obj["message"][
            "text"] + "&APPID=2aceb0c178695a1a6aa807e21ba6acb9").text
    rt = json.loads(rt)

    if (rt['cod'] == "404"):
        api.query("sendMessage", params = {"chat_id": from_id,
                                           "text": "Город не найден. Попробуйте снова, либо напишите /cancel",
                                           "reply_markup": (keyboards.cancel())})
    else:
        api.query("sendMessage", params = {"chat_id": from_id,
                                           "text": "🏣Город: " + rt['name'] + "\n\n⚡Температура: " + str(
                                               int(rt['main']['temp'] - 273.15)) + "\n💦Влажность: " +
                                                   str(rt['main']['humidity']) + "%" +
                                                   "\n🌬Скорость ветра: " + str(
                                               rt['wind']['speed']) + " м/с" + "\n☁Облачность: " + str(
                                               rt['clouds']['all']) + "%" +
                                                   "\n🌞Восход: " + datetime.datetime.fromtimestamp(
                                               rt['sys']['sunrise']).strftime(
                                               "%H:%M") + "\n🌚Закат: " + datetime.datetime.fromtimestamp(
                                               rt['sys']['sunset']).strftime("%H:%M"),
                                           "reply_markup": (keyboards.home_keyboard())})

        con = sl.connect('bd.db')
        cur = con.cursor()
        cur.execute("UPDATE users SET action=? WHERE id=?", ("", from_id))
        con.commit()
        con.close()


def cancel():
    global from_id
    con = sl.connect('bd.db')
    cur = con.cursor()
    cur.execute("UPDATE users SET action=? WHERE id=?", ("", from_id))
    con.commit()
    con.close()
    api.query("sendMessage", params = {"chat_id": from_id, "text": "Все действия отменены.",
                                       "reply_markup": (keyboards.home_keyboard())})
