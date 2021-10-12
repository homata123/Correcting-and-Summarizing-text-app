import pandas as pd
import numpy as np
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
import re
from nltk.corpus import stopwords
from textblob import TextBlob as TextCorrect
#
#df = pd.read_csv("tennis.csv")

#print(df['article_text'][1])
#split the sequences into the data by tokenizing them using a list
from nltk.tokenize import sent_tokenize
def correct(file):
    sentences = []
    
    #print("Original text: \n",f0.read())
    
    
    sentences.append(sent_tokenize(file))
    sentences = [y for x in sentences for y in x]
    
    #print(sentences)
    corrected_words=[]

    def convert(lst):
        return (lst.split())
    

    #this old method sometimes pass dot between two nearby words whose blank = 0 .So I try a new
    #lst =  [k]
    #converted=convert(lst)
    #print(converted)
    converted=[]
    for i in sentences:
        k=convert(i)
        for j in k:
            converted.append(j)

    
    index_trace=[]
    stop_words = stopwords.words('english')
    for i in converted:
        corrected_words.append(TextCorrect(i))
    for i in range(len(converted)):
        if converted[i]!=corrected_words[i].correct() and converted[i] not in stop_words:
            index_trace.append(i)

    
    wrong_words=[]
    correct_words=[]
    for i in index_trace:
        wrong_words.append(converted[i])
    
    
    for i in index_trace:
        correct_words.append(corrected_words[i].correct())
    total=[]
    total.append(wrong_words)
    total.append(correct_words)
    return total
