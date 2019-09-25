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
    return {'num':str(num), 'dices':ret}
#--------------------------------
def toPolish(string):
    stack, output = [], []
    number = ''
    for char in string:
        if re.match('[0-9]',char) != None:
            number += char
            continue
        elif number != '':
            output.append(number)
            number = ''

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
                if stack[-1] == 'd':
                    output.append(stack.pop())
            elif char == '^':
                if re.match('[d^]', stack[-1]) != None:
                    output.append(stack.pop())
            elif re.match('[*/]', char) != None:
                if re.match('[d^*/]', stack[-1]) != None:
                    output.append(stack.pop())
            elif re.match('[+-]', char) != None:
                if re.match('[d^*/+-]', stack[-1]) != None:
                    output.append(stack.pop())
        stack.append(char)
        print(stack)
        print(output)

    if number != '':
        output.append(number)
    while len(stack) > 0:
        a = stack.pop()
        if a == '(':
            raise SyntaxError
        else:
            output.append(a)
    print(output)
    return output
#--------------------------------
def solvePolish(line):
    stack = []
    dices = []
    for char in line:
        if char == 'n':
            stack[-1] = str(-int(stack[-1]))
        elif char == 'd':
            b = int(stack.pop())
            a = int(stack.pop())
            c = diceRoll(a, b)
            stack.append(c['num'])
            dices.append(c['dices'])
        elif char == '^':
            b = int(stack.pop())
            a = int(stack.pop())
            c = a ** b
            stack.append(c)
        elif char == '/':
            b = int(stack.pop())
            a = int(stack.pop())
            if b == 0:
                raise SyntaxError
            c = int(a / b)
            stack.append(c)
        elif char == '*':
            b = int(stack.pop())
            a = int(stack.pop())
            c = a * b
            stack.append(c)
        elif char == '-':
            b = int(stack.pop())
            a = int(stack.pop())
            c = a - b
            stack.append(c)
        elif char == '+':
            b = int(stack.pop())
            a = int(stack.pop())
            c = a + b
            stack.append(c)
        else:
            stack.append(char)
    ret = {}
    if len(stack) > 1:
        raise SyntaxError
    ret['num'] = stack[0]
    ret['dices'] = dices
    return ret
#--------------------------------
def cutDices(string, dices):
    for dice in dices:
        string = re.sub(r'\d+d\d+',str(dice['num']) + str(dice['dices']), string, 1)
    return string
