import sys
import preprocessing as indexes
from stemming.porter2 import stem
from math import log
import collections
import operator

collections =["sample","trec.sample","trec.5000"]
currentCollection = collections[1]  #collection to be used
stemming = True
results = []
index = {}
documents = []

def tf(t,d): 
    global index,documents
    # term frequency
    if t in index and str(d) in documents and str(d) in index[t]:
        return(len(index[t][str(d)]))
    else: 
        return 0

def df(t):
    # num of docs term d appeared in
    global index
    return len(index[t]) if t in index else 0


def weight(t,d,index,documents):
    # term weight for docuement d
    try:
        return (1+log(tf(t,d),10))*log(len(documents)/df(t),10)
    except:
        return 0
    
def get_top_documents(phrase):
    global currentCollection,index,documents
    #list of words in lower case after  stripping and stemming
    words = list(map(lambda word: stem(word.strip().lower()), phrase))
    #documents where these words appeared
    docs = [index[word].keys() for word in words if word in index]
    scores = []        
    if len(docs) > 0:
        common_docs = set().union(*docs)
        #union above gives all the documents where the terms appeared
        for doc in common_docs:
            score = 0
            for term in words:
                score += weight(term,doc,index,documents) 
                #score of phrase for document doc
            scores.append((doc,score)) 
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    #sorts them in descending order and returns the top 1000
    return (sorted_scores[:1000]) 


def output_results():
    #saves the scores in results.ranked.txt in the format given to us
    global results
    file_Title= "results.ranked.txt"
    f = open(file_Title,"w+")
    for q_id,docs in results:
        for doc,score in docs:
            f.write("{0} {1} {2} {3} {4:.4f} {5}\n".format(q_id,0,doc,0,score,0))


def read_queries():
    #reads queries in queries.ranked.txt that were given to us
    global results
    title = "queries.ranked.txt"
    f = open(title)
    for line in f.readlines():
        parts = line.strip().split(" ")
        query_num = parts[0]
        query = [word.strip() for word in parts[1:]]
        results.append([query_num,get_top_documents(query)[:1000]])
    output_results()


def main(arguments):
    global index,documents
    index,documents = indexes.read_index()
    read_queries()

    
if __name__ == "__main__" :
    main(sys.argv)