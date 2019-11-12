from sklearn.metrics import multilabel_confusion_matrix

def read_test_pred():
    catg_true, catg_pred =[],[]
    with open("feats.test", encoding="utf8", errors='ignore') as t:
        for line in t.readlines():
            true_catg = line.split(" ")[0]
            catg_true.append(true_catg)
    t.close()
    with open("pred2.out", encoding="utf8", errors='ignore') as p:
        for line in p.readlines():
            pred_catg = line.split(" ")[0]
            catg_pred.append(pred_catg)
    p.close()
    return catg_true, catg_pred

def calculate_statistics(catg_true,catg_pred):
    accuracies,precisions,recalls,f1 = [],[],[],[]
    for i,category in enumerate(multilabel_confusion_matrix(catg_true,catg_pred),1):
        (tn,fp),(fn,tp) = category
        accuracies.append((tp+tn)/(tn + fp + fn + tp ))
        precisions.append(tp/(tp+fp))
        recalls.append(tp/(tp+fn))
        f1.append((2*float(precisions[-1])*float(recalls[-1]))/((float(precisions[-1])+float(recalls[-1]))))
    save_statistics(accuracies,precisions,recalls,f1)
   
def save_statistics(accuracies,precisions,recalls,f1):
    file_Title= "Eval2.txt"
    f = open(file_Title,"w+")  
    f.write("Accuracy: " + str(round(sum(accuracies)/len(accuracies),3))+"\n")
    f.write("Macro-F1: " + str(round(sum(f1)/len(f1),3))+"\n")
    for i,pres in enumerate(precisions):
        f.write(str(i+1)+":\tP="+str(round(pres,3))+"\tR="+str(round(recalls[i],3))+"\tF="+str(round(f1[i],3))+"\n") 
    print("Eval2.txt saved.")
def main():
    catg_true,catg_pred = read_test_pred()
    calculate_statistics(catg_true,catg_pred)

if __name__ == "__main__" :
    main()