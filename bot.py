import requests as rq
import threading as tr
import botBasic as bot
from botLogic import init
#--------------------------------
userList = []
bot.init()
#--------------------------------
text = 'https://api.vk.com/method/groups.getLongPollServer?v=5.101&group_id=161748193&access_token='
text = text+bot.access_token

r = rq.get(text)
server = r.json()
server = server["response"]

while 1:
	text = bot.lpsCheck(server)
	r = rq.get(text)
	server["ts"]=r.json()["ts"]
	print(r.text)
	updates = r.json()["updates"]
	if len(updates) > 0:
		for update in updates:
			if update["type"] == "message_new":
				message = update["object"]["text"]
				user = str(update["object"]["from_id"])
				newMessage.update({"user":user, "message":message})
				print('{0} | {1}'.format(message, user))
				isExist = True
				for u in userList:
					if u.name == user:
						isExist = False
				if isExist:
					userList.append(Thread(target = init, args = (user, ), daemon = True))
					userList[-1].start()