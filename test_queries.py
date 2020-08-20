import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import nltk
import numpy as np
from collections import Counter
from nltk.util import ngrams
import re 
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import CountVectorizer
import math

def test_query(query):
  posting_list = np.load('posting_list2.npy',allow_pickle='TRUE').item()
  norm_improv1 = np.load('norm2.npy')
  title=np.load('titles2.npy')
  N=len(norm_improv1)

  # query=input("Enter your query:")
  # print(query)


  vectorizer = CountVectorizer()
  query = query.lower()
  query = re.sub(r'[^\w\s]', '', query)
  query_uni_raw = nltk.word_tokenize(query)

#correcting spellings in the query
  spell = SpellChecker()
  query_uni=[]
  for word in query_uni_raw:
      query_uni.append(spell.correction(word))

  lemmer=WordNetLemmatizer()
  lemWords_unigram_verb=[lemmer.lemmatize(word,pos="v") for word in query_uni]
  lemWords_unigram_adverb=[lemmer.lemmatize(word,pos="a") for word in lemWords_unigram_verb]
  query_uni=[lemmer.lemmatize(word, pos="n") for word in lemWords_unigram_adverb]


  query_tf_raw = Counter(query_uni)

#calculating query term frequency weight
  dictkeys = list (posting_list.keys())
  query_tf_wt = dict([(key, val) for key, val in 
             query_tf_raw.items() if key in dictkeys])
  for i in query_tf_wt:
      query_tf_wt[i]=1+math.log10(query_tf_wt[i])
    
#calculating query document frequency weight
  query_df_wt = query_tf_wt
  query_df_wt= {x: math.log10(N/len(posting_list[x])) for x in query_df_wt}
  query_wt = query_tf_wt
  query_wt={x: (query_df_wt[x]*query_tf_wt[x])*(query_df_wt[x]*query_tf_wt[x]) for x in query_wt}
# print(query_wt)

#finding final query weights using ltc scheme
  dlist=list(query_wt.values())
  norm=(math.fsum(dlist))**0.5
  query_wt={x: (query_df_wt[x]*query_tf_wt[x])for x in query_wt}
  query_wt.update((k,v/norm) for (k,v) in query_wt.items())
# print(query_wt)


# In[9]:


#finding weights of query words in docs using lnc scheme
  normal= {i: [] for i in query_wt} 
  final_score=[0]*N
  for i in query_wt:
      for x in range(len(posting_list[i])):
          normal[i].append((posting_list[i][x][0],((1+math.log(posting_list[i][x][1]))/math.sqrt(norm_improv1[posting_list[i][x][0]])*query_wt[i])))
          final_score[normal[i][x][0]]=final_score[normal[i][x][0]]+normal[i][x][1]
# print(normal)
# print(final_score)


# In[10]:


#sorting the scores array and printing titles of results
  final=np.argsort(final_score)
# print(final[-10:])
# print(final)
  final_final=final[-10:]
  ret=[]
  for i in range(len(final_final)):
      if(final_score[final_final[9-i]]>0):
        ret.append(title[final_final[9-i]])
      else:
        ret.append("No more Files")
        break
  return ret




def all_docs():
    title=np.load('titles2.npy')
    ret=[]
    for i in title:
        ret.append(i)
    return ret