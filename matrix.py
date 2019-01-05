#Libraries#
import re
import pandas as pd
import numpy as np
import subprocess
import os
#/Libraries#

#maximal number of lemmas for graph#
N_max=10000
#/maximal number of lemmas for graph#

#path to root directory#
python_path=os.path.dirname(os.path.abspath(__file__))
#/path to root directory#

#read frequencies into list#
file_path=python_path+'/txt/freq.txt';
fr_init=open(file_path,'r',encoding='utf8');
fr=list(fr_init);fr=[int(item) for item in fr]#convert to integer
fr_init.close()
#/read frequencies into list#

#read lemmas into list#
file_path=python_path+'/txt/lemmas.txt';#create absolute path
lm_init=open(file_path,'r',encoding='utf8');
lm=list(lm_init);lm=[str(item) for item in lm]#convert to string
lm_init.close()
#/read lemmas into list#

#statistics of frequencies/lemmas#
number_of_freq=len(fr);
print('Number of frequencies='+str(number_of_freq))
number_of_lemmas=len(lm);
print('Number of lemmas='+str(number_of_lemmas))
#/statistics of frequencies/lemmas#

#create empty lists#
freq_list=[]#frequency list
word1=[];word2=[]#word lists
token_list=[]#token list
#/create empty lists#

#filtering by threshold#
n=0;
for item in fr:
    freq_list.append(int(item));n+=1
    if n==N_max:break

m=0;
for item in lm:
    w1=item.split()[0];w2=item.split()[1]
    w1=''.join([i for i in w1 if not i.isdigit()]);w2=''.join([i for i in w2 if not i.isdigit()])
    word1.append(str(w1));word2.append(str(w2));   
    token_list.append(item);m=m+1#create dirty tokens
    if m==N_max:break

print('Filtered number of lemmas='+str(len(freq_list)))    
#/filtering by threshold#

#create unique vocabulary#
vocab=[];
vocab_dirty=(word1+word2)
for item in vocab_dirty:
    if len(item)>2:vocab.append(item)
unique_vocab=list(set(vocab))
#/create unique vocabulary#

#write vocabulary to uniq_voc.txt#
file_path=python_path+'/txt/uniq_voc.txt';#create absolute path
uniq=open(file_path,'w',encoding='utf8')
for item in unique_vocab: uniq.write(str(item)+'\n')
uniq.close()
print('\nUnique vocabulary is written!\n') 
#/write vocabulary to uniq_voc.txt#

#unique vocabulary statistics#
dim=len(unique_vocab)#dimension of unique vocabulary   
print('Unique vocabulary length='+str(len(unique_vocab))+'\n')
#/unique vocabulary statistics#

#create zero matrix#
w,h=len(unique_vocab),len(unique_vocab);
Matrix=[[0 for x in range(w)] for y in range(h)]
#/create zero matrix#

#create filled matrix#
percent=0;except_num=0;
for i in range(dim):#iterate over unique vocabulary
    #counter#
    if round(100*i/(dim-1))>percent:
        print('Process:'+str(round(100*i/(dim-1)))+'%');
        percent=round(100*i/(dim-1))
    #/counter#    
        
    for j in range(i+1):
        if i==j:Matrix[i][j]=0;Matrix[j][i]=0;continue #remove diagonal elements    
        count=0;
        for item in token_list:
            try:
                if re.search(str(unique_vocab[i]),item) and re.search(str(unique_vocab[j]),item):count+=1
            except Exception:
                except_num+=1
                continue    
        Matrix[i][j]=count;
        Matrix[j][i]=count
#/create filled matrix#

#exceptions statistics# 
print('\n'+'Exceptions:'+str(except_num)+'\n')
#/exceptions statistics#

#create csv file of matrix#
df=pd.DataFrame(np.matrix(Matrix),columns=unique_vocab,index=unique_vocab)
csv_name=('graph-'+str(N_max)+'.csv')
df.to_csv(csv_name,sep=',')
#/create csv file of matrix#

#end of script#
subprocess.call(["E:\wmplayer.exe", "E:\smoke.mp3"])
print('\nGraph is created!')
print('\nFinished')
#/end of script# 



