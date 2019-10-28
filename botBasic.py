import requests as rq
import queue
import random
from time import sleep
#--------------------------------
def init():
	global access_token
	global newMessage
	global server

	access_token = 'dafc83b2c86590370bd54003a90b049aa71d46abe71ee9f663911b9cf1aeec6d5890757ca61ea5b678b95'
	newMessage = queue.Queue()
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
#--------------------------------
def pinPrevMessage(user):
	text = 'https://api.vk.com/method/messages.getHistory?v=5.101&count=1&offset=0'
	text += '&peer_id=' + str(user)
	text += "&access_token=" + access_token
	r = rq.get(text).text
	return r
