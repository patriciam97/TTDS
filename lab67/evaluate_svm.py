from sklearn.metrics import confusion_matrix,multilabel_confusion_matrix
from collections import OrderedDict

def read_test_pred():
    catg_true, catg_pred =[],[]
    with open("feats.test", encoding="utf8", errors='ignore') as t:
        for line in t.readlines():
            true_catg = line.split(" ")[0]
            catg_true.append(true_catg)
    t.close()
    with open("pred4000.out", encoding="utf8", errors='ignore') as p:
        for line in p.readlines():
            pred_catg = line.split(" ")[0]
            catg_pred.append(pred_catg)
    p.close()
    return catg_true, catg_pred

def calculateConfusionMatrix(distinctClasses, testClassesList, predictionClassesList):
    """Calculates the confusion matrix of the classifier
    Returns
    -------
    confusionMatrix : Dictionary type
        Confusion matrix - Dictionary of Dictionaries and frequencies
    """
    confusionMatrix = OrderedDict()
    for index in distinctClasses:
        confusionMatrix[index] = OrderedDict()
        for innerIndex in distinctClasses:
            confusionMatrix[index][innerIndex] = 0

    totalPredictions = len(testClassesList)
    for i in range(0, totalPredictions):
        confusionMatrix[int(testClassesList[i])][int(predictionClassesList[i])] += 1

    return confusionMatrix
    
def calculate_statistics(catg_true,catg_pred):
    accuracies,precisions,recalls,f1 = [],[],[],[]
    print( multilabel_confusion_matrix(catg_true,catg_pred))
    # for i,category in enumerate(calculateConfusionMatrix(list(range(1,15)),catg_true,catg_pred),1):
    for i,category in enumerate(multilabel_confusion_matrix(catg_true,catg_pred,labels = list((range(1,15)))),1):
        tn, fp, fn, tp = category.ravel()
        accuracies.append((tp)/(tn + fp + fn + tp ))
        pres = tp/(tp+fp)
        precisions.append(pres)
        recall = tp/(tp+fn)
        recalls.append(recall)
        f1.append((2*float(pres)*float(recall))/((float(pres)+float(recall))))
    save_statistics(accuracies,precisions,recalls,f1)
   
def save_statistics(accuracies,precisions,recalls,f1):
    file_Title= "Eval4000.txt"
    f = open(file_Title,"w+")  
    f.write("Accuracy: " + str(round(sum(accuracies),3))+"\n")
    f.write("Macro-F1: " + str(round(sum(f1)/len(f1),3))+"\n")
    for i,pres in enumerate(precisions):
        f.write(str(i+1)+":\tP="+str(round(pres,3))+"\tR="+str(round(recalls[i],3))+"\tF="+str(round(f1[i],3))+"\n") 
    print("Eval4000.txt saved.")
def main():
    catg_true,catg_pred = read_test_pred()
    calculate_statistics(catg_true,catg_pred)

if __name__ == "__main__" :
    main()