import sys
import lab2InvertedIndex as indexes
collections =["sample","trec.sample"]

def andOperator(var1,var2,index):
    if (var1 not in index) and (var2 not in index):
        return None
    else:
        return list(set(index[var1].keys()) & set(index[var2].keys()))
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
        return set(documentsWith) ^ set(documentsWithout)
    else:
        return None
def findMatch(arguments):
    index = indexes.readIndex(collections[0])
    notOp = False
    andOp = False
    orOp = False
    for x in arguments:
        if x=="not":
            notOp = True
        elif  x == "and":
            andOp = True
        elif x == "or":
            orOp = True
        else:
            if notOp:
                result = notOperator(x,index)
                notOp = False
            elif andOp:
                print(andOperator(var,x,index))
            else:
                var = x


                
def main(arguments):
    if arguments[1] == "find":
        findMatch(arguments[2:])
    
if __name__ == "__main__" :
    main(sys.argv)