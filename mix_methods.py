import pandas as pd
import numpy as np
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
import re
from nltk.corpus import stopwords
import correct_module
#
#df = pd.read_csv("tennis.csv")

#print(df['article_text'][1])
#split the sequences into the data by tokenizing them using a list
from nltk.tokenize import sent_tokenize
sentences = []
input_path=str(input("Nhap duong dan van ban:"))


f00=open(input_path, encoding='utf-8')


sentences.append(sent_tokenize(f00.read()))
f00.close()
sentences = [y for x in sentences for y in x]
print("So cau trong van ban goc:",len(sentences))
summary_number=[]
def input_number(sentences):
  number_of_sentences=0
  while number_of_sentences>len(sentences) or number_of_sentences==0 :
    print("Nhap vao so cau can tom tat:")
    number_of_sentences=int(input())
  else:
    pass
  return number_of_sentences
number_of_sentences=input_number(sentences)
print("Original text:")
f0=open(input_path, encoding='utf-8')
original_text=f0.read()
print(original_text)


f0.close()
#print(sentences)
###print(sentences)
#use the Glove method for word representation
word_embeddings = {}
f = open('glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
clean_sentences = [s.lower() for s in clean_sentences]
stop_words = stopwords.words('english')
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new
clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
#create vectors for the sentences
sentence_vectors = []
for i in clean_sentences:
  if len(i) != 0:
    v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
  else:
    v = np.zeros((100,))
  sentence_vectors.append(v)
#find similarities between the sentences
sim_mat = np.zeros([len(sentences), len(sentences)])
from sklearn.metrics.pairwise import cosine_similarity
for i in range(len(sentences)):
  for j in range(len(sentences)):
    if i != j:
      sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
      #if i==0 and j==1:
        #print(sim_mat[i][j])
#convert the sim_mat similarity matrix into the graph

import networkx as nx

nx_graph = nx.from_numpy_array(sim_mat)
scores = nx.pagerank(nx_graph)
#summarize text
ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
#for i in range(5):
#print("ARTICLE:")
#print(df['article_text'][i])
#print('\n')
print("The first SUMMARY:")

for i in range(number_of_sentences):  
  print(ranked_sentences[i][1])



#jaccard_min-max
def jaccard_minmax(first_document, second_document):
    #calculate jaccard similarity
  sum_min=[]
  sum_max=[] 
  for i in range(min(len(first_document[0]),len(second_document[0]))):
    sum_min.append(min(first_document[0][i],second_document[0][i]))
    sum_max.append(max(first_document[0][i],second_document[0][i]))
  return float(sum(sum_min)/sum(sum_max))

sim_mat2 = np.zeros([len(sentences), len(sentences)])

for i in range(len(sentences)):
  for j in range(len(sentences)):
    if i != j:
      
      sim_mat2[i][j] = jaccard_minmax(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))
#convert the sim_mat similarity matrix into the graph

import networkx as nx

nx_graph2 = nx.from_numpy_array(sim_mat2)
scores2 = nx.pagerank(nx_graph2)
#summarize text
ranked_sentences2 = sorted(((scores2[i],s) for i,s in enumerate(sentences)), reverse=True)
#for i in range(5):
#print("ARTICLE:")
#print(df['article_text'][i])
#print('\n')
print("The second SUMMARY:")

for i in range(number_of_sentences):  
  print(ranked_sentences2[i][1])
  
#jaccard_intersection

def jaccard_inter(first_document, second_document):
    #calculate jaccard similarity
  sum_intersection=0
  
  for i in range(len(first_document[0])):
    if first_document[0][i] in second_document[0]:
      sum_intersection+=1
  sum_union=len(second_document[0])*2-sum_intersection
  return float(sum_intersection/sum_union)

sim_mat3 = np.zeros([len(sentences), len(sentences)])
from sklearn.metrics.pairwise import cosine_similarity
for i in range(len(sentences)):
  for j in range(len(sentences)):
    if i != j:
      
      sim_mat3[i][j] = jaccard_inter(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))
#convert the sim_mat similarity matrix into the graph

import networkx as nx

nx_graph3 = nx.from_numpy_array(sim_mat3)
scores3 = nx.pagerank(nx_graph3)
#summarize text
ranked_sentences3 = sorted(((scores3[i],s) for i,s in enumerate(sentences)), reverse=True)
#for i in range(5):
#print("ARTICLE:")
#print(df['article_text'][i])
#print('\n')
print("The third SUMMARY:")

for i in range(number_of_sentences):  
  print(ranked_sentences3[i][1])
  
#mixing_follow_index_score
ranked_cosine=[]
ranked_jcm=[]
ranked_jci=[]
ranked_sentences_without_score=[]
ranked_sentences2_without_score=[]
ranked_sentences3_without_score=[]
for i in ranked_sentences:
  ranked_cosine.append(i[0])
  ranked_sentences_without_score.append(i[1])
max_cosine=max(ranked_cosine)
for i in ranked_sentences2:
    ranked_jcm.append(i[0])
    ranked_sentences2_without_score.append(i[1])
max_jcm=max(ranked_jcm)
for i in ranked_sentences3:
    ranked_jci.append(i[0])  
    ranked_sentences3_without_score.append(i[1])  
max_jci=max(ranked_jci)

final_score_list=[]   
for sentence in sentences:
  index_cosine=ranked_sentences_without_score.index(sentence)
  index_jaccard_minmax=ranked_sentences2_without_score.index(sentence)
  index_jaccard_inter=ranked_sentences3_without_score.index(sentence)
  final_score=float(ranked_sentences[index_cosine][0]/max_cosine)+float(ranked_sentences2[index_jaccard_minmax][0]/max_jcm)+float(ranked_sentences3[index_jaccard_inter][0]/max_jci)
  final_score_list.append(final_score)


zipped_lists = zip(final_score_list, sentences)
sorted_zipped_lists = sorted(zipped_lists,reverse=True)
sorted_sentences = [element for _, element in sorted_zipped_lists]
print(" \n")  
print("score_list",final_score_list )
print("mixing method summary: \n")

for i in range(number_of_sentences):
  print(sorted_sentences[i])  
