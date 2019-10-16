import sys
import lab2Indexes as indexes
from stemming.porter2 import stem

collections =["sample","trec.sample"]
operators = []
sets = []
stemming = True
currentCollection=""
def and_operator(var1,var2,index):
    if (len(var1.split(" ")) >1):
        var1 = findPhraseInIndex(var1)
    if (len(var2.split(" ")) >1):
        var2 = findPhraseInIndex(var2)
    if (type(var1)!=list) & (type(var2)!=list):
        if (var1 not in index) or (var2 not in index):
            return []
        else:
            return list(set(index[var1].keys()) & set(index[var2].keys()))
    elif (type(var1) == list) & (type(var2) ==  str):
        if (var2 not in index):
            return []
        else:
            return list(set(var1) & set(index[var2].keys()))
    elif (type(var2) == list) & (type(var1) ==  str):
        if (var1 not in index):
            return []
        else:
            return list(set(var2) & set(index[var1].keys()))
    else:
        return list(set(var1) & set(var2))

def or_operator(var1,var2,index):
    if (len(var1.split(" ")) >1):
        var1 = findPhraseInIndex(var1)
    if (len(var2.split(" ")) >1):
        var2 = findPhraseInIndex(var2)
    if (type(var1)!=list) & (type(var2)!=list):
        if (var1 not in index) and (var2 not in index):
            return []
        elif (var1 in index) and (var2 not in index):
            return list(set(index[var1].keys()))
        elif (var1 not in index) and (var2 in index):
            return list(set(index[var2].keys()))
        else:
            return list(set(index[var1].keys()) | set(index[var2].keys()))
    elif (type(var1) == list) & (type(var2) ==  str):
        if (var2 not in index):
            return []
        else:
            return list(set(var1) | set(index[var2].keys()))
    elif (type(var2) == list) & (type(var1) ==  str):
        if (var1 not in index):
            return []
        else:
            print(index[var1].keys())
            return list(set(var2) | set(index[var1].keys()))
    else:
        return list(set(var1) | set(var2))
        
def not_operator(var,index,documents):
    if (len(var.split(" "))>1):
        var = findPhraseInIndex(var)

    if (type(var)==list):
        print(list(set(documents) ^ set(var)))
        return list(set(documents) ^ set(var))
    else:
        if (var in index):
            return list(set(documents) ^ set(index[var].keys()))
        else:
            return None

def findPhraseInIndex(phrase):
    global stemming,currentCollection
    phrase = phrase.split(" ")
    if (len(phrase)==2):
        if stemming:
            phrase = "_".join([stem(x) for x in phrase])
        else:
            phrase = "_".join(phrase)
        index,documents = indexes.read_n_gram_index(currentCollection,2,stemming)
        if phrase in index:
            return (list(index[phrase].keys()))
        else:
            return ([])

def find_phrase (sets):
    global stemming
    if stemming:
        phrase = "_".join([stem(x) for x in sets])
    else:
        phrase = "_".join(sets)

    if (len(sets)==2):
        for collection in collections:
            index,documents = indexes.read_n_gram_index(collection,2,stemming)
            if phrase in index:
                print(list(index[phrase].keys()))
                return (list(index[phrase].keys()))
            else:
                print("No search results")
    else:
        indexes.build_n_gram(len(sets))
        for collection in collections:
            index,documents = indexes.read_n_gram_index(collection,len(sets),stemming)
            if phrase in index:
                print(list(index[phrase].keys()))
                return(list(index[phrase].keys()))
            else:
                print("No search results")

def set_up_sets_and_operators(arguments):
    global sets,operands
    sets = []
    operands = []
    oper_types = ["AND","OR","NOT","OR NOT","AND NOT"]
    previous = False
    phrase = False
    isPhrase = False
    phraseInQuotes = ""
    for x in arguments:
        if x in oper_types:
            if (x == "AND"):
                previous = "AND"
            elif (x == "OR"):
                previous = "OR"
            elif (previous != False):
                if (x == "NOT" and previous == "AND"):
                    operators.append("AND NOT")
                    previous = False
                elif (x == "NOT" and previous == "OR"):
                    operators.append("OR NOT")
                    previous = False
            else:
                if previous == "AND":
                    previous = False
                    operators.append("AND")
                    operators.append(x)
                elif previous == "OR":
                    previous = False                    
                    operators.append("OR")
                    operators.append(x)
                else:
                    operators.append(x)
                if previous == "\"" and x =="\"":
                    operators.append(phrase)
                    phrase = False
                elif previous != False and x!="\"":
                    if phrase == True:
                        phrase = x
                    else:
                        phrase = phrase + x
                elif previous == False and x == "\"":
                    phrase = True

        else: 
            if (("\"" not in x) and isPhrase == True):
                phraseInQuotes = phraseInQuotes+" "+x
            elif (x[0] == "\"" and x[-1]!= "\"" and isPhrase == False):
                isPhrase = True
                phraseInQuotes = phraseInQuotes+x[1:]
            elif(x[-1]== "\"" and isPhrase == True):
                phraseInQuotes = phraseInQuotes+" "+x[:-1]
                sets.append(phraseInQuotes.lower())
                isPhrase = False
                phraseInQuotes = ""
            elif(x[0]== "\"" and x[-1]== "\""):
                sets.append(x.lower()[1:-1])
            else: 
                sets.append(x.lower())
            if previous != False:
                if previous == "AND":
                        previous = False
                        operators.append("AND")
                elif previous == "OR":
                        previous = False                    
                        operators.append("OR")
                elif previous == "NOT":
                        previous = False                    
                        operators.append("NOT")

