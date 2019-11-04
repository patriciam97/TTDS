from sklearn.metrics import multilabel_confusion_matrix

def read_test_pred():
    catg_true, catg_pred =[],[]
    with open("feats.test", encoding="utf8", errors='ignore') as t:
        for line in t.readlines():
            true_catg = line.split(" ")[0]
            catg_true.append(true_catg)
    t.close()
    with open("pred.out", encoding="utf8", errors='ignore') as p:
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
    print(accuracies)
    print("Accuracy: " + str(round(sum(accuracies)/len(accuracies),3)))
    print("Macro-F1: " + str(round(sum(f1)/len(f1),3)))
    for i,pres in enumerate(precisions):
        print(str(i+1)+":   P="+str(round(pres,3))+"   R="+str(round(recalls[i],3))+"   F="+str(round(f1[i],3))) 

    
def main():
    catg_true,catg_pred = read_test_pred()
    calculate_statistics(catg_true,catg_pred)

if __name__ == "__main__" :
    main()