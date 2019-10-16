import re
from stemming.porter2 import stem
import matplotlib.pyplot as plt
from collections import OrderedDict

stop = []
index = {}
indexNoStem = {}
documents = []
collections =["sample","trec.sample"]

def read_stop_words():
    f = open ("stopWords.txt")
    for x in f:
        stop.append(x.strip())

def read_samples():
    global collections,index,documents
    for collection in collections:
        index = {}
        documents = []
        f = open("collections/"+collection+".txt")
        for x in f.readlines():
            if "ID:" in x:
                doc_id = x.split(":")[1].strip()
            if "TEXT:" in x:
                text = x[5:].strip()
                process_text(doc_id,text)
        save_inverted_index(collection)

def build_inverted_index ():
    read_samples()
    
def generate_index(doc_id,words,wordsNoStemming): 
    # words are processed - tokenize, stopping and stemming
    for i,word in enumerate(words,0):
        if word not in index:
            # first push
            index[word] = {doc_id:[i]}
        else:
            # more push
            documents = index[word].keys()
            if doc_id not in documents:
                index[word][doc_id]=[i]
            else: index[word][doc_id].append(i)

        if wordsNoStemming[i] not in indexNoStem:
            # first push
            indexNoStem[wordsNoStemming[i]] = {doc_id:[i]}
        else:
            # more push
            documents =  indexNoStem[wordsNoStemming[i]].keys()
            if doc_id not in documents:
                 indexNoStem[wordsNoStemming[i]][doc_id]=[i]
            else: indexNoStem[wordsNoStemming[i]][doc_id].append(i)

def sub_array(arr,start,n): 
    # from start get n next elements
    result = []
    for i in list(range(start,start+n)):
        result.append(arr[i].lower())
    return result

def process_text_for_n_gram(doc_id,text,n):
    text = text.split()
    arr = []
    processedPhrases = []
    processedPhrasesNoStem = []
    for i,word in enumerate(text,0):
        if i<(len(text)-n+1):
            arr.append(sub_array(text,i,n))
    for pair in arr:
        pair = [x.strip().replace(",","").replace(".","") for x in pair]
        phrase = "_".join(pair)
        processedPhrasesNoStem.append(phrase)
        pair = [ stem(x) if len(x)>3 else x for x in pair]
        phrase = "_".join(pair)
        processedPhrases.append(phrase)
    generate_index(doc_id,processedPhrases,processedPhrasesNoStem)

def build_n_gram(n): 
    # words are unprocessed
    global collections
    for collection in collections:
        f = open("collections/"+collection+".txt")
        for x in f:
            if "ID:" in x:
                doc_id = x.split(":")[1].strip()
            else:
                text = x[5:].strip()
                process_text_for_n_gram(doc_id,text,n)
        save_n_gram_index(collection,n)

def process_text(doc_id,text):
    processedWords= []
    processedWordsWithoutStem= []
    regex = re.compile('[^a-zA-Z]')
    for word in text.split(" "):
        token = regex.sub('',word.lower())
        if token not in stop:
            if stem(token.strip()) != "":
                processedWords.append(stem(token.strip()))
            processedWordsWithoutStem.append(token.strip())
    generate_index(doc_id,processedWords,processedWordsWithoutStem)

def save_inverted_index(title):
    file_Title= "indexes/inverted_Index/"+title+".txt"
    f = open(file_Title,"w+")
    for word in index:
        f.write("%s:\n" % word)
        for doc in index[word]:
            f.write("\t%s: %s\n"%(doc,",".join(str(x) for x in index[word][doc])))
    
    file_Title= "indexes/inverted_Index/"+title+"_no_Stem.txt"
    f = open(file_Title,"w+")
    for word in indexNoStem:
        f.write("%s:\n" % word)
        for doc in indexNoStem[word]:
            f.write("\t%s: %s\n"%(doc,",".join(str(x) for x in indexNoStem[word][doc])))

def save_n_gram_index(title,n):
    file_Title= "indexes/gram/"+title+"_"+str(n)+".txt"
    f = open(file_Title,"w+")
    for word in index:
        f.write("%s:\n" % word)
        for doc in index[word]:
            f.write("\t%s: %s\n"%(doc,",".join(str(x) for x in index[word][doc])))

    file_Title= "indexes/gram/"+title+"_"+str(n)+"_no_Stem.txt"
    f = open(file_Title,"w+")
    for word in indexNoStem:
        f.write("%s:\n" % word)
        for doc in indexNoStem[word]:
            f.write("\t%s: %s\n"%(doc,",".join(str(x) for x in indexNoStem[word][doc])))

def read_index(f):
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

def read_inverted_index(title,stemming):
    if not stemming :
        title = "indexes/inverted_Index/"+title+"_no_Stem.txt"
    else: 
        title = "indexes/inverted_Index/"+title+".txt"
    f = open(title)
    print(title+":")
    return read_index(f)
        

def read_n_gram_index(title,n,stemming):
    if not stemming :
        title = "indexes/gram/"+title+"_"+str(n)+"_no_Stem.txt"
    else:
        title = "indexes/gram/"+title+"_"+str(n)+".txt"
    f = open(title)
    print(title+":")
    return read_index(f)

def initialize():
    global index,indexNoStem,documents
    index = {}
    indexNoStem = {}
    documents = []

def main():
    build_inverted_index()
    initialize()
    build_n_gram(2)

if __name__ == "__main__" :
    main()

