import sys
import lab2InvertedIndex as indexes
from stemming.porter2 import stem

collections =["sample","trec.sample"]
operators = []
sets = []

def and_operator(var1,var2,index):
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
    elif (type(var2) == set) & (type(var1) ==  str):
        if (var1 not in index):
            return []
        else:
            return list(set(var2) & set(index[var1].keys()))
    else:
        return list(set(var1) & set(var2))

def or_operator(var1,var2,index):
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
    elif (type(var2) == set) & (type(var1) ==  str):
        if (var1 not in index):
            return []
        else:
            return list(set(var2) | set(index[var1].keys()))
    else:
        return list(set(var1) | set(var2))
        
def not_operator(var,index,documents):
    if (var in index):
        return list(set(documents) ^ set(index[var].keys()))
    else:
        return None

def find_phrase (sets):
    phrase = "_".join(sets)
    if (len(sets)==2):
        for collection in collections:
            index,documents = indexes.read_n_gram_index(collection,2)
            print(collection+":"+index[phrase].keys())
        else:
            indexes.build_n_gram(len(sets))
            for collection in collections:
                index,documents = indexes.read_n_gram_index(collection,len(sets))
                print(collection+":"+index[phrase].keys())

def set_up_sets_and_operators(arguments):
    oper_types = ["AND","OR","NOT","OR NOT","AND NOT"]
    previous = False
    for x in arguments:
        x = stem(x)
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

def find_matches(arguments):
    global sets,operators
    set_up_sets_and_operators(arguments)
    print("sets:",sets,"opers:",operators)

    if (len(operators) == 0 and len(sets)>1): 
        # phrase
        return find_phrase(sets)
    elif (len(operators) == 0 and len(sets)==1):
        # just one word
        for collection in collections:
            index,documents = indexes.read_inverted_index(collection)
            if (sets[0] in index):
                print (index[sets[0]].keys())
            else: 
                print([])
    else:
        # logical expression
        for collection in collections:
            sets_copy=sets.copy()
            operators_copy = operators.copy()
            index,documents = indexes.read_inverted_index(collection)
            while (len(operators_copy)!=0):
                oper = operators_copy.pop(0)
                if (oper == "NOT"):
                    var = sets.pop(0)
                    docs = not_operator(var,index,documents)
                    sets_copy.append(list(docs))
                elif (oper == "AND NOT"):
                    sets_copy.insert(0,and_operator(sets_copy.pop(0),not_operator(sets_copy.pop(0),index,documents),index))
                elif (oper == "OR NOT"):
                    sets_copy.insert(0,or_operator(sets_copy.pop(0),not_operator(sets_copy.pop(0),index,documents),index))
                elif (oper == "AND"):
                    sets_copy.insert(0,and_operator(sets_copy.pop(0),sets_copy.pop(0),index))
                elif (oper == "OR"):
                    sets_copy.insert(0,or_operator(sets_copy.pop(0),sets_copy.pop(0),index))
            print(sets_copy)


def main(arguments):
    while True:
        global operators,sets
        operators = []
        sets = []
        query= input("Search for: ")
        find_matches(query.split())
        # for x in find_matches(query.split()):
        #     print (x)
    
if __name__ == "__main__" :
    main(sys.argv)