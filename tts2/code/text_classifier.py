import re
from stemming.porter2 import stem

import requests
from urllib import request, response, error, parse
from urllib.request import urlopen
from bs4 import BeautifulSoup


training_path = "tweetsclassification/Tweets.14cat.train"
testing_path = "tweetsclassification/Tweets.14cat.test"
stop_words = {}
special_chars = re.compile('[^a-zA-Z#]')
non_alpha_chars = re.compile('[^a-zA-Z#]')
links = {}

# set expand links to True in order to expand the tweets with the webpage's title
expand_links = False
stemming = True
stopping = True
hashtags  = True

def read_stop_words():
    # collect stop words
    global stop_words
    f = open ("data/stopWords.txt")
    stop_words = {}
    for x in f.readlines():
        #save stop words in a global list
        stop_words[x.strip()] = 1
    f.close()

def find_unique_terms(words,unique,index):
    for word in words:
        if expand_links:
            if word[0:7]=="http://" :
                if word in links:
                    words.extend(links.get(word).split(" "))
                else:
                    try:
                        html = urlopen(word)
                        soup = BeautifulSoup(html,"lxml")
                        title = soup.title
                        titleText = title.get_text()
                        words.extend(titleText.split(" "))
                        links[word]=titleText
                        print(links)
                    except:
                        pass
        if word != "" and word not in stop_words and word[0:7]!="http://" :
            if word[0]=="#" and hashtags:  
                # append the word without the hashtag character
                words.append(word[1:])
            if hashtags:
                word = special_chars.sub("",word)
            else:
                word = non_alpha_chars.sub("",word)
            if stemming:     
                word = stem(word.strip().lower())
            else:
                word = word.strip().lower()
            if word not in unique:
                unique[word]=index
                index+=1
    return unique,index

def save_unique_terms (unique):
    file_Title= "data/results/feats.dic"
    f = open(file_Title,"w+")
    for word,index in unique.items():
        f.write(word+" : "+str(index)+"\n")
    f.close()

def save_features (features,file_Title):
    f = open(file_Title,"w+")
    for catg_id,words,id_ in features:
        terms = " ".join([str(word)+":"+str(value) for word,value in sorted(words.items())])
        f.write(str(catg_id)+" "+terms+" #"+id_+"\n")
    f.close()

def read_unique_terms():
    unique = {}
    file_Title= "data/results/feats.dic"
    with open(file_Title, encoding="utf8", errors='ignore') as f:
        for line in f.readlines():
            parts = line.split(":")
            unique[parts[0].strip()] = int(parts[1])
        f.close()
    return unique

def read_categories():
    categories = {}
    file_Title= "data/categories.txt"
    with open(file_Title, encoding="utf8", errors='ignore') as f:
        for line in f.readlines():
            parts = line.split("\t")
            categories[parts[0].strip().lower()] = int(parts[1].strip())
        f.close()
        return categories

def read_training_data():
    features = []
    unique = read_unique_terms()
    data = parse_data(training_path)
    categories = read_categories()
    for id_,categ,tweet in data:
        catg_id = categories[categ.strip()]
        words = {}
        for word in tweet:
            if stemming:    
                word = stem(word)
            if word not in words:
                words[unique[word]]=1
        features.append([catg_id,words,id_])
    save_features(features,"data/results/feats.train")

def read_testing_data():
    features = []
    unique = read_unique_terms()
    data = parse_data(testing_path)
    categories = read_categories()
    for id_,categ,tweet in data:
        catg_id = categories[categ.strip()]
        words = {}
        for word in tweet:
            if stemming:
                word = stem(word)
            if (word not in words) and (word in unique):
                words[unique[word]]=1
        features.append([catg_id,words,id_])
    save_features(features,"data/results/feats.test")

def parse_data(title):
    with open(title, encoding="utf8", errors='ignore') as f:
        print("Reading {0}".format(title))
        data = []
        for line in f.readlines():
            parts = (line.split("\t"))
            if len(parts) == 3:    
                id_ = parts[0]
                tweet = parts[1]
                category = parts[2].lower()
                words = tweet.split(" ")
                if expand_links:
                    for word in words:
                        if word[0:7]=="http://" :
                            if word in links:
                                words.extend(links.get(word).split(" "))
                            else:
                                try:
                                    html = urlopen(word)
                                    soup = BeautifulSoup(html,"lxml")
                                    title = soup.title
                                    titleText = title.get_text()
                                    words.extend(titleText.split(" "))
                                    links[word]=titleText
                                    print(links)
                                except:
                                    pass
                # remove any links
                words = [word.strip().lower() if word[0:7]!="http://" else "" for word in words]
                if hashtags:
                    #  remove any non-alphabetic character or non-#
                    words = [special_chars.sub("",word) for word in words]
                else:
                    words = [non_alpha_chars.sub("",word) for word in words]
                # steeming and stopping
                if stemming and stopping:
                    words = [stem(word) for word in words if word.strip() != "" and word not in stop_words.keys()]
                elif stemming:
                     words = [stem(word) for word in words if word.strip() != ""]
                elif stopping:
                    words = [word for word in words if word.strip() != "" and word not in stop_words.keys()]
                else:
                     words = [word for word in words if word.strip() != ""]

                data.append([id_,category,words])
        f.close()
    return data

def extract_unique_terms():
    title = "tweetsclassification/Tweets.14cat.train"
    f = open(title)
    unique = {}
    index = 1
    data = parse_data(training_path)
    for tweet in data:
        unique,index = find_unique_terms(tweet[2],unique,index)
    save_unique_terms(unique)

def main():
    extract_unique_terms()
    print("feats.dic created.")
    read_training_data()
    print("feats.training created.")
    read_testing_data()
    print("feats.testing created.")

if __name__ == "__main__" :
    main()