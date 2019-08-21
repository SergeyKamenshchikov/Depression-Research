import requests #HTTP library
from bs4 import BeautifulSoup #html edit
import re #regular expressions
import subprocess
import os

#counters#
start=0;#counter of processed URLs

#current directory#
absolute_path=os.path.dirname(os.path.abspath(__file__))
#/current directory#

#create list of URLs#
file_path=absolute_path+'/txt/urls-norm-age-gender.txt';#create absolute path
f=open(file_path,'r',encoding='utf-8')
url_list=list(f);
f.close()

num_of_mes=len(url_list)
print('Число сообщений:',num_of_mes,'\n')
#/create list of URLs#

#read URL content into help-norm.txt 
for i in range(start,num_of_mes):

  #content parsing#
  cont=BeautifulSoup(requests.get(url_list[i]).content,'html.parser')#Extract html structure
  main_content=cont.find('div', attrs = {'class': 'text'}).text #Ectract text of <div class="text"></div>
  #/content parsing#

  #parse message#
  a=main_content.find('Напишите свою историю')+len('Напишите свою историю');
  b=main_content.find('Поддержите сайт');
  main_content=main_content[a:b];short=main_content.split()[:100]
  main_content=" ".join(short)#transform into collection of words
  #/parse message#
  
  #write normalized urls#
  file_path=(absolute_path+'/txt/help-norm.txt');#create absolute path
  f=open(file_path,'a',encoding="utf-8");
  f.write(str(main_content)+'\n'+'[END]'+'\n'+'\n'); 
  f.close();
  #/write normalized urls#

  #loading bar
  print(str(i)+' out of '+ str(num_of_mes));
  #/loading bar 
#/read URL content into help-norm.txt 

#end of script#
subprocess.call(["E:\wmplayer.exe", "E:\smoke.mp3"])
print('\nFinished')
#/end of script#    


















