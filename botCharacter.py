import re
import random as rand
import polishCalc as pol
#--------------------------------
genderChance = 0.5
nicknameChance = 0.3
#--------------------------------
constStats = [["INT","Интеллект"],["REF","Рефлексы"],["CHAR","Харизма"],["TECH","Техническе Навыки"],["LUCK","Удача"],["MA","Скорость Бега"],["BODY","Телосложение"],["EM","Эмпатия"]]
constClasses = ["leader","marksman","medic","techie"]
constSkills = {}
constSkills["leader"] = [["Notice","Внимательность"],["Handgun","Пистолеты"],["Submachine gun","Пистолеты-пулеметы"],["Rifle","Винтовки"],["Dodge","Уворот"],["Melee","Рукопашная"],["Interrogation","Допрос"],["Oratory","Красноречие"],["Leadership","Руководство"],["Intimidate","Запугивание"],["Weaponsmith","Обращение с оружием"]]
constSkills["marksman"] = [["Notice","Внимательность"],["Handgun","Пистолеты"],["Submachine gun","Пистолеты-пулеметы"],["Rifle","Винтовки"],["Heavy weapons","Тяжелое оружие"],["Dodge","Уворот"],["Melee","Рукопашная"],["Intimidate","Запугивание"],["Athletics","Атлетика"],["Stealth","Скрытность"],["Weaponsmith","Обращение с оружием"]]
constSkills["medic"] = [["Notice","Внимательность"],["Handgun","Пистолеты"],["Submachine gun","Пистолеты-пулеметы"],["Dodge","Уворот"],["Melee","Рукопашная"],["First Aid","Первая помощь"],["Diagnose","Диагностирование"],["Pharmaceuticals","Фармацевтика"],["Wilderness Survival","Выживание в дикой среде"],["Surgery","Оперирование"],["Weaponsmith","Обращение с оружием"]]
constSkills["techie"] = [["Notice","Внимательность"],["Handgun","Пистолеты"],["Rifle","Винтовки"],["Dodge","Уворот"],["Melee","Рукопашная"],["Driving","Вождение"],["Maintenance","Техобслуживание"],["Electronics","Электроника"],["Demolitions","Взрывчатка"],["Fortification","Укрепления"],["Weaponsmith","Обращение с оружием"]]
#--------------------------------
def commanderStats(message, maxLevel, statList):
    stat = {}
    statRegex = re.compile(r'([^0-9]+\s|\s*)(\d+)')
    char = statRegex.findall(message)
    print(char)
    if len(char) != len(statList):
        raise SyntaxError
    sum = 0
    for entry in char:
        entry[0].strip()
        isStat = False
        for test in statList:
            try:
                test.index(entry[0])
                isStat = True
                stat[test[0]] = int(entry[1])
                break
            except ValueError:
                pass
        if not isStat:
            for test in statList:
                if stat.get(test[0]) == None:
                    stat[test[0]] = int(entry[1])
                    break
        if int(entry[1]) > 10:
            raise SyntaxError
        sum += int(entry[1])
    print("sum = {}".format(sum))
    if sum != maxLevel:
        raise ValueError
    return stat
#--------------------------------
def characterStats(statGen,statList):
    stat = {}
    sumLevel = 0
    for entry in statList:
        stat[entry[0]] = int(pol.solvePolish(pol.toPolish(statGen))["num"])
        sumLevel += stat[entry[0]]
    return {"stat":stat, "sum":sumLevel}
#--------------------------------
def characterNameGen(character, gend):
    countries = ["russian","swedish","japanese","mexican"]
    gender = ["Male","Female"]
    country = rand.choice(countries)
    character.update({"country":country})
    with open("flavorText/names/firstNames/"+country+gender[gend]+".dat", encoding = 'utf-8') as file:
        buffer = []
        for line in file:
            buffer.append(line)
        character.update({"name":rand.choice(buffer).strip()})
    with open("flavorText/names/nicknames.dat", encoding = 'utf-8') as file:
        buffer = []
        for line in file:
            buffer.append(line)
        character.update({"nickname":rand.choice(buffer).strip()})
    search = country
    if country == "russian":
        search += gender[gend]
    with open("flavorText/names/secondNames/"+search+".dat", encoding = 'utf-8') as file:
        buffer = []
        for line in file:
            buffer.append(line)
        character.update({"secondName":rand.choice(buffer).strip()})
#--------------------------------
def characterCreator():
    charList = []
    characterAmount = 3

    i = 0
    min = 0
    max = 50

    while i < characterAmount:
        character = {}
        if rand.random() < genderChance:
            character["gender"] = 0
            gender = 0
        else:
            character["gender"] = 1
            gender = 0
        characterNameGen(character, character["gender"])

        if rand.random() >= nicknameChance:
            character["nickname"] = ""

        stats = {"sum":-1}
        while stats["sum"] <= min or stats["sum"] >= max:
            stats = characterStats("1d10",constStats)
        character["stats"] = stats["stat"]

        randClass = rand.randint(0,3)
        if randClass == 0:
            character["class"] = "leader"
        elif randClass == 1:
            character["class"] = "marksman"
        elif randClass == 2:
            character["class"] = "medic"
        elif randClass == 3:
            character["class"] = "techie"

        skills = {"sum":-1}
        while skills["sum"] <= min or skills["sum"] >= max:
            skills = characterStats("1d11-1",constSkills[character["class"]])
        character["skills"] = skills["stat"]

        character["cost"] = (stats["sum"]+skills["sum"])*(10*(max+25))

        charList.append(character)
        i += 1
        min += 25
        max += 25
    return charList
#--------------------------------
def characterReader(character):
    output = ""
    output += character["name"] + " "
    if character["nickname"] != "":
         output += '"' + character["nickname"] + '" '
    output += character["secondName"] + "\n"

    string = ""
    if character["country"] == "russian":
        string += "Россия"
    elif character["country"] == "swedish":
        string += "Швеция"
    elif character["country"] == "japanese":
        string += "Япония"
    elif character["country"] == "mexican":
        string += "Мексика"
    string += ", "
    if character["gender"] == 0:
        string += "Мужчина"
    else:
        string += "Женщина"
    output += string + "\n"

    output += "$"+str(character["cost"]) + "\n\n"

    i = 0
    for statName, stat in character["stats"].items():
        output += str(stat)+" "+constStats[i][1]+"\n"
        i += 1
    output += "\n"

    output += "Класс: "
    if character["class"] == "leader":
        output += "Лидер"
    if character["class"] == "marksman":
        output += "Марксман"
    if character["class"] == "medic":
        output += "Медик"
    if character["class"] == "techie":
        output += "Техник"
    output += "\n"

    i = 0
    for skillName, skill in character["skills"].items():
        if skill != 0:
            output += str(constSkills[character["class"]][i][1])+" "+str(skill)+"\n"
        i += 1
    return output;
