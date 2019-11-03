files = ["./systems/S1.results","./systems/S2.results","./systems/S3.results","./systems/S4.results","./systems/S5.results","./systems/S6.results"]
def read_file(title,results):
    with open(title, encoding="utf8", errors='ignore') as f:
        results[title[10:13]] = []
        for line in f.readlines():
            line = line.split(" ")
            q_id = int(line[0])
            doc_id = int(line[2])
            rank_of_doc = line[3]
            score = line[4]
            if q_id not in results[title[10:13]]:
                results[title[10:13]]={q_id: [rank_of_doc,doc_id,score]}
            else:
               results[title[10:13]][q_id].append([rank_of_doc,doc_id,score])    
    return results
    
def main():
    results = {}
    for file in files:
        resutls = read_file(file,results)
    print(results)
if __name__ == "__main__" :
    main()