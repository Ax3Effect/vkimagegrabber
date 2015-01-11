# -*- coding: utf-8 -*-
import vk
import time
try:
    import ujson as json
except ImportError:
    print("ujson not found, using json")
    import json
import traceback
import urllib.request
import datetime
from time import strftime
from random import randint
from configobj import ConfigObj
import random
config = ConfigObj("settings.ini")
vk_access_token = config['vk_token']
vkapi = vk.API(access_token=vk_access_token)
countNumber = 0

### Settings ###
chat_id = 1 # change it to your chat_id, you can get chat id by going to the conference page
# and looking at "&sec=c*number*" parameter
howMany = 0 # Put this to whatever message limit is * 200 (0 is no limit)


def downloadImage(url, filename):
    global countNumber
    countNumber = countNumber + 1
    print("Downloading image " + str(countNumber) + " - " + filename)
    imageName = str(filename) + ".jpg"
    try:
        urllib.request.urlretrieve(url, imageName)
    except Exception:
        downloadImage(url, filename)


def getMessages(chat_id,offset):
    try:
        msgGet = vkapi.messages.getHistory(chat_id = chat_id, offset = offset, count = 200, rev = 0)
        return msgGet
    except Exception:
        getMessages(chat_id,offset) # grabbing again

print("Ax3 VK Image Grabber - http://vk.com/ax3effect - http://github.com/ax3effect")
print("Getting chat id: " + str(chat_id))

if howMany == 0:
    howManyVar = 999999999 # just making no limits for downloading limit
else:
    howManyVar = howMany

try:
    # Main download function
    for e in range(0, howManyVar):
        counta = e * 200 # VK only allows 200 messages per request
        msginfo = getMessages(chat_id, counta)
        try:
            for i in msginfo["items"]:
                try:
                    photoinfo1 = i["attachments"][0]["photo"]
                    try: # trying to get bigger image resolution
                        photoinfo2 = photoinfo1["photo_1280"]
                        downloadImage(photoinfo2, datetime.datetime.fromtimestamp(int(i["date"])).strftime('%Y-%m-%d %H-%M-%S'))

                    except Exception:
                        photoinfo2 = photoinfo1["photo_604"]
                        downloadImage(photoinfo2, datetime.datetime.fromtimestamp(int(i["date"])).strftime('%Y-%m-%d %H-%M-%S'))
                except Exception:
                    #traceback.print_exc()
                    pass
                    #print("Photo not found.")
            print("-- Downloading offset " + str(counta))
        except Exception:
            pass
except Exception:
    traceback.print_exc()
    pass