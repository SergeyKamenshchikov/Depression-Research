#libraries#
import os
import subprocess
#/libraries#

#current directory#
absolute_path=os.path.dirname(os.path.abspath(__file__))
#/current directory#

#Create list of unique links#
file_path=absolute_path+'/txt/links.txt';#create absolute path
file_list=list(open(file_path,'r',encoding='utf-8'))#read links into the list
file_list=list(set(file_list))#make unique list of URLs
#/Create list of unique links#

#Write normalized urls#
file_path=(absolute_path+'/txt/links-unique.txt');#create absolute path to age-url dictionary
f=open(file_path,'w',encoding="utf-8");
for item in file_list:
    f.write(str(item)) 
f.close();
#/Write normalized urls#

#End of script#
print('\nFinished')
#/End of script#  
