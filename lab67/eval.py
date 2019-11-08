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

def statsAt(results,true,cutoff,ap=False) :
    stats = {}
    for file,result in results.items():
        precisions,recalls = [],[]
        print(file)
        stats[file]={'pres':{},'recall':{}}
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
            recall = tp/len(documents)
            
            stats[file]['pres'][q_id] = round(pres,2)
            precisions.append(pres)

            stats[file]['recall'][q_id]=round(recall,2)
            recalls.append(recall)
        stats[file]['pres']['avg']=(round(sum(precisions)/len(precisions),2))
        stats[file]['recall']['avg']=(round(sum(recalls)/len(recalls),2))
    return stats

def rPrecision(results,true,stats):
    for file,result in results.items():
        precisions = []
        stats[file]['rPres']={}
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
            stats[file]['rPres'][q_id]=round(pres,2)
            precisions.append(pres)
        stats[file]['rPres']['avg']=round(sum(precisions)/len(precisions),2)
    return stats

def AP(results,true,stats):
    for file,result in results.items():
        ap = []
        stats[file]['ap']={}
        for q_id,docs in result.items():
            documents = []
            for rel,t_docs in true[str(q_id)].items():
                documents.extend(t_docs)
            r = len(documents)
            i = 0
            for rank,doc in docs.items():
                print(rank,doc)
                # if str(doc[0]) in documents:
                    # do blah
            i+=1  
        return stats

def main():
    results = {}
    for file in files:
        resutls = read_file(file,results)
    true = read_true_results()
    statistics = statsAt(results,true,10)
    statistics = rPrecision(results,true,statistics)
    print(statistics)
    # statistics = AP(results,true,statistics)
if __name__ == "__main__" :
    main()