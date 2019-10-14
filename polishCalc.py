import re
import random as rand
#--------------------------------
def diceRoll(amount, sides):
    amount = int(amount)
    sides = int(sides)
    num = 0
    dices = []
    i = 0
    while i < amount:
        new = rand.randint(1,sides)
        num += new
        dices.append(new)
        i+=1

    ret = {}
    ret['num'] = str(num)
    ret['dices'] = dices
    return ret
#--------------------------------
def toPolish(string):
    stack, output = [], []
    number = ''
    for char in string:
        if number == 'a':
            number = ''
        #print('1 ' + str(output))
        #print('2 ' + str(stack))
        #print('3 ' + str(number))
        #print('-------')
        if re.match('[0-9]',char) != None:
            number += char
            continue
        elif number != '':
            output.append(number)
            number = 'a'

        if char == ')':
            a = ''
            while a != '(':
                if len(stack) == 0:
                    raise SyntaxError
                if a != '':
                    output.append(a)
                a = stack.pop()
            continue

        if char == '-' and number == '':
            char = 'n'
        elif len(stack) > 0:
            if char == 'd':
                if re.match('[dp]', stack[-1]):
                    output.append(stack.pop())
            elif char == 'p':
                if stack[-1] == 'd':
                    stack[-1] = 'p'
                else:
                    raise SyntaxError
                continue
            elif char == '^':
                if re.match('[dp^]', stack[-1]) != None:
                    output.append(stack.pop())
            elif re.match('[*/]', char) != None:
                if re.match('[dp^*/]', stack[-1]) != None:
                    output.append(stack.pop())
            elif re.match('[+-]', char) != None:
                if re.match('[dp^*/+-]', stack[-1]) != None:
                    output.append(stack.pop())
        stack.append(char)

    if number == 'a':
        number = ''
    if number != '':
        output.append(number)
    while len(stack) > 0:
        a = stack.pop()
        if a == '(':
            raise SyntaxError
        else:
            output.append(a)
    #print(output)
    return output
#--------------------------------
def solvePolish(line):
    stack = []
    dices = []
    for char in line:
        #print('b ' + str(stack))
        #print(str(char == '-'))
        if char == 'n':
            stack[-1] = str(-int(stack[-1]))
        elif re.match(r'[dp^/*\-+]', char):
            b = int(stack.pop())
            a = int(stack.pop())
            if char == 'd':
                c = diceRoll(a, b)
                #print(c)
                dices.append(c)
                c = c['num']
            elif char == 'p':
                d = int(stack.pop())
                #print(stack)
                c = diceRoll(d, a)
                i = 0
                while i < b:
                    min = -1
                    pos = 0
                    iter = 0
                    for die in c['dices']:
                        intDie = int(die)
                        if min == -1 or intDie < min:
                            pos = iter
                            min = intDie
                        iter += 1
                    c['num'] = str(int(c['num']) - min)
                    #print(c['dices'])
                    c['dices'].pop(pos)
                    i += 1
                dices.append(c)
                c = c['num']
            elif char == '^':
                c = a ** b
            elif char == '/':
                if b == 0:
                    raise SyntaxError
                c = int(a / b)
            elif char == '*':
                c = a * b
            elif char == '-':
                c = a - b
            elif char == '+':
                c = a + b
            stack.append(c)
        else:
            stack.append(char)
        #print('a ' + str(stack))
    ret = {}
    if len(stack) > 1:
        raise SyntaxError
    ret['num'] = stack[0]
    ret['dices'] = dices
    return ret
#--------------------------------
def formatSolved(string, dices):
    #print(string)
    #print(dices)
    for dice in dices:
        string = re.sub(r'(\d+|\(.+\))d(\d+|\(.+\))(p{0,1}(\(.+\)|\d+)|)',str(dice['num']) + str(dice['dices']), string, 1)
    return string
