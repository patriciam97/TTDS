from sklearn.metrics import multilabel_confusion_matrix

def read_test_pred():
    catg_true, catg_pred =[],[]
    with open("feats.test", encoding="utf8", errors='ignore') as f:
        for line in f.readlines():
            true_catg = line.split(" ")[0]
            catg_true.append(true_catg)
    with open("pred.out", encoding="utf8", errors='ignore') as f:
        for line in f.readlines():
            pred_catg = line.split(" ")[0]
            catg_pred.append(pred_catg)
    return catg_true, catg_pred

def calculate_statistics(catg_true,catg_pred):
    acc = 0
    for i,category in enumerate(multilabel_confusion_matrix(catg_true,catg_pred),1):
        tp,fp = category[0]
        tn,fn = category[1]
        acc += (tp+tn)/(tn + fp + fn + tp )
        pres = tp/(tp+fp)
        recall = tp/(tp+fn)
        f1 = (2*pres*recall)/(pres+recall)
        print(str(i)+":	P="+str(pres)+" R="+str(recall)+" F="+str(f1)) 
    print(acc)
    
def main():
    catg_true,catg_pred = read_test_pred()
    calculate_statistics(catg_true,catg_pred)

if __name__ == "__main__" :
    main()