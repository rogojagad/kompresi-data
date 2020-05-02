# Python 3
import operator
import json
import time
from math import log1p
from collections import Counter

class Encoder:
    def __init__(self):
        self.charDict = dict()
        self.srcText = ""
        self.sortedCharByOccurence = list()
        self.tree = dict()
    
    def runEncode(self):
        self.readInput()

        # Start time

        startTime = time.clock()

        self.makeCount()

        splitIndex = self.getSplitterIndex(self.sortedCharByOccurence)

        left = self.sortedCharByOccurence[:splitIndex]
        right = self.sortedCharByOccurence[splitIndex:]

        self.updateTree(left, 1, "0")
        self.updateTree(right, 1, "1")

        self.buildTree(left, 1, "0")
        self.buildTree(right, 1, "1")

        procTime = time.clock() - startTime

        print("\nCompression time : " + str(procTime) + " seconds")
        
        # print(self.charDict)
        # print(json.dumps(self.tree, indent=1))

        self.performanceMeasure(procTime)

        self.writeEncoded()

        self.makeTreeBackup()

        # print(self.sortedCharByOccurence)

    def readInput(self):
        source = open("input.txt", "r")
        self.srcText = source.read()

    def makeCount(self):
        self.charDict = dict(Counter(self.srcText))

        charList = sorted(self.charDict.items(), key=operator.itemgetter(1), reverse=True)

        for char in charList:
            self.sortedCharByOccurence.append(char[0])

    def getSplitterIndex(self, charList):
        total = 0

        for char in charList:
            total += self.charDict[char]

        count = 0
        splitterIndex = 0

        for i in range(len(charList) // 2):
            char = charList[i]
            count += self.charDict[char]

            if (count - (total/2) >= 0):
                splitterIndex = i + 1
                break
        
        return splitterIndex

    def buildTree(self, chrList, itrCount, bit):
        # print(chrList)
        if len(chrList) == 1:
            self.updateTree(chrList[0], itrCount + 1, "0")
        elif len(chrList) == 2:
            self.updateTree(chrList[0], itrCount + 1, "0")
            self.updateTree(chrList[1], itrCount + 1, "1")
        else:
            splitIndex = self.getSplitterIndex(chrList)

            self.updateTree(chrList[:splitIndex+1], itrCount + 1, "0")
            self.updateTree(chrList[splitIndex+1:], itrCount + 1, "1")
            
            self.buildTree(chrList[:splitIndex+1], itrCount + 1, "0")
            self.buildTree(chrList[splitIndex+1:], itrCount + 1, "1")

    def updateTree(self, chrList, itrCount, bit):
        for char in chrList:
            if char not in self.tree:
                # self.tree[char] = [itrCount, bit, self.charDict[char]]
                self.tree[char] = {
                    'Code length' : itrCount,
                    'Code' :  bit,
                    'Frequency' : self.charDict[char],
                }
            else:
                self.tree[char]['Code length'] += 1
                self.tree[char]['Code'] += bit

    def performanceMeasure(self, procTime):
        # output = open("output-encoded.txt", "w")
        compressedBitsCount = 0

        for char, data in self.tree.items():
            compressedBitsCount += data['Code length'] * data['Frequency']

        originalBitCounts = len(self.srcText) * 8

        print("\nOriginal bits count : " + str(originalBitCounts))
        print("Bits count after compression : " + str(compressedBitsCount))
        print("Compression ratio : " + str( originalBitCounts /compressedBitsCount))
        print("Compression Speed :" + str(originalBitCounts/procTime) + " bit/sec")
        print("Space Savings : " + str( 1 - (compressedBitsCount / originalBitCounts) ))
        print("Compression Gain : " + str( 100 * log1p( originalBitCounts /compressedBitsCount) ))

    def writeEncoded(self): 
        output = open("output-encoded.txt", "w")

        for char in self.srcText:
            output.write(self.tree[char]['Code'] + ' ')

    def makeTreeBackup(self):
        backup = dict()

        for char, data in self.tree.items():
            backup[char] = data["Code"]

        with open("tree.json", "w") as tree:
            json.dump(backup, tree)

if __name__ == "__main__":
    sf = Encoder()

    sf.runEncode()

    # sf.runDecode()