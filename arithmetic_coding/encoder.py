# Python 3
import operator
import json
import time
import random
from floatToBin import *
from decimal import *
from collections import Counter
from math import log1p

# Input generated at http://www.unit-conversion.info/texttools/random-string-generator/

class Encoder:
    def __init__(self):
        self.probabilityDict = dict()
        self.charRange = dict()
        self.srcText = ""
        self.finalResult = 0
        getcontext().prec = 2

    def run(self):
        self.prepare()
        
        self.buildRange(0, 1)

        self.encode()

        self.performanceMeasure()

        self.dumpLookupData()

    def prepare(self):
        self.readSource()

        self.setCharProb()

        self.checkProbTruth()

    def dumpLookupData(self):
        with open("probability-dict.json", "w") as tree:
            json.dump(self.probabilityDict, tree)

        with open("encoder-range-dict.json", "w") as tree:
            json.dump(self.charRange, tree)

        length = open("source-length.txt", "w")
        length.write(str(len(self.srcText)))

    def buildRange(self, mostLower, mostUpper):
        currentLower = mostLower
        for char, prob in self.probabilityDict.items():
            currentUpper = ((mostUpper - mostLower) * prob) + currentLower

            currentRange = [currentLower, currentUpper]

            self.charRange[char] = currentRange

            currentLower = currentUpper
        # print(self.charRange)

    def readSource(self):
        source = open("raw_src.txt", "r")
        self.srcText = source.read().strip()

    def setCharProb(self):
        charNum = int(input("Berapa banyak karakter yang ingin dimasukkan?\n"))

        for i in range(charNum):
            charAndProb = input("Masukkan karakter dan probability nomor " + str(i + 1) + "\n")
            
            self.assignCharProb(charAndProb.split(' ')[0], float(charAndProb.split(' ')[1]))

    def assignCharProb(self, key, prob):
        self.probabilityDict[key] = prob

    def checkProbTruth(self):
        sum = 0

        for char, prob in self.probabilityDict.items():
            sum += prob
        print(sum)
        if sum != 1:
            print("\nJumlah total probability tidak sama dengan 1 !!!!")
            exit()

    def encode(self):
        print("\nMemulai Proses Encoding\n")

        startTime = time.clock()

        selectedRange = []

        for char in self.srcText:
            selectedRange = self.charRange[char]

            print("Karakter saat ini adalah : " + char)
            print(self.charRange)
            print("Selected range : ", end='')
            print(selectedRange, end="\n\n")

            self.buildRange(selectedRange[0], selectedRange[1])

        randomPicked = random.uniform(selectedRange[0],selectedRange[1])

        self.finalResult = randomPicked

        print("Angka yang diambil : " + str(randomPicked))

        print("Waktu yang dibutuhkan untuk encoding : " + str(time.clock() - startTime))

        result = open("encode-result.txt", "w")
        result.write(str(self.finalResult))

    def performanceMeasure(self):
        resultSize = self.getResultSize()

        sourceSize = len(self.srcText) * 8

        print("Compression ratio : " + str(sourceSize / resultSize))
        print("Space Savings : " + str( 1 - (resultSize / sourceSize) ))
        print("Compression Gain : " + str( 100 * log1p( sourceSize / resultSize) ))

    def getResultSize(self):
        converted = float_bin(self.finalResult, places = 7)

        decimalLen = len(converted.split(".")[0])
        floatingLen = len(converted.split(".")[1])
        return decimalLen + floatingLen

if __name__ == "__main__":
    enc = Encoder()

    enc.run()