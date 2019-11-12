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
        filename='S'+str(file)
        stats[filename]={}
        precisions,recalls = [],[]
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
            if q_id not in stats[filename]: stats[filename][q_id]={}
            stats[filename][q_id]['pres'] = round(pres,3)
            precisions.append(pres)

            stats[filename][q_id]['recall'] =round(recall,3)
            recalls.append(recall)
        if 'avg' not in stats[filename]: stats[filename]['avg']={}
        stats[filename]['avg']['pres'] =(round(sum(precisions)/len(precisions),3))
        stats[filename]['avg']['recall'] =(round(sum(recalls)/len(recalls),3))
    return stats

def rPrecision(results,true,stats):
    for file,result in results.items():
        filename='S'+str(file)
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
            stats[filename][q_id]['rPres']=round(pres,3)
            precisions.append(pres)
        stats[filename]['avg']['rPres'] =round(sum(precisions)/len(precisions),3)
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
        filename='S'+str(file)
        ap = []
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
            stats[filename][q_id]['ap']=round(ap_val,3)
        stats[filename]['avg']['map']=round(sum(ap)/len(ap),3)
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
        filename='S'+str(file)
        nDcg = []
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
            stats[filename][q_id]['dgc_'+str(k)] = round(nDcg_val/nDcG_ideal[q_id],3)
        stats[filename]['avg']['dgc_'+str(k)]= round(sum(nDcg)/len(nDcg),3)
    return stats
    
def output_stats(stats):
    a=open("All.eval","w+")
    a.write("\tP@10\tR@50\tr-Precision\tAP\tnDCG@10\tnDCG@20\n")

    for file,results  in stats.items():
        file_name = "{0}.results".format(file)
        f= open(file_name,"w+")
        f.write("\tP@10\tR@50\tr-Precision\tAP\tnDCG@10\tnDCG@20\n")
        for q_id,results in results.items():
            pres = results['pres']
            recall = results['recall']
            rPres = results['rPres']
            if q_id != "avg":
                ap = results['ap']
            else:
                ap = results['map']
            dgc_10 = results['dgc_10']
            dgc_20 = results['dgc_20']
            if q_id != "avg":
                f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(q_id,pres,recall,rPres,dgc_10,dgc_20))
            else:
                f.write("mean\t{0}\t{1}\t{2}\t{3}\t{4}".format(pres,recall,rPres,dgc_10,dgc_20))
                a.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(file,pres,recall,rPres,dgc_10,dgc_20))
        print("{0}.results Saved".format(file))
        f.close()
    print("All.results Saved")
    a.close()
        
        


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