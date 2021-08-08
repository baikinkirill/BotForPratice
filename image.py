# -*- coding: utf-8 -*-

import re
import textwrap
import datetime
from urllib.request import urlopen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import requests
import json
import random
import api
import os

text = u"Tylko jedno w głowie mam Koksu pięć gram odlecieć sam W krainę zapomnienia W głowie myśli mam Kiedy skończy się ten stan Gdy już nie będę sam Bo wjedzie biały węgorz Tylko jedno w głowie mam Koksu pięć gram odlecieć sam W krainę zapomnienia W głowie myśli mam Kiedy skończy się ten stan Gdy już nie będę sam"
author = "Павел Дуров"
time = "19:40"
img = "https://sun1-92.userapi.com/impf/c836333/v836333001/31189/8To0r3d-6iQ.jpg?size=200x0&quality=96&crop=514,119,337,337&sign=a91b1b1e6e4c9c976c7de0af333e9a92&c_uniq_tag=vs6c9I0iocxfOBxSe4XSFFdDtF9fN2XTfL295svY0SA&ava=1"


class create:

    def __init__(self, text1, authorid, time1, peer_id1, author):
        global text, time, img, peer_id
        text = text1
        time = time1
        time = datetime.datetime.utcfromtimestamp(int(time) + 60 * 3 * 60).strftime('%H:%M')
        Online="был(а) в сети "
        ti=int(datetime.datetime.now().timestamp()-int(datetime.datetime.now().strftime("%H"))*60*60-int(datetime.datetime.now().strftime("%M"))*60-int(datetime.datetime.now().strftime("%S")))


        if(ti-60*60*24<time1<ti):
            print("Вчера")
            Online=Online+"вчера в "+time
        elif(time1>ti):
            Online=Online+"в "+time
        else:
            Online=Online+datetime.datetime.utcfromtimestamp(int(time1) + 60 * 3 * 60).strftime('%d.%m.%Y')+" в "+str(time)



        peer_id = peer_id1
        # obj=VKApi.getUser(authorid)
        obj = api.query("getUserProfilePhotos", params = {"user_id": authorid})
        img = api.query("getUserProfilePhotos", params = {"user_id": authorid}).json()

        try:
            if (len(img['result']['photos']) > 0):
                img = "https://api.telegram.org/file/bot753593125:AAHvUANvzJwY6cwmXW6t9QigimAcuimijjs/" + (
                    api.query("getFile", params = {"file_id": img['result']['photos'][0][0]['file_id']}).json()[
                        'result'][
                        'file_path'])
            else:
                img = "https://sovet-doctora73.ru/images/doctors/unnamed.jpg"
        except:
            img = "https://sovet-doctora73.ru/images/doctors/unnamed.jpg"

        p = os.path.abspath('img/GoogleSans-Regular.ttf')
        p1 = os.path.abspath('img/GoogleSans-Medium.ttf')
        font = ImageFont.truetype(p, 50)
        font1 = ImageFont.truetype(p, 25)
        font2 = ImageFont.truetype(p1, 55)
        font3 = ImageFont.truetype(p, 30)
        wrap = textwrap.wrap(text, width = 45)
        image = Image.new("RGB", (1920, font.getsize(wrap[0])[1] * (len(wrap)+len(re.findall("\n",text))+20) + 100), "#b2cdec")
        draw = ImageDraw.Draw(image)
        margin = offset = 40
        maxX = 0

        texte=text.split("\n")
        for i in range(0,len(texte)):
            if(texte[i]==""):
                draw.text((margin, offset - 5), "", font = font, fill = "#000")
                x = font.getsize("")[0]
                if (x > maxX):
                    maxX = x
                offset += font.getsize(line)[1]
            wrap=textwrap.wrap(texte[i], width = 45)
            for line in wrap:
                draw.text((margin, offset - 5), line, font = font, fill = "#000")
                x = font.getsize(line)[0]
                if (x > maxX):
                    maxX = x
                offset += font.getsize(line)[1]


        if (maxX < 60):
            maxX = 60
        draw.text((maxX + 5, offset), time, font = font1, fill = "#7c8b9c")

        print(offset)
        image = create.add_corners(image.crop((0, 0, maxX + 80, offset + 40)), 35)

        image1 = Image.new("RGB", (1300 + 200, offset + 300), "#FFFFFF")
        image1.paste(image, (15, 200), image)
        image2 = Image.open("img/snimok.png")
        image1.paste(image2, (0, -5), image2)
        image3 = Image.open(urlopen(img)).resize((150, 150))
        image3 = create.add_corners(image3, 70)
        image1.paste(image3, (160, 15), image3)
        draw = ImageDraw.Draw(image1)
        draw.text((350, 35), author, font = font2, fill = "#000")
        draw.text((350, 110), Online, font = font3, fill = "#828B94")
        draw.line((0, 180, 1300 + 200, 180), fill = "#cccccc")

        rtf = random.randint(0, 99999999)

        image1.save(str(rtf) + ".png")

        create.send(self, peer_id, str(rtf))

    def send(self, peer_id, str):
        global text, author, time, img
        # token = consts.token

        params = api.query("sendPhoto", params = {"chat_id": peer_id},
                           files = {"photo": open(str + ".png", "rb")}).json()
        print(params)
        print("message")
        os.remove(str + ".png")

    def add_corners(im, rad):
        global text, author, time, img, peer_id

        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, (rad * 2) - 1, (rad * 2) - 1), fill = 255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im
