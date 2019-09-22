import threading as tr
import botBasic as bot
#--------------------------------
def init(user):
	lockMessage = tr.Condition()
	while 1:
		lockMessage.wait_for(bot.newMessage["user"] == user)