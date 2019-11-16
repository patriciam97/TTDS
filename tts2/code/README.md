
  TTDS Coursework 2 - 16/11/2019
  
  The system was build using Python 3.7.4 on Anaconda.

  Dependencies:
  - math
  - sklearn.metrics
  - collections
  - re
  - stemming.porter2
  - requests
  - urllib
  - bs4


  Folder Contents:
  - data
    - results                   - Folder that contains all saved outputs from eval.py,evaluate_svm.py, text_classifier.py
    - systems                   - Folder that contains 6 IR systems and true results that are used in eval.py
    - categoris.txt             - Text file that contains available categories for text_classification
    - stopWords.txt             - Text file that contains stop words used in text_classification
  - svm_multiclass_linux_64     - SVM used with results of text_classifier.py
  - svm_multiclass_classify     - SVM used with results of text_classifier.py
  - svm_multiclass_learn        - SVM used with results of text_classifier.py
  - tweetsclassification        - Folder that contains datasets used in text_classifier.py
  - eval.py                     - Code that evaluates the 6 IR Systems against the true documents
  - evaluate_svm.py             - Code that evaluates the results produced by SVM
  - text_classifier.py          - Code that preprocess the tweets in the right format to be used by SVM


  Running the system:

    Create a conda environment and install the dependencies mentioned above.
    Then: 

    FOR TEXT-CLASSIFICATION:
   - $ python3 text_classifier.py
   - Run the SVM:
      - $ ./svm_multiclass_learn -c 1000 data/results/feats.train model 
      - $ ./svm_multiclass_classify data/results/feats.test model pred.out 
   - $ python3 evaluate_svm.py

   FOR IR EVALUATION:
   - $ python3 eval.py