#Libraries#
import pandas as pd
import numpy as np
import math
from nltk.stem.snowball import SnowballStemmer
from stop_words import get_stop_words
import subprocess
import os
import matplotlib.pyplot as plt
import collections
from random import sample
from sklearn.feature_extraction.text import CountVectorizer
import re
import nltk
from nltk.util import ngrams
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.tokenize import word_tokenize
import pymorphy2
import distance
from scipy.stats import skew
from scipy.stats import kurtosis
#/Libraries#

#Params#
standartization=False
n=2;#Dimension of n-gramms
m=100;#Number of displayed n-gramms
#/Params#

#Show standartization FT
print('\nStandartization='+str(standartization))
#/Show standartization FT

#PDF function
def distribution(z,k):#z - list,k - label

    plt.hist(z,rwidth=0.9)
    plt.xlabel(k);
    plt.ylabel('Frequency')
    plt.show()
#/PDF function    
   
#Read content of file to str
python_path=os.path.dirname(os.path.abspath(__file__))
file_path=python_path+'/txt/help-norm.txt';#create absolute path
f=open(file_path,'r',encoding = "utf-8")
file_content=f.read()#read file to string
f.close()
#/Read content of file to str

#Count words#
counted_words=len(file_content.split())
print('\nЧисло слов:',str(counted_words))
#/Count words#

#Sentence length distribution#
sent_content=file_content.replace('[END]','.').replace('?','.').replace('!','.')#preprocess
sent_content=sent_content.replace(';','.')#preprocess
sent_content=sent_content.split('.');

sent_len=[]#list of sentences
for item in sent_content: sent_len.append(len(item.split()))#take sentence lengths

print('\nСредняя длина предложения: '+str(round(np.mean(sent_len))))#average length of sent_len
print('Стандартное отклонение: '+str(round(np.std(sent_len))));print('Медиана: '+str(round(np.median(sent_len))))#mediane length of sent_len
print('Минимум: '+str(round(min(sent_len))));print('Максимум: '+str(round(max(sent_len))))
print('Скошенность: '+str(round(skew(sent_len),2)));print('Эксцесс: '+str(round(kurtosis(sent_len),2)))
#distribution(sent_len,'sentence_length');
#/Sentence length distribution#

#Remove waste from merged file except [END] and Cases#
processed_content=file_content.replace('?',' ').replace('!',' ').replace(';',' ')#preprocess
processed_content=processed_content.replace("'",'')
processed_content=processed_content.strip('\n\t')
processed_content=processed_content.replace(',',' ').replace('.',' ').replace('-',' ')
processed_content=processed_content.replace('(','').replace(')','').replace('ред мод',' ')
processed_content=processed_content.replace('<','').replace('>','')
#/Remove waste from merged file except [END] and Case#

#Normalize the text#
morph=pymorphy2.MorphAnalyzer()#Morphology analyzer initiate
stemmer=SnowballStemmer("russian")
stop_words=get_stop_words('russian')
norm_mes=processed_content.split('[END]')#split processed text into messages
print('\nЧисло сообщений: ',len(norm_mes))

msg_lst=[];txt_stemmed=[];k=0;percent=0;
print('\n')
for item in norm_mes:#iterating over messages  
    #preloader#
    k=k+1;progress=round(100*k/len(norm_mes));
    if round(progress)>percent:
        print('Process:'+str(progress)+'%')
        percent=progress
    #/preloader#    

    #word collection#
    mes_dict=item.split(' ')
    #/word collection#
    
    for word in mes_dict:#iterate over the word
        word=word.lower()#lower case

        if standartization==True:
            lemma=morph.parse(word)[0].normal_form #transform word into normal form
            if ('NOUN' in morph.parse(word)[0].tag)==True:msg_lst.append(str(lemma))#create message list
        else:          
            lemma=word;msg_lst.append(str(lemma))#create message list    

    #create txt_stemmed list of standartized constructs#
    msg=" ".join(msg_lst)#Reconstruct message
    msg_lst=[]#reload msg container    
    txt_stemmed.append(str(msg))
    #/create txt_stemmed list of standartized constructs#
#/Normalize the text#

#Creating n-gramms#
content_string=" ".join(txt_stemmed)#convert list to string
text_token=nltk.word_tokenize(content_string);#split into words
ngrams=list(nltk.ngrams(text_token,n))#define list of gramms
ngrams_processed=[]

if standartization==True:
    for item in ngrams:
        item_x=str(item).replace(",","").replace("(","").replace(")","").replace("'","")
        if item_x in stop_words:continue #test stopwords
        ngrams_processed.append(item);      
if standartization==False:
    ngrams_processed=ngrams;
        
ngramsFreqs=nltk.FreqDist(ngrams_processed)#Determine frequency of ngrams
freq_len_st=len(list(ngramsFreqs))  
keys_list=[str(i[0]).replace(",","").replace("(","").replace(")","").replace("'","") for i in ngramsFreqs.most_common(freq_len_st)]
freq_list=[int(i[1]) for i in ngramsFreqs.most_common(freq_len_st)]
number_of_lemms=sum(freq_list)

if n==2 and standartization==True:
    file_path=python_path+'/txt/lemmas.txt';
    l=open(file_path,'w',encoding='utf8')
    file_path=python_path+'/txt/freq.txt';
    f=open(file_path,'w',encoding='utf8')
    for i in range(1,len(keys_list)):
        l.write(str(keys_list[i])+'\n')
        f.write(str(freq_list[i])+'\n')
    l.close();f.close();

print('\n<Наиболее частые токены>')
for words, count in ngramsFreqs.most_common(m):
    print(" ".join(list(words)))
#Creating n-gramms#

#Энтропия Шеннона#
h_sum=0;
print('\nПорядок энтропии='+str(n))
for item in freq_list: h_sum=h_sum+(item/number_of_lemms)*math.log(item/number_of_lemms)  
print('Энтропия='+str(round(-h_sum,2)))
#Энтропия Шеннона#

#Irrational vocabulary#
reason=['абсолютно','полностью','совершенно','безусловно','постоянно','вечно','всегда','точно','несомненно','вообще','никогда','каждый','все',
        'должен','должна','должны','обязан','обязана','обязаны','я','не','меня','мне','нет']

#Irrational analysis   
hn=0;#number of irrational messages
mn=0;#number of messages
rsn=0;#number of irrationalities

for i in range(len(norm_mes)):
    mn=mn+1;#update number of messages
    reason_found=False#Reload trigger

    for var in reason:
        if re.search(str(var),norm_mes[i]):
            reason_found=True;
            rsn=rsn+1;

    if reason_found==True:
        hn=hn+1
     
print('\nNumber of irrational messages: '+str(hn))
print('Number of messages: '+str(mn))
print('Number of irrationalities: '+str(rsn))

#end of script#
subprocess.call(["E:\wmplayer.exe", "E:\smoke.mp3"])
print('\nFinished')
#/end of script# 







