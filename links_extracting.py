import requests #HTTP library
from bs4 import BeautifulSoup #html edit
import re #regular expressions
import time

#Initial counter
n=1;
#Scope value
m=2000;
#Starting url
url='http://www.pobedish.ru/main/help?action=&keyword=&where=&page=1'

while str(requests.get(url))=='<Response [200]>' and n<=m:
  #Get html structure
  cont=BeautifulSoup(requests.get(url).content,'html.parser')
  #Extract body structure
  cont=cont.find('body') #content of body
  #Ectract content of a tags
  links=list(cont.findAll('a'))#list of links

  #Create filtered list of links
  link_list=[]
  for link in links:
    if link.get('href').startswith('/main/help/') and link.get('href').endswith('.htm'):
      link_list.append(link.get('href'))

  #Output of link
  print(url)    
   
  #Write link to links.txt
  file=open('links.txt','a',encoding='utf-8')
  for list_item in link_list: file.write(str(list_item+'\n'))
  file.close()

  #Update counter
  n=n+1;
  url='http://www.pobedish.ru/main/help?action=&keyword=&where=&page='+str(n)
  
  results=[]

print('Finished')

















