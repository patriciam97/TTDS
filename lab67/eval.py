files = ["./systems/S1.results","./systems/S2.results","./systems/S3.results","./systems/S4.results","./systems/S5.results","./systems/S6.results"]

def read_file(title,results):
    with open(title, encoding="utf8", errors='ignore') as f:
        results[title[10:12]] = {}
        for line in f.readlines():
            line = line.split(" ")
            q_id = int(line[0])
            doc_id = int(line[2])
            rank_of_doc = line[3]
            score = line[4]
            results[title[10:12]][rank_of_doc] = [doc_id,score] 
    return results

def read_true_results():
    true = {}
    with open("./systems/qrels.txt", encoding="utf8", errors='ignore') as f:
        for line in f.readlines():
            line = line.split(" ")
            q_id = line[0][:-1]
            if q_id not in true:
                true[q_id]= {}
            for _tuple in line[1:]:
                _tuple = _tuple.strip().split(",")
                if len(_tuple) == 2:
                    doc = _tuple[0][1:]
                    rel = _tuple[1][:-1]
                    if rel in true[q_id]:
                        true[q_id][rel].append(doc)
                    else: true[q_id][rel] = [doc]
    return true

def precisionAt(results,true,cutoff) :
    found,other = 0,0
    for key,value in results.items():
        print(key)
        for q_id,docs in value.items():
            top_docs = docs[:(cutoff+2)]
            print(top_docs)
            true_results_for_query = true[str(q_id)]
            print(true_results_for_query)
            for doc in top_docs:
                doc = doc[0]
                if doc in true_results_for_query:
                    found+=1
                else:
                    other+=1
            print(found,other)
            
def main():
    results = {}
    for file in files:
        resutls = read_file(file,results)
    true = read_true_results()
    print(results)
    # print(true)
    # precisionAt(results,true,10)
if __name__ == "__main__" :
    main()