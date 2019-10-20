
  TTDS Coursework 1 - 20/10/2019
  
  The system was build using Python 3.7.4 on Anaconda.

  Dependencies:
  - collections
  - re
  - itertools
  - xml.etree.ElementTree
  - sys
  - math
  - operator
  - stemming.porter2

  Folder Contents:
  - index.txt                  index built by preprocessing.py
  - preprocessing.py           used to pre-process the text and build the index of the collection
  - search_modules.py          used for toolean search,phrase search and proximity search
  - tfidf.py                   used for term frequency–inverse document frequency
  - stopWords.txt              contains all stop words
  - results.ranked.txt         results from tfidf.py
  - results.boolean.txt        results from search_modules.py
  - queries.ranked.txt         queries read by tfidf.py
  - queries.boolean.txt        queris read by search_modules.py

  Running the system:

    Create a conda environment and install the dependencies mentioned above.
    Then: 
   - $ python3 preprocessing.py           to preprocess the collection and build the index
   - $ python3 search_modules.py          to run the boolean queries and save the results in results.boolean.txt
   - $ python3 tfidf.py                   to run the ranked queries and save the results in results.ranked.txt