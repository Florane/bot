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
	print(r.text)
	if server.get("failed") != none
		bot.lpsInit()
		continue
	server["ts"]=r.json()["ts"]
	updates = r.json()["updates"]
	if len(updates) > 0:
		for update in updates:
			if update["type"] == "message_new":
				message = update["object"]["text"]
				peer = str(update["object"]["peer_id"])
				if peer[0] == '2':

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
