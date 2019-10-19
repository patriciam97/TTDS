import sys
import lab2Indexes as indexes
from stemming.porter2 import stem
from math import log
import collections
import operator

collections =["sample","trec.sample"]
stemming = False

def tf(t,d,index,documents): 
    global stemming
    # term frequency
    if t in index and str(d) in documents and str(d) in index[t]:
        return(len(index[t][str(d)]))
    else: 
        return 0

def df(t,index):
    # num of docs term d appeared in
    global stemming
    return len(index[t]) if t in index else 0


def weight(t,d,index,documents):
    try:
        return (1+log(tf(t,d,index,documents),10))*log(len(documents)/df(t,index),10)
    except:
        return 0
    
def get_top_documents(phrase):
    global stemming
    index,documents = indexes.read_n_gram_index(collections[1],1,stemming)
    words = list(map(lambda word: stem(word.strip().lower()), phrase))
    docs = [index[word].keys() for word in words if word in index]
    scores = []        
    if len(docs) > 0:
        common_docs = set().union(*docs)
        # print(common_docs)
        for doc in common_docs:
            # print(doc)
            score = 0
            for term in words:
                score += weight(term,doc,index,documents)
            scores.append((doc,score))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    # print (sorted_scores[:5])
    return (sorted_scores[:10000])

def read_queries():
    title = "queries.txt"
    f = open(title)
    for line in f.readlines():
        parts = line.strip().split(" ")
        query_num = parts[0]
        query = [word.strip() for word in parts[1:]]
        for doc,score in get_top_documents(query)[:1]:
            print(query_num," 0 ",doc," 0 ",score,"0")

def main(arguments):
    global stemming
    stemming = input("Want to use Porter Stemming?")
    if stemming.lower() == "no":
        stemming = False
        print("Stemming set to False.")
    else:
        stemming = True
        print("Stemming set to True.")
    read_queries()
    # while True:
    #     query= input("Search for: ")
    #     get_top_documents(query)
    #     print ( "-------------------------")
    
if __name__ == "__main__" :
    main(sys.argv)