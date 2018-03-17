#BASIC functions for Python - Super Multi-Purpose

def getInt(prompt="Please give a number"):
    num = -1
    done = False
    while not done:
        try:
            num = int(input(prompt))
            done = True
        except ValueError:
            done = False
    return num
