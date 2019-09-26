import requests as rq
import threading as tr
import botBasic as bot
from botLogic import init
#--------------------------------
userList = []
bot.init()
#--------------------------------
bot.lpsInit()
while 1:
	text = bot.lpsCheck(bot.server)
	r = rq.get(text)
	if r.json().get("failed") == 2:
		bot.lpsInit()
		continue
	if len(r.json().get('updates')) == 0:
		continue
	print(r.text)
	bot.server["ts"]=r.json()["ts"]
	updates = r.json()["updates"]
	if len(updates) > 0:
		for update in updates:
			if update["type"] == "message_new":
				message = update["object"]["text"]
				peer = str(update["object"]["peer_id"])
				bot.newMessage.clear()
				if peer[:2] == '20':
					user = str(update["object"]["from_id"])
					with open('technical/admins.dat') as file:
						for line in file:
							if line.strip() == user:
								bot.newMessage.update({"admin":user})
				bot.newMessage.update({"user":peer, "message":message, "new":True})
				print('{0} | {1}'.format(message, peer))
				isExist = True
				for u in userList:
					if u.name == peer:
						isExist = False
				if isExist:
					userList.append(tr.Thread(target = init, args = (peer, ), daemon = True, name = peer))
					userList[-1].start()
	print('---------------------------')
