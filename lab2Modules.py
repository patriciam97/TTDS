import sys
import lab2InvertedIndex as indexes
collections =["sample","trec.sample"]

def andOperator(var1,var2,index):
    if (type(var1)!=list) & (type(var1)!=set) & (type(var2)!=list) & (type(var2)!=set):
        if (var1 not in index) and (var2 not in index):
            return None
        else:
            return list(set(index[var1].keys()) & set(index[var2].keys()))
    elif ((type(var1) == list) |(type(var1) == set)) & (type(var2) ==  str):
        if (var2 not in index):
            return None
        else:
            return list(set(var1) & set(index[var2].keys()))
    elif ((type(var2) == list) |(type(var2) == set)) & (type(var1) ==  str):
        if (var1 not in index):
            return None
        else:
            return list(set(var2) & set(index[var1].keys()))
    else:
        return list(set(var1) & set(var2))
def orOperator(var1,var2,index):
    if (type(var1)!=list) & (type(var1)!=set) & (type(var2)!=list) & (type(var2)!=set):
        if (var1 not in index) and (var2 not in index):
            return None
        else:
            return list(set(index[var1].keys()) | set(index[var2].keys()))
    elif ((type(var1) == list) |(type(var1) == set)) & (type(var2) ==  str):
        if (var2 not in index):
            return None
        else:
            return list(set(var1) | set(index[var2].keys()))
    elif ((type(var2) == list) |(type(var2) == set)) & (type(var1) ==  str):
        if (var1 not in index):
            return None
        else:
            return list(set(var2) | set(index[var1].keys()))
    else:
        return list(set(var1) | set(var2))
def notOperator(var,index):
    if (var in index):
        documentsWithout = []
        documentsWith = []
        matches = { key:value for (key,value) in index.items() if key != var}
        for w in matches:
            for doc in index[w]:
                if doc not in documentsWithout:
                    documentsWithout.append(doc)
        for doc in index[var]:
            documentsWith.append(doc)
        return list(set(documentsWith) ^ set(documentsWithout))
    else:
        return None

def findPhrase(phrase,index):
    documents = {}
    documents = set(index[phrase[0]].keys())
    diff = 0
    results =[]
    for word in phrase[1:]:
        documents = set(documents & set(index[word].keys()))
    for doc in documents:
        for word in phrase:
            for pos in index[word][doc]:
                # print(pos)
                diff = abs(diff-int(pos))
            if (diff == len(phrase)-1):
                results.append(doc)
    return results
def findMatches(arguments):
    results = []
    variables = []
    phrase = []
    index = indexes.readIndex(collections[0])
    notOp = False
    andOp = False
    orOp = False
    isPhrase = True
    if (len(arguments)==1):
        results.append(list(index[arguments[0]].keys()))
    else:
        for keyword in arguments:
            if (keyword == "NOT"):
                notOp = True
                isPhrase = False
            elif (keyword == "AND"):
                andOp = True
                isPhrase = False
            elif (keyword == "OR"):
                orOp = True
                isPhrase = False
            else:
                variables.append(keyword)
                if (isPhrase):
                    phrase.append(keyword)
                if (notOp):
                    var = variables.pop()
                    results.append(notOperator(var,index))
                    notOp = False
                elif (andOp):
                    if ( len(variables) == 0):
                        results.append(andOperator(results.pop(),results.pop(),index))
                    elif ( len(variables) == 1):
                        results.append(andOperator(results.pop(),variables.pop(),index))
                    else: 
                        results.append(andOperator(variables.pop(),variables.pop(),index))
                    andOp = False
                elif (orOp):
                    if ( len(variables) == 0):
                        results.append(orOperator(results.pop(),results.pop(),index))
                    elif ( len(variables) == 1):
                        results.append(orOperator(results.pop(),variables.pop(),index))
                    else: 
                        results.append(orOperator(variables.pop(),variables.pop(),index))
                    orOp = False
        if (andOp):
            results.append(andOperator(results.pop(),results.pop(),index))
        elif (orOp):
            results.append(orOperator(results.pop(),results.pop(),index))
        elif (isPhrase):
            results.append(findPhrase(phrase,index))
    return results

def main(arguments):
    if arguments[1] == "FIND":
        for x in findMatches(arguments[2:]):
            print (x)
    
if __name__ == "__main__" :
    main(sys.argv)