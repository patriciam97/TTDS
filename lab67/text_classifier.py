import re

def find_unique_terms(words,unique,index):
    for word in words:
        if word not in unique:
            unique[word]=index
            index+=1
    return unique,index

def save_unique_terms (unique):
    file_Title= "feats.dic"
    f = open(file_Title,"w+")
    for word,index in unique.items():
        f.write(word+" : "+str(index)+"\n")
    f.close()

def read_training_data():
    title = "tweetsclassification/Tweets.14cat.train"
    f = open(title)
    unique = {}
    index = 1
    for line in f.readlines():
        parts = (line.split("\t"))
        if len(parts) == 3:    
            id_ = parts[0]
            tweet = parts[1]
            category = parts[2]
            alphabetic_chars = re.compile('[^a-zA-Z]')
            words = [word if word[0:7]!="http://" else "" for word in tweet.split(" ")]
            words = [alphabetic_chars.sub("",word) for word in words]
            unique,index = find_unique_terms(words,unique,index)
    save_unique_terms(unique)
    f.close()
def main():
    read_training_data()

if __name__ == "__main__" :
    main()