from random import randint

def randUpper():
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    index = randint(0, 25)
    return upper[index]

def randLower():
    lower = "abcdefghijklmnopqrstuvwxyz"
    index = randint(0, 25)
    return lower[index]

def randNumber():
    numbers = "1234567890"
    index = randint(0, 9)
    return numbers[index]

def randSpecial():
    special = "!@#$%&?"
    index = randint(0, 6)
    return special[index]

def generate():
    password = ""

    for _ in range(4):
        order = randint(0, 3)
        match order:
            case 0:
                password += randLower()
                password += randSpecial()
                password += randUpper()
                password += randNumber()
            case 1:
                password += randSpecial()
                password += randUpper()
                password += randNumber()
                password += randLower()
            case 2:
                password += randUpper()
                password += randNumber()
                password += randLower()
                password += randSpecial()
            case 3:
                password += randNumber()
                password += randLower()
                password += randSpecial()
                password += randUpper()
    return password