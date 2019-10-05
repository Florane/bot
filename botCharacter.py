import re
#--------------------------------
def commanderStats(message, maxLevel, statList):
    stat = {}
    statRegex = re.compile(r'([^0-9]+|)\s(\d+)')
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
        sum += int(entry[1])
    print("sum = {}".format(sum))
    if sum != maxLevel:
        raise ValueError
    return stat
#--------------------------------
