from collections import Counter
import json

def getCountChar(text):
    data = dict(Counter(text))

    return data

def getCharProb(charCount, strLen):
    charProb = dict()

    for char, count in charCount.items():
        charProb[char] = count / strLen

    return charProb

def getCharProbList(charProb):
    probLst = list()
    charLst = list()

    for char, prob in charProb.items():
        charLst.append(char)
        probLst.append(prob)

    return charLst, probLst

def tunstall(alphabet, dist, n):
    size = len(alphabet)
    iterations = (2 ** n - size) // (size - 1)
 
    t = []
    for i, s in enumerate(alphabet):
        t.append( [s, dist[i]] )
 
    for _ in range(iterations):
        d = max(t, key=lambda p:p[1])
        ind = t.index(d)
        seq, seqProb = d
         
        for i, s in enumerate(alphabet):
            t.append( [seq + s, seqProb * dist[i]] )
        del t[ind]
 
    for i, entry in enumerate(t):
        entry[1] = '{:03b}'.format(i)
     
    return t

def toJson(result):
    temp = dict()

    for data in result:
        temp[data[0]] = data[1]

    return temp

if __name__=="__main__":
    text = input()

    charCount = getCountChar(text)
    
    charProb = getCharProb(charCount, len(text))

    alphabet, prob = getCharProbList(charProb)

    print(alphabet)

    print(prob)

    n = len(alphabet)

    result = tunstall(alphabet, prob, n)

    resultInJson = toJson(result)

    with open("result.json", "w") as result:
        json.dump(resultInJson, result)