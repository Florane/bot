import botBasic as bot
import polishCalc as pol
import botCharacter as char
import time
import re
import threading as tr
#--------------------------------
def isNewMessage(user):
	while not (bot.newMessage.get("user") == user and bot.newMessage.get("new") == True):
		time.sleep(0.1)
	bot.newMessage.update({"new":False})
	return True
#--------------------------------
def createCommander(user, helpListings, mainLock):
	with open('characters/' + user + '.json', 'w+', encoding = 'utf-8') as characterFile:
		character = {}
		with open('flavorText/firstCharacter/createCharacter/0.dat', encoding = 'utf-8') as file:
			bot.printMessage(file.read(), user)
		mainLock.wait()
		if isNewMessage(user):
			character['flavor'] = bot.newMessage.get('message')

		maxLevel = pol.solvePolish(pol.toPolish('40+3d6p1'))['num']
		with open('flavorText/firstCharacter/createCharacter/1.dat', encoding = 'utf-8') as file:
			bot.printMessage(file.read().format(maxLevel), user)
		helpListings[0] = 'mc'
		while mainLock.wait():
			if isNewMessage(user):
				try:
					statList = [["INT","Интеллект"],["REF","Рефлексы"],["CHAR","Харизма"],["TECH","Техническе Навыки"],["LUCK","Удача"],["MA","Скорость Бега"],["BODY","Телосложение"],["EM","Эмпатия"]]
					character['stats'] = char.commanderStats(bot.newMessage.get('message'), maxLevel, statList)
					break
				except SyntaxError:
					bot.printMessage('Ошибка: Неверное кол-во вхождений', user)
				except ValueError:
					bot.printMessage('Ошибка: Неверная сумма вхождений', user)

		with open('flavorText/firstCharacter/createCharacter/2.dat', encoding = 'utf-8') as file:
			bot.printMessage(file.read().format(maxLevel), user)
		helpListings[0] = 'mvb'
		while mainLock.wait():
			if isNewMessage(user):
				try:
					statList = [["Notice","Внимательность"],["Handgun","Пистолеты"],["Submachine gun","Пистолеты-пулеметы"],["Rifle","Винтовки"],["Dodge","Уворот"],["Melee","Рукопашная"],[""]]
					character['stats'] = char.commanderStats(bot.newMessage.get('message'), maxLevel, statList)
					break
				except SyntaxError:
					bot.printMessage('Ошибка: Неверное кол-во вхождений', user)
				except AddingError:
					bot.printMessage('Ошибка: Неверная сумма вхождений', user)
		bot.printMessage('Новая анкета на персонажа! @id{0}'.format(user), '391442603')
		characterFile.write(str(character))
#--------------------------------
def firstCharacter(user, helpListings, mainLock, errorLock):
	with open('flavorText/firstCharacter/begin.dat', encoding = 'utf-8') as file:
		bot.printMessage(file.read(), user)
		helpListings[0] = 'm'
		while 1:
			errorLock.clear()
			print(errorLock.is_set())
			mainLock.wait()
			if isNewMessage(user) and bot.newMessage["message"] == 'Зарегистрировать компанию':
				print('test')
				break
			elif bot.newMessage["message"] == 'Зарегистрировать коммандора':
				with open('flavorText/firstCharacter/characterFirst0.dat', encoding = 'utf-8') as file:
					bot.printMessage(file.read(), user)
				createCommander(user, helpListings, mainLock)
				break
			else:
				bot.printMessage('Нажмите на одну из кнопок ниже, чтобы продолжить' ,user)
		helpListings[0] = 'm'
		errorLock.set()
#--------------------------------
def diceCalc(string):
	string = string.lower()
	string = re.sub(r'\s+',r'',string)
	try:
		solved = pol.solvePolish(pol.toPolish(string))
	except:
		return None
	return str(solved['num']) + ' = ' + pol.cutDices(string, solved['dices'])
#--------------------------------
def init(user):
	helpListings = ['mf']
	if user[:3] == '200':
		helpListings[0] = 'm'
	mainLock = tr.Event()
	errorLock = tr.Event()
	errorLock.set()
	while 1:
		mainLock.clear()
		if isNewMessage(user):
			message = bot.newMessage["message"].title()
			#admin = bot.newMessage.get("admin")
			if message == 'Помощь':
				print(helpListings)
				answer = ''
				with open('help.dat',encoding = 'utf-8') as file:
					for line in file:
						ans = re.match(r'[' + helpListings[0] + ']\s(.*)', line)
						if ans != None:
							answer += ans.group(1) + '\n'
				bot.printMessage(answer, user)
			elif re.match(r'Помощь', message) != None:
				answer = ''
				command = re.match(r'Помощь\s(.*)', message).group(1)
				with open('help.dat',encoding = 'utf-8') as file:
					found = False
					prevListing = ''
					for line in file:
						print(line)
						if re.match(r'[' + helpListings[0] + ']\s(.*)', line) != None:
							print('1')
							prevListing = line[0]
							if re.match(r'[' + helpListings[0] + ']\s(.*)', line).group(1) == command:
								print('11')
								found = True
							else:
								print('12')
								found = False
						elif re.match(r'-\s(.*)', line) != None:
							print('2')
							if re.match(r'-\s(.*)', line).group(1) == command and prevListing in helpListings[0]:
								print('21')
								found = True
						elif re.match(r'.\s', line) != None:
							print('3')
							found = False
						elif found == True:
							print('4')
							if re.match(r'-\s', line) == None:
								print('41')
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
			elif user[:3] != '200':
				if message == 'Начать' and helpListings[0].find('f') >= 0:
					tr.Thread(target = firstCharacter,args =  (user, helpListings, mainLock, errorLock)).start()
				elif errorLock.is_set():
					bot.printMessage('Введите "Помощь" чтобы получить список комманд', user)
				else:
					bot.newMessage.update({'new':True})
			#леня ну мать твою
			elif message == 'Aide':
				bot.printMessage('леня блять', user)
		mainLock.set()
		#time.sleep(0.1)
