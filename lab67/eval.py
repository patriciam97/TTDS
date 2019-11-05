files = ["./systems/S1.results","./systems/S2.results","./systems/S3.results","./systems/S4.results","./systems/S5.results","./systems/S6.results"]

def read_file(title,results):
    with open(title, encoding="utf8", errors='ignore') as f:
        file = int(title[11:].split(".")[0])
        results[file] = {}
        for line in f.readlines():
            line = line.split(" ")
            q_id = int(line[0])
            doc_id = int(line[2])
            rank_of_doc = int(line[3])
            score = line[4]
            if q_id in results[file]:
                results[file][q_id][rank_of_doc] = [doc_id,score] 
            else:
                results[file][q_id] = {}
                results[file][q_id][rank_of_doc] = [doc_id,score] 
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
    for file,result in results.items():
        precisions = []
        for q_id,docs in result.items():
            tp = 0
            fp = 0
            documents = []
            for rel,t_docs in true[str(q_id)].items():
                documents.extend(t_docs)
            for rank,doc in docs.items():
                if rank <= cutoff:
                    if str(doc[0]) in documents:
                        tp+=1
                    else:
                        fp+=1
            pres = tp/(tp+fp)
            precisions.append(pres)
        print("Precision for file "+str(file)+" is: "+str(round(sum(precisions)/len(precisions),2)))

def recallAt(results,true,cutoff) :
    for file,result in results.items():
        recalls = []
        for q_id,docs in result.items():
            tp = 0
            fp = 0
            documents = []
            for rel,t_docs in true[str(q_id)].items():
                documents.extend(t_docs)
            for rank,doc in docs.items():
                if rank <= cutoff:
                    if str(doc[0]) in documents:
                        tp+=1
                    else:
                        fp+=1
            recall = tp/len(documents)
            recalls.append(recall)
        print("Recall for file "+str(file)+" is: "+str(round(sum(recalls)/len(recalls),2)))

def rPrecision(results,true):
    for file,result in results.items():
        precisions = []
        for q_id,docs in result.items():
            tp = 0
            fp = 0
            documents = []
            for rel,t_docs in true[str(q_id)].items():
                documents.extend(t_docs)
            for rank,doc in docs.items():
                if rank <= len(documents):
                    if str(doc[0]) in documents:
                        tp+=1
                    else:
                        fp+=1
            pres = tp/(tp+fp)
            precisions.append(pres)
        print("RPrecision for file "+str(file)+" is: "+str(round(sum(precisions)/len(precisions),2)))

def AP(results,true):
    for file,result in results.items():
        precisions = []
        for q_id,docs in result.items():
            documents = []
            for rel,t_docs in true[str(q_id)].items():
                documents.extend(t_docs)
            i = 1
            for rank,doc in docs.items():
                if str(doc[0]) in documents:
                    precisions.append(rank/i)
                i+=1
        print("AP for file "+str(file)+" is: "+str(round(sum(precisions)/len(precisions),2)))
def main():
    results = {}
    for file in files:
        resutls = read_file(file,results)
    true = read_true_results()
    precisionAt(results,true,10)
    recallAt(resutls,true,50)
    rPrecision(results,true)
    AP(results,true)
if __name__ == "__main__" :
    main()