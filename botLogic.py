import threading as tr
import botBasic as bot
from time import sleep
import re
#--------------------------------
def isNewMessage(user):
	while not (bot.newMessage["user"] == user and bot.newMessage["new"] == True):
		sleep(0.1)
	bot.newMessage.update({"new":False})
	return True
#--------------------------------
def firstCharacter(user):
	with open('flavorText/firstCharacter/begin.dat', encoding = 'utf-8') as file:
		bot.printMessage(file.read(), user)
		while 1:
			if isNewMessage(user) and bot.newMessage["message"] == 'Компания':
				print('test')
				break
			elif bot.newMessage["message"] == 'Персонаж':
				print('test2')
				break
			else:
				bot.printMessage('Нажмите на одну из кнопок ниже, чтобы продолжить' ,user)
#--------------------------------
def init(user):
	while 1:
		if isNewMessage(user):
			message = bot.newMessage["message"].title()
			if message == 'Помощь':
				answer = ''
				with open('help.dat',encoding = 'utf-8') as file:
					for line in file:
						ans = re.match(r'\:\s(.*)', line)
						if ans != None:
							answer += ans.group(1) + '\n'
				bot.printMessage(answer, user)				
			elif re.match(r'Помощь', message) != None:
				answer = ''
				command = re.match(r'Помощь\s(.*)', message).group(1)
				with open('help.dat',encoding = 'utf-8') as file:
					found = False
					for line in file:
						if re.match(r'\:\s(.*)', line) != None:
							if re.match(r'\:\s(.*)', line).group(1) == command:
								found = True
							else:
								found = False
						elif re.match(r'\:', line) != None:
							found = False
						elif found == True:
							answer += line
				bot.printMessage(answer, user)
			#--------------------
			elif message == 'Начать':
				firstCharacter(user)
			else:
				bot.printMessage('Введите "Помощь" чтобы получить список комманд',user)
		sleep(0.1)