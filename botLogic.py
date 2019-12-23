import botBasic as bot
from os.path import exists
import queue
import random as rand
import polishCalc as pol
import botCharacter as char
import time
import re
import threading as tr
#--------------------------------
def getNewMessage(user):
	while 1:
		try:
			while bot.newMessage.queue[0].get("user") != user:
				time.sleep(0.1)
				continue
			break
		except IndexError:
			pass
	return bot.newMessage.get()
#--------------------------------
def formatCommanderStats(user,helpListings,mainLock,maxLevel,fileName,setHL,statList):
	with open('flavorText/firstCharacter/createCharacter/'+fileName, encoding = 'utf-8') as file:
		bot.printMessage(file.read().format(maxLevel), user)
	helpListings[0] = setHL
	while mainLock.wait():
		try:
			addStats = char.commanderStats(getNewMessage(user).get('message'), maxLevel, statList)
			break
		except SyntaxError:
			bot.printMessage('Ошибка: Неверное кол-во вхождений', user)
		except ValueError:
			bot.printMessage('Ошибка: Неверная сумма вхождений', user)
	return addStats
#---------------
def createCommander(user, helpListings, mainLock, player):
	character = {}
	with open('flavorText/firstCharacter/createCharacter/0.dat', encoding = 'utf-8') as file:
		bot.printMessage(file.read(), user)
	mainLock.wait()
	character['flavor'] = getNewMessage(user).get('message')
	character["stats"] = formatCommanderStats(user,helpListings,mainLock,pol.solvePolish(pol.toPolish('40+3d6p1'))['num'],'1.dat','mc',char.constStats)
	character["skills"] = formatCommanderStats(user,helpListings,mainLock,50,'2.dat','mvb',char.constSkills["leader"])

	character["class"] = "leader"

	bot.printMessage('Новая анкета на персонажа! @id{0}'.format(user), '391442603')
	player["characters"].append(character)
#--------------------------------
def createCompany(user, helpListings, mainLock):
	with open('flavorText/firstCharacter/createCompany/0.dat', encoding = 'utf-8') as file:
		bot.printMessage(file.read(), user)
	mainLock.wait()
	return getNewMessage(user).get('message')
#--------------------------------
def firstCharacter(user, helpListings, mainLock, errorLock):
	with open('flavorText/firstCharacter/begin.dat', encoding = 'utf-8') as file:
		bot.printMessage(file.read(), user)
	helpListings[0] = 'm'
	player = {"company":{},"characters":[]}
	while 1:
		errorLock.clear()
		print(errorLock.is_set())
		mainLock.wait()
		selection = getNewMessage(user).get("message")
		if selection == 'Зарегистрировать компанию' or selection == '1':
			with open('flavorText/firstCharacter/companyFirst0.dat', encoding = 'utf-8') as file:
				bot.printMessage(file.read(), user)
			player['company']['flavor'] = createCompany(user, helpListings, mainLock)
			with open('flavorText/firstCharacter/characterFirst0.dat', encoding = 'utf-8') as file:
				bot.printMessage(file.read(), user)
			createCommander(user, helpListings, mainLock,player)
			break
		elif selection == 'Зарегистрировать коммандора' or selection == '2':
			with open('flavorText/firstCharacter/characterFirst0.dat', encoding = 'utf-8') as file:
				bot.printMessage(file.read(), user)
			createCommander(user, helpListings, mainLock,player)
			with open('flavorText/firstCharacter/companyFirst0.dat', encoding = 'utf-8') as file:
				bot.printMessage(file.read(), user)
			player['company']['flavor'] = createCompany(user, helpListings, mainLock)
			break
		else:
			bot.printMessage('Нажмите на одну из кнопок ниже, чтобы продолжить' ,user)
	with open('technical/characters/'+user+'.json','w', encoding = 'utf-8') as file:
		file.write(str(player))
	helpListings[0] = 'ms'
	errorLock.set()
#--------------------------------
def diceCalc(string):
	string = string.lower()
	string = re.sub(r'\s+',r'',string)
	try:
		solved = pol.solvePolish(pol.toPolish(string))
	except:
		return None
	return str(solved['num']) + ' = ' + pol.formatSolved(string, solved['dices'])
#--------------------------------
def init(user):
	helpListings = ['mf']
	if user[:3] == '200':
		helpListings[0] = 'ms'
	if exists("characters/"+str(user)+".json"):
		helpListings[0] = 'ms'
	mainLock = tr.Event()
	errorLock = tr.Event()
	errorLock.set()
	while 1:
		mainLock.clear()
		messageSave = getNewMessage(user)
		message = messageSave.get("message").title()
		admin = messageSave.get("admin")
		peer = messageSave.get("peer")
		if message == 'Помощь':
			print(helpListings)
			answer = ''
			with open('help.dat',encoding = 'utf-8') as file:
				for line in file:
					ans = re.match(r'[' + helpListings[0] + ']\s(.*)', line)
					if ans != None:
						answer += ans.group(1) + '\n'
			bot.printMessage('Введите "Помощь", чтобы увидеть список команд\nВведите "Помощь <команда>" чтобы увидеть подсказку к команде\n\n'+answer+'\n\nтакже, можешь написать "good bot". это не делает ничего, но я те скажу спс', user)
		elif re.match(r'Помощь', message) != None:
			answer = ''
			command = re.match(r'Помощь\s(.*)', message).group(1)
			with open('help.dat',encoding = 'utf-8') as file:
				found = False
				prevListing = ''
				for line in file:
					if re.match(r'[' + helpListings[0] + ']\s(.*)', line) != None:
						prevListing = line[0]
						if re.match(r'[' + helpListings[0] + ']\s(.*)', line).group(1) == command:
							found = True
						else:
							found = False
					elif re.match(r'-\s(.*)', line) != None:
						if re.match(r'-\s(.*)', line).group(1) == command and prevListing in helpListings[0]:
							found = True
					elif re.match(r'.\s', line) != None:
						found = False
					elif found == True:
						if re.match(r'-\s', line) == None:
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
		elif message == 'Нанять' and helpListings[0].find('f') < 0:
			randFile = rand.randint(0,1)
			with open("flavorText/characterBuy/"+str(randFile)+".dat") as file:
				bot.printMessage(file.read(), user)
			buyList = char.characterCreator()
			for character in buyList:
				output = char.characterReader(character)
				bot.printMessage(output, user)
#-----------------------------
		#леня ну мать твою
		elif message == 'Aide':
			bot.printMessage('леня блять', user)
		elif message == 'Good Bot':
			print("why tho")
			with open("technical/good_bot.count") as file:
				goodBotCount = int(file.read())
				goodBotCount += 1
			with open("technical/good_bot.count", "w") as file:
				file.write(str(goodBotCount))
			bot.printMessage("thanks for thanking me "+str(goodBotCount)+" times", user)
#----------------------------
		elif user[:3] != '200':
			if message == 'Начать' and helpListings[0].find('f') >= 0:
				tr.Thread(target = firstCharacter,args =  (user, helpListings, mainLock, errorLock)).start()
			elif errorLock.is_set():
				bot.printMessage('Введите "Помощь" чтобы получить список комманд', user)
			else:
				bot.newMessage.put(messageSave)
#-----------------------------
		elif admin != None:
			if message == 'Бро, Сделай Мне Закреп':
				with open('technical/todo_list.dat', encoding = 'utf-8') as file:
					bot.printMessage(file.read(), user)
				bot.printMessage('Готово', user)
			if message == 'Тест':
				print(bot.pinPrevMessage(user))
		mainLock.set()
		#time.sleep(0.1)
