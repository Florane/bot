import requests as rq
import random
from time import sleep
#--------------------------------
def init():
	global access_token
	global newMessage
	global server

	access_token = '3ec68f5d2d7437c543d56f5c2620dafc033ccd64286ecc73d23ec8969e9a5424ea9553458ddbbd681e067'
	newMessage = {}
	server = {}
#--------------------------------
def lpsInit():
	lps = 'https://api.vk.com/method/groups.getLongPollServer?v=5.101&group_id=161748193&access_token='
	lps = lps+access_token
	r = rq.get(lps)
	print(r.text)
	server.update(r.json()["response"])
#--------------------------------
def lpsCheck(json):
	text = json["server"]
	text += "?act=a_check&key="
	text += json["key"]
	text += "&ts="
	text += json["ts"]
	text += "&wait=60"
	return text
#--------------------------------
def printMessage(message, user):
	newMsg = []
	maxSize = 1000
	while 1:
		newMsg.append(message[:maxSize])
		if not len(message) > maxSize:
			break
		message = message[maxSize:]
	r = ''
	print(newMsg)
	print(len(newMsg))
	for msg in newMsg:
		text = 'https://api.vk.com/method/messages.send?v=5.101'
		text += '&peer_id=' + str(user)
		text += "&random_id=" + str(random.getrandbits(64))
		text += "&message=" + msg
		text += "&access_token=" + access_token
		r += rq.get(text).text
		if len(newMsg) > 1:
			sleep(2)
	return r
