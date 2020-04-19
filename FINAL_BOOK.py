#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 7:11:46 2020

@author: prituldave
"""
from nxviz import MatrixPlot,ArcPlot,CircosPlot
from hiveplot import HivePlot
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
def ecdf(data):
    return np.sort(data),np.arange(1,len(data)+1)/len(data)

for i in range(1,6):
    df = pd.read_csv("/Users/prituldave/projects/networkx/GOT/book"+str(i)+".csv")
    
    print(df.head())
    
    
    G = nx.Graph()
    '''G.add_nodes_from(df['Source'])
    G.add_nodes_from(df['Target'])'''
    
    
    for s,t,w in zip(df['Source'],df['Target'],df['weight']):
        G.add_edge(s,t,weight=w)
        
    print(G.nodes(data=True))
    #pos = nx.spring_layout(G)
    plt.axis('equal') 
    nx.draw(G,with_labels=True,font_size=5,node_size=8);plt.show()
    #nx.draw_networkx_edge_labels(G,pos)
    

    m = MatrixPlot(G)
    m.draw();plt.show()
    
    
    a = ArcPlot(G)
    a.draw();plt.show()
    
    
    c = CircosPlot(G)
    c.draw()
    
    
    
    #Top 5 import persons without weights#
    persons_list = []
    for p in G.nodes:
        persons_list.append([p,len(list(G.neighbors(p)))])
    vvip_list = sorted(persons_list, key = lambda x: x[1],reverse=True)
    print("\n Top5 interactions in Book without weights \n"+str(i),vvip_list[:5])
    
    
    #Visualizing degree of centrality#
    fig = plt.figure(i+6)
    neighbors = [len(list(G.neighbors(node))) for node in G.nodes()]
    x, y = ecdf(neighbors)
    plt.scatter(x, y)
    plt.title('\nNumber of Neighbors');plt.show()
    
    
    
    #Betweeness centrality#
    print("\nBetweeness centraility without weights",sorted(nx.betweenness_centrality(G).items(), key=lambda x:x[1], reverse=True)[0:5])
    
    
    
    #Top 5 important persons with weights#
    #sorted(weighted_degree(G, 'weight').items(), key=lambda x:x[1], reverse=True)[0:10]
    l = list(G.degree(weight='weight'))
    vvip_list = sorted(l, key = lambda x: x[1],reverse=True)
    print("\n Top5 interactions in Book with weight\n"+str(i),vvip_list[:5])
    
    #Betweeness centraility#
    print("\nBetweeness centraility with weights",sorted(nx.betweenness_centrality(G,weight='weight').items(), key=lambda x:x[1], reverse=True)[0:5])
    


'''
Conclusion:-
Eddard Stark is highly important person in book1 
Information passing is highly done by Robert-Baratheon in book1
Tyrion-Lannister is highly important person in book2 and book3
Information passing is highly done by Jaime-Lannister in book2
Information passing is highly done by Joffrey-Baratheon in book3
Jaime-Lannister and Cersei-Lannister is highly important person in book4
Information passing is highly done by Stannis-Baratheon in book4 and book5
Jon-Snow is highly important person in book5
'''


#Evolution of character importance#
edd_stark=[]
Tyrion_Lannister=[]
Jaime_Lannister=[]
Jon_Snow=[]
for i in range(1,6):
    df = pd.read_csv("/Users/prituldave/projects/networkx/GOT/book"+str(i)+".csv")
    G = nx.Graph()
    for s,t,w in zip(df['Source'],df['Target'],df['weight']):
        G.add_edge(s,t,weight=w)
    
    edd_stark.append(nx.degree_centrality(G).get('Eddard-Stark'))
    Tyrion_Lannister.append(nx.degree_centrality(G).get('Tyrion-Lannister'))
    
    Jaime_Lannister.append(nx.degree_centrality(G).get('Jaime-Lannister'))
    
    Jon_Snow.append(nx.degree_centrality(G).get('Jon-Snow'))
    

plt.plot(edd_stark,label='Eddard-Stark')
plt.plot(Tyrion_Lannister,label='Tyrion-Lannister')
plt.plot(Jaime_Lannister,label='Jaime-Lannister')
plt.plot(Jon_Snow,label='Jon-Snow')
plt.legend(loc='best')
plt.show()

'''
Conclusion:-
Interaction of Jon snow increase by book 5
Interaction of Eddard-Stark completely decrease by book5 which indicating he dies off as book progress
'''


#Whats up with Stannis Baratheon#
for i in range(1,6):
    df = pd.read_csv("/Users/prituldave/projects/networkx/GOT/book"+str(i)+".csv")
    G = nx.Graph()
    for s,t,w in zip(df['Source'],df['Target'],df['weight']):
        G.add_edge(s,t,weight=w)
    print(sorted(nx.betweenness_centrality(G,weight='weight').items(), key=lambda x:x[1], reverse=True)[0:5])   

'''
Conclusion:-
Betweeness centrality of Stannis-Baratheon is high in Book4 and Book5.
It means he has done maximum interaction in Book4 and Book5
'''
#Page Rank#
temp = []
for i in range(1,6):
    df = pd.read_csv("/Users/prituldave/projects/networkx/GOT/book"+str(i)+".csv")
    G = nx.Graph()
    for s,t,w in zip(df['Source'],df['Target'],df['weight']):
        G.add_edge(s,t,weight=w)
    print("\n Page rank for book ",i)
    print(sorted(nx.pagerank_numpy(G, weight=None).items(), key=lambda x:x[1], reverse=True)[0:10])



#Correlation:- Combining all and analyzing#
for i in range(1,6):
    df = pd.read_csv("/Users/prituldave/projects/networkx/GOT/book"+str(i)+".csv")
    G = nx.Graph()
    for s,t,w in zip(df['Source'],df['Target'],df['weight']):
        G.add_edge(s,t,weight=w)
    measures = [nx.pagerank(G),nx.betweenness_centrality(G, weight='weight'), nx.degree_centrality(G)]

    cor = pd.DataFrame.from_records(measures)

#Final Conclusion#
'''
Eddard Stark is the most important person as it die by book5
because degree of centrality is high in Eddard Stark
'''