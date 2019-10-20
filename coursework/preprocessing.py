import re
from stemming.porter2 import stem
from collections import OrderedDict
import itertools
import xml.etree.ElementTree as ET

stop = []
index = {}
documents = []
collections =["sample","trec.sample","trec.5000"]
current_collection = collections[2]

def read_stop_words():
    # collect stop words
    global stop
    f = open ("stopWords.txt")
    stop = {}
    for x in f.readlines():
        #save stop words in a global list
        stop[x.strip()] = 1
    f.close()

def filter_out_stop_words(words, stop_words):
    return list(filter(lambda word: word not in stop_words and word != "", words))
    
def read_samples(ngram):
    # reads xml file and sends doc_id, content(heading and text) to the process_text function
    global current_collection,index,documents,stop
    #reads collection xml
    f = open("../collections/"+current_collection+".xml")
    it = itertools.chain('<root>', f, '</root>')
    root = ET.fromstringlist(it)
    for doc in list(root):
        doc_id, headline, text = doc.find('DOCNO').text, doc.find('HEADLINE'), doc.find('TEXT')
        # filter out stop words from content after tokenization
        content = ""
        if headline!= None:
            content = content+" "+headline.text
        if text!= None:
            content = content+" "+text.text
        content = content.lower()
        content = filter_out_stop_words([word for word in content.split()],stop)
        if not ngram:
            #process text for boolean,proximity and phrase search
            process_text(doc_id,content)
        else:
            #process text for n grams where ngram is an int indicating n
            process_text_for_n_gram(doc_id,content,ngram)

def build_inverted_index():
    read_samples(False)
    
def generate_index(doc_id,words): 
    # words are processed - tokenize and stemming
    for i,word in enumerate(words,0):
        if word not in index:
            # first push
            index[word] = {doc_id:[i]}
        else:
            # not first push
            documents = index[word].keys()
            if doc_id not in documents:
                index[word][doc_id]=[i]
            else: index[word][doc_id].append(i)

def sub_array(arr,start,n): 
    # from start get n next elements
    result = []
    for i in list(range(start,start+n)):
        result.append(arr[i].lower())
    return result

def process_text_for_n_gram(doc_id,text,n):
    # gets n pairs appends them with underscore a
    arr = []
    processedPhrases = []
    regex = re.compile('[^a-zA-Z]')
    for i,word in enumerate(text,0):
        if i<(len(text)-n+1):
            arr.append(sub_array(text,i,n))
    for pair in arr:
        pair = [regex.sub('',x.lower()).strip() for x in pair]
        phrase = "_".join(pair)
        pair = [ stem(x) if len(x)>3 else x for x in pair]
        phrase = "_".join(pair)
        processedPhrases.append(phrase)
    generate_index(doc_id,processedPhrases)

def build_n_gram(n): 
    read_samples(n)

def process_text(doc_id,text):
    processedWords= []
    #regex to find everything that is non-alphabetic
    regex = re.compile('[^a-zA-Z]')
    for word in text:
        token = regex.sub('',word)
        if token not in stop:
            if stem(token.strip()) != "":
                processedWords.append(stem(token.strip()))
    generate_index(doc_id,processedWords)

def save_index():
    file_Title= "index.txt"
    f = open(file_Title,"w+")
    for word in index:
        f.write("%s:\n" % word)
        for doc in index[word]:
            f.write("\t%s: %s\n"%(doc,",".join(str(x) for x in index[word][doc])))
        f.write("\n")
    
def read_index():
    #reads index.txt back into memory
    title = "index.txt"
    f = open(title)
    index = {}
    documents = {}
    for line in f.readlines():
        if line=="\n": continue
        line = line.strip().split(":")
        if(line[1]==""):
            word = line[0]
            index[word]={}
        else:
            document = line[0]
            positions = line[1].split(",")
            if document not in documents:
                documents[document] = 1
            for x in positions:
                pos = x.strip()
                if (document not in index[word]):
                    index[word][document]=[pos]
                else:
                    index[word][document].append(pos)
    return index,list(documents.keys())

def initialize():
    global index,documents
    index = {}
    documents = []

def main():
    read_stop_words()
    build_inverted_index()
    build_n_gram(2)
    save_index()

if __name__ == "__main__" :
    main()

