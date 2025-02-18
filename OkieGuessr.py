# Author: Cédric (@cedric10012002)
# Date: 18/02/2025
import csv
import logging
import numpy as np
from random import choice
from datetime import datetime
from cryptography.fernet import Fernet

# https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
# A dummy key of course
OBJ = Fernet("j6BPsuMV80Y0iP6jAYzN68iEw7x0dw12bn7AhQanEY4=")
LOG = logging.getLogger(__name__)


def averageIncome(n, minBet, delta):
    return ((n + 1) * (2 * minBet + (n - 1) * delta)) / 4


def displayAverageIncome(minBet, maxBet, delta):
    deltaDiff = (maxBet - minBet)
    n = deltaDiff / delta + 1
    LOG.info("Average income: $%.2f" % (averageIncome(n, minBet, delta)))


def askMinBet():
    minBet = input("\nWhat is the minimum bet?: $")
    if not minBet.replace('.', '', 1).isdigit():
        print("Invalid minimum bet: non-numeric input or negative number.")
        return askMinBet()
    elif float(minBet) == 0:
        print("Invalid minimum bet: the minimum bet cannot be equal to $0.")
        return askMinBet()
    else:
        return float(minBet)


def askMaxBet(minBet):
    maxBet = input("What is the maximum bet?: $")
    if not maxBet.replace('.', '', 1).isdigit():
        print("Invalid maximum bet: non-numeric input or negative number.\n")
        return askMaxBet(minBet)
    elif float(maxBet) <= minBet:
        print("Invalid maximum bet: the maximum bet must be greater than the minimum bet.\n")
        return askMaxBet(minBet)
    else:
        return float(maxBet)


def askDelta(minBet, maxBet):
    delta = input("What is the size of increments?: $")
    if not delta.replace('.', '', 1).isdigit():
        print("Invalid increment size: non-numeric input or negative number.\n")
        return askDelta(minBet, maxBet)
    elif float(delta) == 0:
        print("Invalid increment size: the increment size cannot equal 0.\n")
        return askDelta(minBet, maxBet)
    elif (maxBet - minBet) % float(delta) == 0:
        return float(delta)
    else:
        print("Invalid increment size: the difference of the maximum and minimum bet is."
              " not a multiple of the increment size.\n")
        return askDelta(minBet, maxBet)


def displayBets(hiddenNum, bets, pastBets):
    formattedBets = map(lambda i: '$' + '%g' % i, bets)
    print(*formattedBets, sep=' | ')
    newBet = input("What is the next bet?: $")
    if not newBet.replace('.', '', 1).isdigit():
        print("Invalid bet: non-numeric input or negative number.\n")
        displayBets(hiddenNum, bets, pastBets)
    elif float(newBet) not in bets:
        print("This bet is not present in the list!\n")
        pastBets.append(float(newBet))
        writeSession(hiddenNum, bets, pastBets)
        displayBets(hiddenNum, bets, pastBets)
    elif float(newBet) == hiddenNum:
        print("The hidden number was $%g!" % hiddenNum)
        pastBets.append(float(newBet))
        income = sum(pastBets)
        LOG.info("Income: $%g" % income)
        input("Press enter to start a new session:")
    else:
        print("That wasn't the hidden number, try again.\n")
        bets.remove(float(newBet))
        pastBets.append(float(newBet))
        writeSession(hiddenNum, bets, pastBets)
        displayBets(hiddenNum, bets, pastBets)


def writeSession(hiddenNum, bets, pastBets):
    data = [[hiddenNum, bets, pastBets]]
    with open('sessionData.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    encryptFile()


def readSession():
    decryptFile()
    with open('sessionData.csv', mode='r') as csvfile:
        reader = csv.reader(csvfile)
        data = next(reader)
    return list(map(eval, data))


def encryptFile():
    with open('sessionData.csv', 'rb') as file:
        original = file.read()
    encrypted = OBJ.encrypt(original)
    with open('sessionData.csv', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decryptFile():
    with open('sessionData.csv', 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = OBJ.decrypt(encrypted)
    with open('sessionData.csv', 'wb') as dec_file:
        dec_file.write(decrypted)


def recoverSession():
    data = readSession()
    hiddenNum = data[0]
    bets = data[1]
    pastBets = data[2]
    windowShortening(hiddenNum, bets)
    displayBets(hiddenNum, bets, pastBets)


def windowShortening(hiddenNum, bets):
    amount = input("Window shortening: How much elements should be removed? (0 for none): ")
    print()
    if not amount.isnumeric():
        print("Invalid amount: the amount of elements should be an integer.\n")
        return windowShortening(hiddenNum, bets)
    else:
        amount = int(amount)
        if amount >= len(bets) or amount < 0:
            print("Invalid amount: the amount should be smaller than the length of the list and non-negative.\n")
            return windowShortening(hiddenNum, bets)
        else:
            while amount != 0:
                toBeRemoved = choice(bets)
                if toBeRemoved != hiddenNum:
                    bets.remove(toBeRemoved)
                    amount -= 1
            return bets


def newSession():
    LOG.info("New session started.")
    minBet = askMinBet()
    maxBet = askMaxBet(minBet)
    delta = askDelta(minBet, maxBet)
    print()
    displayAverageIncome(minBet, maxBet, delta)
    bets = np.arange(minBet, maxBet + delta, delta).tolist()
    hiddenNum = choice(bets)
    displayBets(hiddenNum, bets, [])


if __name__ == '__main__':
    logging.basicConfig(filename='sessionsInfo.log', level=logging.INFO)
    LOG.info("\n%s", datetime.now())
    print("Welcome Okie! Ready to drop your inventory today?\n")
    ans = input("Do you want to use the previous session? (y/n): ")
    if ans == "y":
        recoverSession()
    while True:
        newSession()
