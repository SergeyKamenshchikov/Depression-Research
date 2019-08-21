import requests #HTTP library
from bs4 import BeautifulSoup #html edit
import re #regular expressions
import csv
import os
import subprocess
import pymorphy2 #morpholizer

#Create object for morphologic analysis#
morph=pymorphy2.MorphAnalyzer()

#current directory#
absolute_path=os.path.dirname(os.path.abspath(__file__))

#Counters#
start=1;

#Create list of unique links
file_path=absolute_path+'/txt/links.txt';#create absolute path
file_list=list(open(file_path,'r',encoding='utf-8'))#read links into the list
file_list=list(set(file_list))#make unique list
mes=len(file_list)#length of list

#Read link content#
for i in range(start,mes):
  url='http://www.pobedish.ru'+file_list[i]#construct url

  #connection
  cont=BeautifulSoup(requests.get(url).content,'html.parser')
  #/connection
  
  #get age
  age_content=cont.find('p', attrs = {'class': 'ist'}).text#Ectract text of <p class="ist"></p>
  age_content=''.join(age_content.split())#remove places
  a=age_content.find('возраст:')+len('возраст:');
  age_content=age_content[a:]#slicing
  age_content=re.sub("[^0-9]","",age_content)#remove non numeric
  age_content=age_content[0:2]#first 2 symbols
  #/get age

  #define gender
  gender_content=cont.find('p', attrs = {'class': 'ist'}).text #Ectract text of <p class="ist"></p>
  gender_content=''.join(gender_content.split(',')[0].split());gender=morph.parse(gender_content)[0].tag.gender
  if gender=='masc': gen='men' #men
  elif gender=='femn': gen='woman' #woman
  else:gen='undefined' #undefined
  #/define gender

  #define length of message
  mes_content=cont.find('div', attrs = {'class': 'text'}).text #Ectract text of <div class="text"></div>
  a=mes_content.find('Напишите свою историю')+len('Напишите свою историю');
  b=mes_content.find('Поддержите сайт');
  length=len(mes_content[a:b].split());
  #/define length of message

  #write to file
  if int(age_content)>10 and (gen!='undefined') and int(length)>100:#filters of age,gender,length of message

    #variables for record
    age=str(age_content)#age string
    gen=str(gen)#gender
    length=str(length)#length of message
    url_unq=str(file_list[i][10:])#short url
    #/variables for record

    #write variables to file
    file_path=absolute_path+'/txt/age-urls-gender-length.txt';file=open(file_path,'a',encoding='utf-8');
    record=(age+';'+gen+';'+str(length)+';'+url_unq);
    file.write(record);file.close();
    #/write variables to file

  #loading bar
  print(str(i)+' out of '+ str(mes));
  #loading bar 

#/Read link content#
   
#End of script#
subprocess.call(["E:\wmplayer.exe", "E:\smoke.mp3"])
print('\nFinished')
#/End of script#  


















