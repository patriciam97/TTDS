import re
from stemming.porter2 import stem
import matplotlib.pyplot as plt
from collections import OrderedDict

stop = []
index = {}
documents = []
collections =["sample","trec.sample"]

def read_stop_words():
    f = open ("stopWords.txt")
    for x in f:
        stop.append(x.strip())

def read_samples():
    global collections
    for collection in collections:
        f = open("collections/"+collection+".txt")
        for x in f:
            if "ID:" in x:
                doc_id = x.split(":")[1].strip()
            else:
                text = x.split(":")[1]
                process_text(doc_id,text)
        save_inverted_index(collection)
        global index

def build_inverted_index ():
    read_samples()
    
def generate_index(doc_id,words): 
    # words are processed - tokenize, stopping and stemming
    for i,word in enumerate(words,1):
        if word not in index:
            # first push
            index[word] = {doc_id:[i]}
        else:
            # more push
            documents = index[word].keys()
            if doc_id not in documents:
                index[word][doc_id]=[i]
            else: index[word][doc_id].append(i)

def sub_array(arr,start,n): 
    # from start get n next elements
    result = []
    for i in list(range(start,start+n)):
        result.append(arr[i])
    return result

def process_text_for_n_gram(doc_id,text,n):
    text = text.split()
    arr = []
    processedPhrases = []
    for i,word in enumerate(text,0):
        if i<(len(text)-n+1):
            arr.append(sub_array(text,i,n))
    for pair in arr:
        phrase = "_".join(pair)
        processedPhrases.append(phrase)
    generate_index(doc_id,processedPhrases)
    return processedPhrases
    
def build_n_gram(n):
    # words are unprocessed
    global collections
    for collection in collections:
        f = open("collections/"+collection+".txt")
        for x in f:
            if "ID:" in x:
                doc_id = x.split(":")[1].strip()
            else:
                text = x.split(":")[1]
                process_text_for_n_gram(doc_id,text,n)
        save_n_gram_index(collection,n)

def process_text(doc_id,text):
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
    generate_index(doc_id,processedWords)

def save_inverted_index(title):
    title= "indexes/"+title+"_Inverted_Index.txt"
    f = open(title,"w+")
    for word in index:
        f.write("%s:\n" % word)
        for doc in index[word]:
            f.write("\t%s: %s\n"%(doc,",".join(str(x) for x in index[word][doc])))

def save_n_gram_index(title,n):
    title= "indexes/"+title+"_"+str(n)+"_Gram.txt"
    f = open(title,"w+")
    for word in index:
        f.write("%s:\n" % word)
        for doc in index[word]:
            f.write("\t%s: %s\n"%(doc,",".join(str(x) for x in index[word][doc])))

def read_index(f):
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

def read_inverted_index(title):
    title = "indexes/"+title+"_Inverted_Index.txt"
    f = open(title)
    print(title+":")
    return read_index(f)
        

def read_n_gram_index(title,n):
    title = "indexes/"+title+"_"+str(n)+"_Gram.txt"
    f = open(title)
    print(title+":")
    return read_index(f)

def main():
    build_inverted_index()
    build_n_gram(2)

if __name__ == "__main__" :
    main()

