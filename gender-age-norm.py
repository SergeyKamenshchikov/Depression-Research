#Data Frame library#
import pandas as pd
import numpy as np
import subprocess
import matplotlib.pyplot as plt
import requests #HTTP library
import pymorphy2 #morpholizer
from bs4 import BeautifulSoup #html edit
import re #regular expressions
import os #paths

#parameters#
init_pdf=True

#Create object for morphologic analysis#
morph=pymorphy2.MorphAnalyzer()

#current directory#
absolute_path=os.path.dirname(os.path.abspath(__file__))
   
#Read urls-gender-age into the list#
file_path=(absolute_path+'/txt/age-urls-gender-length.txt');#create absolute path to age-url dictionary
f=open(file_path,'r',encoding="utf-8");
age_gender_length_urls=list(f)
f.close();

#Read age-gender-urls single list into the 4 lists#
urls=[];ages=[];gender=[];length=[];#create empty lists

for item in age_gender_length_urls:
    string=item.split(';')#split age-url-gender

    a=int(re.sub('[^0-9]','',string[0]))#age
    b=str(string[1])#gender
    c=int(string[2])#length
    d=('http://www.pobedish.ru/main/help'+string[3])#full url
    d=re.sub('\n','',d)#full url

    ages.append(a)
    gender.append(b)
    length.append(c)
    urls.append(d)
#/Read age-gender-urls single list into the 4 lists#

print('<Число сообщений на входе>:',len(urls),'\n')    

#Age statistics#
if init_pdf==True:
    print('Макс. возраст:',max(ages));print('Мин. возраст:',min(ages))
    print('Средний возраст:',round(np.mean(ages)));print('Медиана',round(np.median(ages)))
    print('Стандартное отклонение:',round(np.std(ages)),'\n')

##    bin_edges=[15,20,25,30,35,40,45,50,55,60,65,70,75]
##    plt.hist(ages,bins=bin_edges,rwidth=0.95)
##    plt.xlabel('Возраст')
##    plt.ylabel('Число сообщений')
##    plt.show()
#/Age statistics#

#Create ranges#
age_ranges=[(20,25),(25,30),(30,35),(35,40),(40,45)]
print('Выбранный диапазон:',age_ranges)
#/Create ranges#    

#Length statistics#
if init_pdf==True:
    print('\nМакс. длина сообщения:',max(length));print('Мин. длина:',min(length))
    print('Средняя длина:',round(np.mean(length)));print('Медиана',round(np.median(length)))
    print('Стандартное отклонение:',round(np.std(length)),'\n')

##    plt.hist(length,20,range=(100,1000),rwidth=0.95)
##    plt.xlabel('Длина сообщения')
##    plt.ylabel('Число сообщений')
##    plt.show()
#/Length statistics#

#Gender statistics#
count_men=0;count_women=0;
for item in gender:
    if item=='men':count_men=(count_men+1)
    if item=='woman':count_women=(count_women+1)

print('Мужчины:',count_men)
print('Женщины:',count_women)
print('Ж/М:',round(count_women/count_men,2))
#/Gender statistics#       

#Create lists#
uniform=[];#list of standartized ages
excluded=[];#ecluded list of URLs
urls_norm=[]#lists of URLs, standartized by ages,gender and length
lengths_norm=[]#list of normalized lengths of messages
#/Create lists#

#Counters#
found=True
gen_old='men'
men_count=0
women_count=0
#/Counters#

#Create uniform distribution with lists of ages,gender,length,urls
while found==True:#match has been found
    for item in age_ranges:#iterate over age ranges
        found=False#reload trigger        
        for i in range(len(urls)):#search match over urls  

            #check filter for url over the age,gender,exclusion 
            if  (item[0]<=ages[i]<item[1]) and gender[i]!=gen_old and (urls[i] not in excluded):#age fits range and gender is changed and url is unique
                gen_old=gender[i];#record old gender

                #update lists
                excluded.append(urls[i])#update excluded list of URLs
                urls_norm.append(urls[i])#add to normalized URLs
                uniform.append(ages[i])#add to standartized ages
                lengths_norm.append(length[i])#add to standartized lengths
                
                #/update lists
                #count genders
                if gender[i]=='men':men_count=(men_count+1)
                if gender[i]=='woman':women_count=(women_count+1)
                #/count genders
                
                found=True;
                break #break cycle of URLs matching
            #/check filter for url over the age,gender,exclusion
            
        if found==False:break #break cycle of range matching      
#/Create uniform distribution with lists of ages,gender,length,urls

#Exclude the remainder
if len(uniform)%len(age_ranges)>0:
    theshold=len(uniform)-(len(uniform)%len(age_ranges))
    uniform=uniform[:theshold]
    urls_norm=urls_norm[:theshold]
#/Exclude the remainder    

print('\nВыполнена нормализация:')

#Distribution of ages
bin_edges=[20,25,30,35,40,45]
plt.hist(uniform,bins=bin_edges,rwidth=0.9)
plt.xlabel('Возраст')
plt.ylabel('Число сообщений')
plt.show()
#/Distribution of ages

#Statistics of ages
print('\nОбъем статистики возрастов:'+str(len(uniform)))
print('Максимум возраста:'+str(round(max(uniform))))
print('Минимум возраста:'+str(round(min(uniform))))
#/Statistics of ages

#Statistics of genders
print('\nМужчины:',int(men_count))
print('Женщины:',int(women_count))
print('Ж/М:',round(women_count/men_count,2))
#Statistics of genders

#Length statistics#
print('\nМакс. длина сообщения:',max(lengths_norm));print('Мин. длина:',min(lengths_norm))
print('Средняя длина:',round(np.mean(lengths_norm)));print('Медиана',round(np.median(lengths_norm)))
print('Стандартное отклонение:',round(np.std(lengths_norm)),'\n')

plt.hist(lengths_norm,20,range=(100,1000),rwidth=0.95)
plt.xlabel('Длина сообщения')
plt.ylabel('Число сообщений')
plt.show()
#/Length statistics#

#URL statistics#
print('Число сообщений:',len(urls_norm))
#/URL statistics#

#Write normalized urls#
file_path=(absolute_path+'/txt/urls-norm-age-gender.txt');#create absolute path to age-url dictionary
f=open(file_path,'w',encoding="utf-8");
for item in urls_norm:
    f.write(str(item)+'\n'); 
f.close();
#/Write normalized urls#

#End of script#
##subprocess.call(["E:\wmplayer.exe", "E:\smoke.mp3"])

print('\nFinished')
#/End of script#

'''
Then we have to add in bayes script length normalization -
reduce to 100 words. And repeat the standard procedure
'''











