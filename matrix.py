#Libraries#
import re
import pandas as pd
import numpy as np
import subprocess
import os
#/Libraries#

#maximal number of lemmas for graph
N_max=10000
#/maximal number of lemmas for graph

#Read frequencies/lemmas into lists#
python_path=os.path.dirname(os.path.abspath(__file__))
file_path=python_path+'/txt/freq.txt';#create absolute path
fr_init=open(file_path,'r',encoding = "utf-8");fr=list(fr_init)
fr=[int(item) for item in fr]#convert to integer
fr_init.close()

file_path=python_path+'/txt/lemmas.txt';#create absolute path
lm_init=open(file_path,'r',encoding='UTF-8');lm=list(lm_init)
lm=[str(item) for item in lm]#convert to string
lm_init.close()

number_of_freq=len(fr);print('Number of frequencies='+str(number_of_freq))
number_of_lemmas=len(lm);print('Number of lemmas='+str(number_of_lemmas))
#/Read frequencies/lemmas into lists#

#Create empty lists#
freq_list=[]#frequency list
word1=[];word2=[]#word lists
token_list=[]#token list
#/Create empty lists#

#Lists filtered by threshold#
n=0;m=0;
for item in fr:
    freq_list.append(item);n+=1
    if n==N_max:break
for item in lm:
    w1=item.split()[0];w2=item.split()[1]
    word1.append(w1);word2.append(w2)
    token_list.append(item);m=m+1
    if m==N_max:break

print('Filtered number of lemmas='+str(len(freq_list)))    
#/Lists filtered by threshold#

#Create unique vocabulary#
vocab=[];vocab_dirty=word1+word2;
for item in vocab_dirty:
    if len(item)>2:vocab.append(item)
unique_vocab=list(set(vocab))

file_path=python_path+'/txt/uniq_voc.txt';#create absolute path
uniq=open(file_path,'w',encoding='utf8')
for item in unique_vocab: uniq.write(str(item)+'\n')
uniq.close()

dim=len(unique_vocab)   
print('Unique vocabulary length='+str(len(unique_vocab)))
print('\nUnique vocabulary is written!\n')  
#/Create unique vocabulary#

#Create matrix#
w,h=len(unique_vocab),len(unique_vocab);##create two ranges
Matrix=[[0 for x in range(w)] for y in range(h)]#NxN zero matrix
percent=0;

for i in range(dim):
    if round(100*i/(dim-1))>percent:
        print('Process:'+str(round(100*i/(dim-1)))+'%');
        percent=round(100*i/(dim-1))
        
    for j in range(i+1):
        if i==j:Matrix[i][j]=0;Matrix[j][i]=0;continue #remove diagonal elements    
        count=0;
        for item in token_list:
           if re.search(str(unique_vocab[i]),item) and re.search(str(unique_vocab[j]),item):
               count+=1
        Matrix[i][j]=count;
        Matrix[j][i]=count
#/Create matrix#

#Create csv file of matrix#
df=pd.DataFrame(np.matrix(Matrix),columns=unique_vocab,index=unique_vocab)
df.to_csv('graph-10000.csv',sep = ',')
#/Create csv file of matrix#

#end of script#
subprocess.call(["E:\wmplayer.exe", "E:\smoke.mp3"])
print('\nGraph is created!')
print('\nFinished')
#/end of script# 



