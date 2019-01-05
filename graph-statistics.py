import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import collections
from scipy.stats import skew
from scipy.stats import kurtosis
import numpy as np
import os

#Create graph object from adjency matrix#
python_path=os.path.dirname(os.path.abspath(__file__))
file_path=python_path+'\graph-10000.csv';#create absolute path
df=pd.read_csv(file_path,index_col=0)#read matrix from csv
G=nx.Graph(df.values)
#Create graph object from adjency matrix#

#Replace node names#
mapping={}
words_list=list(df.index)#words 
keys_list=list(range(len(words_list)))
mapping=dict(zip(keys_list,words_list))
G=nx.relabel_nodes(G,mapping)#replace node names
#/Replace node names#

#degree centrality#
degree_centrality=list(nx.degree_centrality(G).values());dc_labels=list(nx.degree_centrality(G).keys())

max_dc=round(100*max(degree_centrality));min_dc=round(100*min(degree_centrality))
av_dc=round(100*np.average(degree_centrality));attractor_dc=dc_labels[degree_centrality.index(max(degree_centrality))]
print('Maximum DC='+str(max_dc)+'%');print('Minimum DC='+str(min_dc)+'%')
print('Average DC='+str(av_dc)+'%');print('Attractor DC label=['+str(attractor_dc)+']\n')

aray_dc=np.array(degree_centrality);aray_lb1=np.array(dc_labels)
ind=aray_dc.argsort()#sort indexes correspondingly
sorted_dc_values=list(aray_dc[ind])[::-1];sorted_dc_labels=list(aray_lb1[ind])[::-1]

print('<Arranged list of DC attractors>');DC_list=[]
for i in range(10): DC_list.append(str(sorted_dc_labels[i])+' ('+str(int(round(100*sorted_dc_values[i])))+'%'+')')
print(DC_list)    
#/degree centrality#betweenness

#betwennes centrality#
between_centrality=list(nx.betweenness_centrality(G).values());bс_labels=list(nx.betweenness_centrality(G).keys())

max_bc=round(100*max(between_centrality));min_bc=round(100*min(between_centrality))
av_bc=round(100*np.average(between_centrality));attractor_bc=bс_labels[between_centrality.index(max(between_centrality))]
print('\nMaximum BC='+str(max_bc)+'%');print('Minimum BC='+str(min_bc)+'%')
print('Average BC='+str(av_bc)+'%');print('Attractor BC label=['+str(attractor_bc)+']\n')

aray_bc=np.array(between_centrality);aray_lb2=np.array(bс_labels)
ind=aray_bc.argsort()#sort indexes correspondingly
sorted_bc_values=list(aray_bc[ind])[::-1];sorted_bc_labels=list(aray_lb2[ind])[::-1]

print('<Arranged list of BC attractors>')
BC_list=[]
for i in range(10):
    BC_list.append(str(sorted_bc_labels[i])+' ('+str(int(round(100*sorted_bc_values[i])))+'%'+')')
print(BC_list) 
#/betwennes centrality#

#neighbors#
key_node='депрессия'
print('\nСоседи слова ['+str(key_node)+']:')
print(list(G.neighbors(key_node))[0:10])
#/neighbors#

print('\nFinished')


