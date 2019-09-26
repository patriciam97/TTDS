import re
from stemming.porter2 import stem
import matplotlib.pyplot as plt
from collections import OrderedDict

stop = []
processedWords= []
unprocessedWords = 0
unique = {}
def readStopWords():
    f = open ("stopWords.txt")
    for x in f:
        stop.append(x.strip())
def process():
    x = []
    y = []
    global unprocessedWords
    bible=open("pg10.txt", "r")
    contents =bible.read()
    regex = re.compile('[^a-zA-Z]')
    for word in contents.split():
        unprocessedWords+=1
        if word not in unique:
            unique[word] = 1
        else:
            unique[word] = unique.get(word)+1
        token = regex.sub('',word.lower())
        if token not in stop:
            if stem(token).strip() != "":
                processedWords.append(stem(token).strip())
        x.append(len(unique.keys()))
        y.append(unprocessedWords)
    printHeaps(x,y)


def printHeaps(x,y):
    plt.plot(x,y)
    plt.xticks([])
    plt.yticks([])
    plt.show()
def printZipfs():
    dd = OrderedDict(sorted(unique.items(), key=lambda x: x[1],reverse=True))
    x = list(dd.values())
    y = list(range(1,len(unique)+1))
    plt.plot(x ,y)
    plt.xticks([])
    plt.yticks([])
    plt.show()
def printBeford():
    dd = OrderedDict(sorted(unique.items(), key=lambda x: x[1],reverse=True))
    x = list(map(lambda x: int(str(x)[0]), list(dd.values())))
    y = list(range(1,len(dd)+1))
    plt.plot(x ,y )
    plt.xticks([])
    plt.yticks([])
    plt.show()
def main():
    readStopWords()
    process()
    print("Unprocessed Words: ",unprocessedWords)
    print("Processed Words: ",len(processedWords))
    print("Unique Words: ",len(unique))
    # printZipfs()
    # printBeford()

if __name__ == "__main__" :
    main()