def proximitySearch(dist,var1,var2):
    global collections
    results = []
    if (stemming):
        var1 = stem(var1)
        var2 = stem(var2)
    for collection in collections:
        index,documents = indexes.read_inverted_index(collection,stemming)
        if (var1 in index) and (var2 in index):
            var1_docs = set(index[var1].keys())
            var2_docs = set(index[var2].keys())
            common_docs =  var1_docs.intersection(var2_docs)
            for doc in common_docs:
                var1_docs_iterator = 0
                var2_docs_iterator = 0
                while var1_docs_iterator < len(index[var1][doc]) and var2_docs_iterator < len(index[var2][doc]):
                        val1_pos = int(index[var1][doc][var1_docs_iterator])
                        val2_pos = int(index[var2][doc][var2_docs_iterator])
                        if abs(val1_pos - val2_pos) <= int(dist):
                            results.append(doc)
                            break
                        if val2_pos > val1_pos:
                            var2_docs_iterator += 1
                        elif val2_pos < val1_pos:
                            var1_docs_iterator += 1
                        else:
                            var1_docs_iterator += 1
                            var2_docs_iterator += 1
        print(results)
def find_matches(arguments):
    global sets,operators,stemming,currentCollection
    sets = []
    operators = []

    if (arguments[0].startswith("#",0)):
        dist=arguments[0][1:].split("(")[0]
        var1=arguments[0].split("(")[1].split(",")[0].strip()
        var2=arguments[0].split(",")[1].split(")")[0].strip()
        proximitySearch(dist,var1,var2)
    else:
        set_up_sets_and_operators(arguments)
        print("sets:"+str(sets)+"opers:"+str(operators))
        if (len(operators) == 0 and len(sets)==1):
            # just one word
            if (len(sets[0].split(" "))>0):
                return find_phrase(sets[0].split(" ")) 
            else:
                for collection in collections:
                    index,documents = indexes.read_inverted_index(collection,stemming)
                    if stemming:
                        word = stem(sets[0])
                    else:
                        word = sets[0]
                    if (word) in index:
                        print (list(index[word].keys()))
                    else: 
                        print("No search results")
        else:
            # logical expression
            for collection in collections:
                currentCollection = collection
                sets_copy=sets.copy()
                operators_copy = operators.copy()
                index,documents = indexes.read_inverted_index(collection,stemming)
                if stemming:
                    for i,x in enumerate(sets_copy):
                        sets_copy[i] = stem(x)
                while (len(operators_copy)!=0):
                    print("sets:"+str(sets_copy)+"opers:"+str(operators_copy))
                    oper = operators_copy.pop(0)
                    if (oper == "NOT"):
                        var = sets_copy.pop(0)
                        docs = not_operator(var,index,documents)
                        if docs != None:
                            sets_copy.append(list(docs))
                    elif (oper == "AND NOT"):
                        sets_copy.insert(0,and_operator(sets_copy.pop(0),not_operator(sets_copy.pop(0),index,documents),index))
                    elif (oper == "OR NOT"):
                        sets_copy.insert(0,or_operator(sets_copy.pop(0),not_operator(sets_copy.pop(0),index,documents),index))
                    elif (oper == "AND"):
                        sets_copy.insert(0,and_operator(sets_copy.pop(0),sets_copy.pop(0),index))
                    elif (oper == "OR"):
                        sets_copy.insert(0,or_operator(sets_copy.pop(0),sets_copy.pop(0),index))
                if (sets_copy == [[]]):
                    print("No search results")
                else:
                    print(sets_copy[0])

def main(arguments):
    global stemming
    stemming = input("Want to use Porter Stemming?")
    if stemming.lower() == "no":
        stemming = False
        print("Stemming set to False.")
    else:
        stemming = True
        print("Stemming set to True.")
    while True:
        query= input("Search for: ")
        find_matches(query.split())
        print ( "-------------------------")
    
if __name__ == "__main__" :
    main(sys.argv)