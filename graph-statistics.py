import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import collections
from scipy.stats import skew
from scipy.stats import kurtosis
import numpy as np
import os

def distribution(z,k):#z - list,k - label

    #List creation 
    x=list(collections.Counter(z).keys())
    y=list(collections.Counter(z).values())
    y=[item/len(z)for item in y]

    #Properties of distribution 
    print('Скошенность='+str(round(skew(z),2)))
    print('Эксцесс='+str(round(kurtosis(z),2)))
    print('Стандартное отклонение='+str(round(np.std(z),2)))

    #Plot
    plt.hist(x,50,rwidth=0.7,weights=y)
    plt.ylim([0,1])
    plt.xlim([0,0.05])
    plt.xlabel(k)
    plt.ylabel('Frequency')
    plt.show()

    #Save file
    my_df=pd.DataFrame(x,y)
    file_name=(k+'.csv')
    my_df.to_csv(file_name)

#Create graph object from adjency matrix#
python_path=os.path.dirname(os.path.abspath(__file__))
file_path=python_path+'/graphs/graph-10000.csv';#create absolute path
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

#Graph parameters
degree_centrality=list(nx.degree_centrality(G).values());dc_labels=list(nx.degree_centrality(G).keys())
F=np.array(degree_centrality);W=np.array(dc_labels)
ind=F.argsort();sorted_dc=list(W[ind])

sorted_dc=sorted_dc[::-1]
print('\nArranged list of DC attractors:')
print(sorted_dc[0:10])

between_centrality=list(nx.betweenness_centrality(G).values());bс_labels=list(nx.betweenness_centrality(G).keys())
F=np.array(between_centrality);W=np.array(bс_labels)
ind=F.argsort();sorted_bc=list(W[ind])

sorted_bc=sorted_bc[::-1]
print('\nArranged list of BC attractors:')
print(sorted_bc[0:10])

max_dc=round(100*max(degree_centrality))
min_dc=round(100*min(degree_centrality))
av_dc=round(100*np.average(degree_centrality))
attractor_dc=dc_labels[degree_centrality.index(max(degree_centrality))]

max_bc=round(100*max(between_centrality))
min_bc=round(100*min(between_centrality))
av_bc=round(100*np.average(between_centrality))
attractor_bc=bс_labels[between_centrality.index(max(between_centrality))]

key_node='депрессия'

#distribution(degree_centrality,'degree_centrality')#plot distribution
#distribution(between_centrality,'between_centrality')#plot distribution

print('\nNumber of nodes='+str(len(G.nodes())))
print('Number of edges='+str(len(G.edges())))

print('\nMaximum DC='+str(max_dc)+'%')
print('Minimum DC='+str(min_dc)+'%')
print('Average DC='+str(av_dc)+'%')
print('Attractor DC label=['+str(attractor_dc)+']\n')

print('\nMaximum BC='+str(max_bc)+'%')
print('Minimum BC='+str(min_bc)+'%')
print('Average BC='+str(av_bc)+'%')
print('Attractor BC label=['+str(attractor_bc)+']\n')

print('Соседи слова ['+str(key_node)+']:')
print(list(G.neighbors(key_node))[0:10])

print('Finished')


