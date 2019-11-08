import math
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

def statsAt(results,true,cutoff) :
    stats = {}
    for file,result in results.items():
        precisions,recalls = [],[]
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

def precisionAtK(documents,true,k):
    tp,fp = 0,0
    for rank,doc in documents.items():
        if str(doc[0]) in true[:k]:
            tp+=1
        else:
            fp+=1
    return tp/(tp+fp)

def AP(results,true,stats):
    for file,result in results.items():
        ap = []
        stats[file]['ap']={}
        true_documents = []
        for q_id,docs in result.items():
            ap_val = 0
            for rel,t_docs in true[str(q_id)].items():
                true_documents.extend(t_docs)
            for rank,doc in docs.items():
                if str(doc[0]) in true_documents[:rank]:
                    ap_val += precisionAtK(docs,true_documents,rank)
            ap_val/=len(t_docs)
            ap.append(ap_val)
            stats[file]['ap'][q_id]=round(ap_val,2)
        stats[file]['map']=round(sum(ap)/len(ap),2)
    return stats

def nDCGAtK(results,true,k,stats):
    nDcG_ideal= {}
    for q_id in true:
        ideal = 0
        for rel,t_docs in sorted(true[str(q_id)].items()):
            if float(rel) == 1:
                ideal += float(rel)
            elif float(rel) <= k:
                ideal +=float(rel)/math.log(float(rel),2)
            else: continue
        nDcG_ideal[float(q_id)] = ideal

    for file,result in results.items():
        nDcg = []
        stats[file]['dgc_'+str(k)]={}
        true_documents = []
        for q_id,docs in result.items():
            nDcg_val = 0
            for rank,doc in sorted(docs.items()):
                if rank == 1:
                    nDcg_val=float(doc[1])
                elif rank <= k:
                    nDcg_val+=(float(doc[1])/math.log(int(rank),2))
                else: continue
            nDcg.append(nDcg_val/nDcG_ideal[q_id])
            stats[file]['dgc_'+str(k)][q_id] = round(nDcg_val/nDcG_ideal[q_id],2)
        stats[file]['dgc_'+str(k)]['avg'] = round(sum(nDcg)/len(nDcg),2)
    return stats
    
def output_stats(stats):
    for file,results  in stats.items():
        file_name = "S{0}.results".format(file)
        f= open(file_name,"w+")
        f.write("\tP@10\tR@50\tr-Precision\tAP\tnDCG@10\tnDCG@20\n")
        queries = [[] for i in range(11)]
        for q_id, value in results['pres'].items():
            if q_id == 'avg':
                queries[-1].append(value)
            else:
                queries[int(q_id)-1].append(value)

        for q_id, value in results['recall'].items():
            if q_id == 'avg':
                queries[-1].append(value)
            else:
                queries[int(q_id)-1].append(value)

        for q_id, value in results['rPres'].items():
            if q_id == 'avg':
                queries[-1].append(value)
            else:
                queries[int(q_id)-1].append(value)

        for q_id, value in results['ap'].items():
            if q_id == 'map':
                queries[-1].append(value)
            else:
                queries[int(q_id)-1].append(value)

        for q_id, value in results['dgc_10'].items():
            if q_id == 'avg':
                queries[-1].append(value)
            else:
                queries[int(q_id)-1].append(value)

        for q_id, value in results['dgc_20'].items():
            if q_id == 'avg':
                queries[-1].append(value)
            else:
                queries[int(q_id)-1].append(value)

        for i,query in enumerate(queries):
            f.write(str(i))
            for value in query:
                f.write("\t{0}".format(str(value)))
            f.write("\n")
        f.close()


def main():
    results = {}
    for file in files:
        resutls = read_file(file,results)
    true = read_true_results()
    statistics = statsAt(results,true,10)
    statistics = rPrecision(results,true,statistics)
    statistics = AP(results,true,statistics)
    statistics = nDCGAtK(results,true,10,statistics)
    statistics = nDCGAtK(results,true,20,statistics)
    output_stats(statistics)

if __name__ == "__main__" :
    main()