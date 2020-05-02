# Python 3
import operator
import json
import time
import random
from decimal import *
from collections import Counter

class Decoder:
    def __init__(self):
        self.inputNum = self.readInput()
        self.charProbability = self.readProbability()
        self.srcLength = self.readSrcLength()
        self.charRange = dict()
        self.resultStr = ""

    def readSrcLength(self):
        length = open("source-length.txt", "r")
        return int(length.read())

    def readProbability(self):
        with open('probability-dict.json') as data:
            return json.load(data)

    def readInput(self):
        source = open("encode-result.txt", "r")
        return float(source.read())

    def run(self):
        self.buildRange(0,1)

        self.decode(self.srcLength)

        self.dumpResultData()

    def dumpResultData(self):
        output = open("decode-result.txt", "w")
        output.write(self.resultStr)

        with open("decoder-range-dict.json", "w") as tree:
            json.dump(self.charRange, tree)

    def decode(self, length):
        print("\nMemulai Proses Decoding\n")

        startTime = time.clock()

        for i in range(length):
            keyChar, selectedRange = self.getRangeAndChar()

            print("Range yang dipilih : ",end=' ')
            print(selectedRange)
            print("Karakter didapatkan : " + keyChar + "\n")

            self.resultStr += keyChar

            self.buildRange(selectedRange[0], selectedRange[1])

        endTime = time.clock() - startTime

        print("Waktu yang dibutuhkan untuk encoding : " + str(endTime))

    def buildRange(self, mostLower, mostUpper):
        currentLower = mostLower
        rangeDist = mostUpper - mostLower

        for char, prob in self.charProbability.items():
            currentUpper = (rangeDist * prob) + currentLower

            currentRange = [currentLower, currentUpper]

            self.charRange[char] = currentRange

            currentLower = currentUpper

    def getRangeAndChar(self):
        for char, probRange in self.charRange.items():
            if self.inputNum >= probRange[0] and self.inputNum < probRange[1]:
                return char, probRange

if __name__ == "__main__":
    dc = Decoder()
    dc.run()