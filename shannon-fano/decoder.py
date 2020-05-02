# Python 3

import json
import time

debug = ""

class Decoder:
    def __init__(self):
        self.encodedText = ""

    def runDecode(self): 
        with open('tree.json', 'r') as tree:
            self.tree = json.load(tree)

        self.readDecoded()

        codeList = self.encodedText.split(' ')

        self.decodeAndPrint(codeList)

        self.performanceMeasure()

    def readDecoded(self):
        source = open("output-encoded.txt", "r")
        self.encodedText = source.read()

    def decodeAndPrint(self, codeList):
        result = ""
    
        for char in codeList:
            # print(char)
            alphabet = self.getAlphabet(char)
            debug = char

            try:
                result += alphabet
            except TypeError:
                print(debug)
            #     print(e)

        output = open("output-decoded.txt", "w")
        output.write(result)

    def getAlphabet(self, target):
        for char, code in self.tree.items():
            if target == code: 
                return char
    
    def performanceMeasure(self): pass

if __name__ == "__main__":
    dc = Decoder()

    dc.runDecode()