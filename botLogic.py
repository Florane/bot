import threading as tr
import botBasic as bot
from time import sleep
import re
import random as rand
#--------------------------------
def isNewMessage(user):
	while not (bot.newMessage["user"] == user and bot.newMessage["new"] == True):
		sleep(0.1)
	bot.newMessage.update({"new":False})
	return True
#--------------------------------
def createCharacter(user):
	with open('characters/' + user + '.json', 'w', encoding = 'utf-8') as file:
		with open('flavorText/createCharacter/0.dat', encoding = 'utf-8') as file:
			bot.printMessage(file.read(), user)
		isNewMessage(user)
		bot.printMessage('Новая анкета на персонажа! @id{0}'.format(user), user)

#--------------------------------
def firstCharacter(user):
	with open('flavorText/firstCharacter/begin.dat', encoding = 'utf-8') as file:
		bot.printMessage(file.read(), user)
		while 1:
			if isNewMessage(user) and bot.newMessage["message"] == 'Компания':
				print('test')
				break
			elif bot.newMessage["message"] == 'Персонаж':
				with open('flavorText/firstCharacter/characterFirst0.dat', encoding = 'utf-8') as file:
					bot.printMessage(file.read(), user)
				createCharacter(user)
				break
			else:
				bot.printMessage('Нажмите на одну из кнопок ниже, чтобы продолжить' ,user)
#--------------------------------
def diceRoll(amount, sides):
	ret = 0
	dices = []
	i = 0
	while i < amount:
		new = rand.randint(1,sides)
		ret += new
		dices.append(new)
		i+=1
	return str(ret) + ' ' + str(dices)
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
			elif re.match(r'Бросить', message) != None or re.match(r'Roll', message) != None:
				roll = re.compile(r'(\d+)D(\d+)')
				roll = roll.search(message)
				if roll != None:
					bot.printMessage('Вам выпало {0}'.format(diceRoll(int(roll.group(1)), int(roll.group(2)))), user)
				else:
					bot.printMessage('Неверный синтаксис\nБросить <число>d<число>', user)
			#--------------------
			elif user[0] != '2':
				if message == 'Начать':
					firstCharacter(user)
				else:
					bot.printMessage('Введите "Помощь" чтобы получить список комманд', user)
		sleep(0.1)
