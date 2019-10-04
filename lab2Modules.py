import sys
import lab2InvertedIndex as indexes
collections =["sample","trec.sample"]

def andOperator(var1,var2,index):
    if (type(var1)!=list) & (type(var2)!=list):
        if (var1 not in index) and (var2 not in index):
            return None
        else:
            return list(set(index[var1].keys()) & set(index[var2].keys()))
    elif (type(var1) == list) & (type(var2) ==  str):
        print("here")
        print(list(set(var1) & set(index[var2].keys())))
        if (var2 not in index):
            return None
        else:
            return list(set(var1) & set(index[var2].keys()))
    elif (type(var2) == set) & (type(var1) ==  str):
        if (var1 not in index):
            return None
        else:
            return list(set(var2) & set(index[var1].keys()))
    else:
        return list(set(var1) & set(var2))
def orOperator(var1,var2,index):
    if (type(var1)!=list) & (type(var2)!=list):
        if (var1 not in index) and (var2 not in index):
            return None
        else:
            return list(set(index[var1].keys()) | set(index[var2].keys()))
    elif (type(var1) == list) & (type(var2) ==  str):
        if (var2 not in index):
            return None
        else:
            return list(set(var1) | set(index[var2].keys()))
    elif (type(var2) == set) & (type(var1) ==  str):
        if (var1 not in index):
            return None
        else:
            return list(set(var2) | set(index[var1].keys()))
    else:
        return list(set(var1) | set(var2))
        
def notOperator(var,index,documents):
    if (var in index):
        return list(set(documents) ^ set(index[var].keys()))
    else:
        return None

def findMatches(arguments):
    index,documents = indexes.readIndex("sample")
    oper_types = ["AND","OR","NOT","OR NOT","AND NOT"]
    operators = []
    sets = []
    previous = False
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
                elif previous == "OR":
                    previous = False                    
                    operators.append("OR")
                operators.append(x)
        else: 
            sets.append(x)
            if previous != False:
                if previous == "AND":
                        previous = False
                        operators.append("AND")
                elif previous == "OR":
                        previous = False                    
                        operators.append("OR")
    while (len(operators)!=0):
        print("sets:",sets,"opers:",operators)
        oper = operators.pop(0)
        print("operatorrrr:",oper)
        if (oper == "NOT"):
            var = sets.pop(0)
            docs = notOperator(var,index,documents)
            # sets.insert(0,[docs])
            sets.append(list(docs))
        elif (oper == "AND NOT"):
            sets.insert(0,andOperator(sets.pop(0),notOperator(sets.pop(0),index,documents),index))
        elif (oper == "OR NOT"):
            sets.insert(0,orOperator(sets.pop(0),notOperator(sets.pop(0),index,documents),index))
        elif (oper == "AND"):
            sets.insert(0,andOperator(sets.pop(0),sets.pop(0),index))
        elif (oper == "OR"):
            sets.insert(0,orOperator(sets.pop(0),sets.pop(0),index))
    return (sets)


def main(arguments):
    if arguments[1] == "FIND":
        for x in findMatches(arguments[2:]):
            print (x)
    
if __name__ == "__main__" :
    main(sys.argv)