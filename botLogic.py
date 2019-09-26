import botBasic as bot
import polishCalc as pol
import time
import re
#--------------------------------
def isNewMessage(user):
	while not (bot.newMessage.get("user") == user and bot.newMessage.get("new") == True):
		time.sleep(0.1)
	bot.newMessage.update({"new":False})
	return True
#--------------------------------
def createCharacter(user):
	with open('characters/' + user + '.json', 'w+', encoding = 'utf-8') as file:
		with open('flavorText/firstCharacter/createCharacter/0.dat', encoding = 'utf-8') as file:
			bot.printMessage(file.read(), user)
		isNewMessage(user)
		bot.printMessage('Новая анкета на персонажа! @id{0}'.format(user), '391442603')
#--------------------------------
def firstCharacter(user):
	with open('flavorText/firstCharacter/begin.dat', encoding = 'utf-8') as file:
		bot.printMessage(file.read(), user)
		while 1:
			if isNewMessage(user) and bot.newMessage["message"] == 'Зарегистрировать компанию':
				print('test')
				break
			elif bot.newMessage["message"] == 'Зарегистрировать коммандора':
				with open('flavorText/firstCharacter/characterFirst0.dat', encoding = 'utf-8') as file:
					bot.printMessage(file.read(), user)
				createCharacter(user)
				break
			else:
				bot.printMessage('Нажмите на одну из кнопок ниже, чтобы продолжить' ,user)
#--------------------------------
def diceCalc(string):
	string = string.lower()
	string = re.sub(r'\s+',r'',string)
	try:
		solved = pol.solvePolish(pol.toPolish(string))
	except SyntaxError:
		return None
	return str(solved['num']) + ' = ' + pol.cutDices(string, solved['dices'])
#--------------------------------
def init(user):
	while 1:
		if isNewMessage(user):
			message = bot.newMessage["message"].title()
			#admin = bot.newMessage.get("admin")
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
				roll = re.compile(r'\S+\s(.+)')
				roll = roll.search(message)
				answer = diceCalc(roll.group(1))
				if roll != None and answer != None:
					bot.printMessage('Вам выпало {0}'.format(answer), user)
				else:
					bot.printMessage('Неверный синтаксис', user)
			#--------------------
			elif user[:2] != '20':
				if message == 'Начать':
					firstCharacter(user)
				else:
					bot.printMessage('Введите "Помощь" чтобы получить список комманд', user)
		time.sleep(0.1)
