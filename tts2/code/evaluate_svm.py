from sklearn.metrics import confusion_matrix,multilabel_confusion_matrix
from collections import OrderedDict

def read_test_pred(baseline):
    catg_true, catg_pred =[],[]
    with open("data/results/feats.test", encoding="utf8", errors='ignore') as t:
        for line in t.readlines():
            true_catg = line.split(" ")[0]
            catg_true.append(true_catg)
    t.close()
    file = "data/results/pred.out" if baseline else "data/results/pred4000.out" 
    with open("data/results/pred4750.out", encoding="utf8", errors='ignore') as p:
        for line in p.readlines():
            pred_catg = line.split(" ")[0]
            catg_pred.append(pred_catg)
    p.close()
    return catg_true, catg_pred

    
def calculate_statistics(catg_true,catg_pred,baseline):
    accuracies,precisions,recalls,f1 = [],[],[],[]
    for i,category in enumerate(multilabel_confusion_matrix(catg_true,catg_pred,labels = list((range(1,15)))),1):
        tn, fp, fn, tp = category.ravel()
        accuracies.append((tp)/(tn + fp + fn + tp ))
        pres = tp/(tp+fp)
        precisions.append(pres)
        recall = tp/(tp+fn)
        recalls.append(recall)
        f1.append((2*float(pres)*float(recall))/((float(pres)+float(recall))))
    save_statistics(accuracies,precisions,recalls,f1,baseline)
   
def save_statistics(accuracies,precisions,recalls,f1,baseline):
    file_Title= "data/results/Eval.txt" if baseline else "data/results/Eval2.txt" 
    f = open(file_Title,"w+")  
    f.write("Accuracy: " + str(round(sum(accuracies),3))+"\n")
    f.write("Macro-F1: " + str(round(sum(f1)/len(f1),3))+"\n")
    f.write("Results per class:\n")
    for i,pres in enumerate(precisions):
        f.write(str(i+1)+": P="+str(round(pres,3))+" R="+str(round(recalls[i],3))+" F="+str(round(f1[i],3))+"\n") 
    print("${0} saved".format(file_Title))
def main():
    baseline = False
    catg_true,catg_pred = read_test_pred(baseline)
    calculate_statistics(catg_true,catg_pred,baseline)

if __name__ == "__main__" :
    main()