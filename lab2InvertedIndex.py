import re
from stemming.porter2 import stem
import matplotlib.pyplot as plt
from collections import OrderedDict

stop = []
index = {}
collections =["sample","trec.sample"]
def readStopWords():
    f = open ("stopWords.txt")
    for x in f:
        stop.append(x.strip())
def readSamples():
    global collections
    for collection in collections:
        f = open("collections/"+collection+".txt")
        for x in f:
            if "ID:" in x:
                id_var = x.split(":")[1].strip()
            else:
                text = x.split(":")[1]
                processText(id_var,text)
        saveIndex(collection)
        global index
        index={}
def buildInvertedIndex(id_var,words):
    for i,word in enumerate(words,1):
        if word not in index:
            # first push
            index[word] = {id_var:[i]}
        else:
            # more push
            documents = index[word].keys()
            if id_var not in documents:
                index[word][id_var]=[i]
            else: index[word][id_var].append(i)
def processText(id_var,text):
    processedWords= []
    unprocessedWords = 0
    unique = {}
    regex = re.compile('[^a-zA-Z]')
    for word in text.split():
        unprocessedWords+=1
        if word not in unique:
            unique[word] = 1
        else:
            unique[word] = unique.get(word)+1
        token = regex.sub('',word.lower())
        if token not in stop:
            if stem(token).strip() != "":
                processedWords.append(stem(token).strip())
    buildInvertedIndex(id_var,processedWords)
def saveIndex(title):
    title= title+"Index.txt"
    f = open(title,"w+")
    for word in index:
        f.write("%s:\n" % word)
        for doc in index[word]:
            f.write("\t%s: %s\n"%(doc,",".join(str(x) for x in index[word][doc])))
def readIndex(title):
    title = title+"Index.txt"
    f = open(title)
    index = {}
    documents = []
    for line in f:
        if(line.split(":")[1].strip()==""):
            word = line.split(":")[0]
            index[word]={}
        else:
            document = line.split(":")[0].strip()
            positions =line.split(":")[1].split(",")
            if document not in documents:
                documents.append(document)
            for x in positions:
                pos = x.strip()
                if (document not in index[word]):
                    index[word][document]=[pos]
                else:
                    index[word][document].append(pos)
    return index,documents

def main():
    readSamples()
if __name__ == "__main__" :
    main()

