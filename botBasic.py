import requests as rq
import random

def init():
	global access_token
	global newMessage

	access_token = '3ec68f5d2d7437c543d56f5c2620dafc033ccd64286ecc73d23ec8969e9a5424ea9553458ddbbd681e067'
	newMessage = {"user":0, "message":"", "new":False}

def lpsCheck(json):
	text = json["server"]
	text += "?act=a_check&key="
	text += json["key"]
	text += "&ts="
	text += json["ts"]
	text += "&wait=60"
	return text

def printMessage(message, user):
	text = 'https://api.vk.com/method/messages.send?v=5.101'
	text += '&peer_id=' + str(user)
	text += "&random_id=" + str(random.getrandbits(64))
	text += "&message=" + message
	text += "&access_token=" + access_token
	r = rq.get(text)
	return r
