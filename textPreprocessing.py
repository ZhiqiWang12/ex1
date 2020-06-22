import re
import nltk
from nltk.corpus import stopwords as StopwordsLoader

import nltk
nltk.download('book')
from nltk.book import *
texts()
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

def get_wordnet_pos(word):
    #Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def lemma(con_list):
    # Init the Wordnet Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Tokenize: Split the sentence into words
    lem_list = list()
    for word in con_list:
        lem_list.append(lemmatizer.lemmatize(word,get_wordnet_pos(word)))
    lem_str = ''
    for item in lem_list:
        lem_str += word+' '
    return lem_str



stopwords = StopwordsLoader.words()

def match(pattern , string):
    if re.match(pattern,string):
        result = True
    else:
        result = False
    return result
#2.remove hashtag and usermentioned
#3.remove non-alphanumeric characters?
#"([a-z0-9]|[' '])"
def remove_non_alphanumeric(string,pattern):
    con_AlNum = str()
    for x in string:
        if match(pattern,x):
            con_AlNum  += x
    return con_AlNum



def negation_detection(string):
    pattern1 = ".*(\#).*"

    negation_list = ['never','not','but']
    sentences = string.split()
    new_list = []
    negation_flag = False

    words = string.split()
    for word in words:
        if word in negation_list:
            negation_flag = True
        if negation_flag == True and match(pattern1,word)==False:
            new_list.append('not'+word)
        else:
            new_list.append(word)
    new_string = ''
    for item in new_list:
        new_string +=item+' '
    return new_string
def emoji_substitute(string):
    emoji_dict = {':)':'happy',':(':'sad',':P':'tongue',':D':'grin',':O':'gasp',';)':'wink','B|':'glasses','>:(':'grumpy',':/':'unsure',":'(":'cry',"3:)":'devil',"O:)":'angel',':*':'kiss','<3':'heart','^-^':'kiki',"-_-":'squint',"o.O":'confused','>:O':'upset',':v':'pacman',':3':'curly lips',":|]":'robot','(^^^)':'shark','<(")':'penguin','(y)':'thumb'}
    new_string=''
    if string in emoji_dict:
        new_string = (emoji_dict[string]+' ')*8
    else:
        new_string = string
    return new_string
def hash_tag_multiple(string):
    pattern1 = ".*(\#).*"
    pattern2 = "[a-z0-9]"
    new_string = ''
    if match(pattern1,string):
        new_string = remove_non_alphanumeric(string,pattern2)
        new_string  = (new_string+' ')*4
    else:
        new_string = string 
    return new_string

def remove_one_digit_URL_tag(string):
    str_list = string.lower().split()
    str_list_new = list()
    pattern1 = ".+[a-z]"
    pattern3 = ".*(\@).*"
    pattern2 = ".*(((http(s)?)|ftp)|(www|domain)).+"
    pattern4 = "([a-z0-9])"
    i=0
    j=0
    k = 0
    for word in str_list :
        if len(word)>1:#remove the words that only have one character
            if match(pattern1,word):#remove the pure number
                if match(pattern2,word):#remove URL
                    j+=1
                else:
                    if match(pattern3,word):
                        k+=1
                    else:
                        non_str = remove_non_alphanumeric(word,pattern4)
                        if non_str not in stopwords:
                            str_list_new.append(non_str)
        else:
            i+=1
    str_new = ''
    for word in str_list_new:
        str_new +=word+' '
    str_new1 = remove_non_alphanumeric(str_new,pattern4)
    return str_new
def text_preprocess(filename):
    ori_data = {}
    with open(filename,'r') as f:
        line = f.readline()
        while line:
            li = line.split('\t')
            ori_data[li[0]] = [li[1],li[2]]
            line = f.readline()
    pre_data = {}
    #1.emoji substitue
    for item in ori_data:
        ori_list=ori_data[item][1].split()
        adopted_tweets = ''
        for word in ori_list:
            adopted_tweets += emoji_substitute(word)+' '
        ori_data[item][1] = adopted_tweets
    #print(1)
    #2.negation
    for item in ori_data:
        ori_data[item][1]=negation_detection(ori_data[item][1])
    #print(2)
    #3.hash tag
    for item in ori_data:
        ori_list = []
        ori_list=ori_data[item][1].split()
        adopted_tweets = ''
        for word in ori_list:
            adopted_tweets += hash_tag_multiple(word)+' '
        ori_data[item][1] = adopted_tweets
    #print(3)
    #4.remove unrelated symbols
    for item in ori_data:
        string = remove_one_digit_URL_tag(ori_data[item][1])
        ori_data[item][1] = string
    #print(4)
    #5.lemmetizer
    #for item in ori_data:
        #ori_data[item][1] = lemma(ori_data[item][1].split())
    #print(5)
    return ori_data


def transfer_data_con_target(pre_data):
    con = []
    target = []
    for item in pre_data:
        con.append(pre_data[item][1])
        target.append(pre_data[item][0])
    return con, target
