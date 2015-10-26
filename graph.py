#Graph 
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Read the big table
tablota=pd.read_csv("tablota1.csv", sep=',')
likes1=pd.read_csv("likes_oli.csv", sep=',',header=None)
likes2=pd.read_csv("likes_akram.csv", sep=',',header=None)

likes1.columns=['URL','Likes','Shares']
likes1=likes1[likes1.URL!='URL']

likes2.columns=['URL','Likes','Shares']
likes2=likes2[likes2.URL!='URL']

likes=pd.concat([likes1,likes2])

#Reindex
likes=likes.reset_index(drop=True)
tablota=tablota.reset_index(drop=True)

url=likes.URL[1]

likes=likes[np.array([type(url1)==type(url) for url1 in likes.URL])]
tablota=tablota[np.array([type(url1)==type(url) for url1 in tablota.url_statement])]


#Function that extract the URL
def domain(url):
	split=url.split("/")
	return split[2]

#Create the domains
likes["domain"]=map(domain,likes.URL)

tablota["domain_statement"]=map(domain,tablota.url_statement)
tablota["domain_duplicates"]=map(domain,tablota.url_duplicates)


#Filter
tablota=tablota[tablota.counts>=3]

#Sacamos las sumas de los 
tablota=tablota[tablota.columns[range(4,6)]]
likes=likes[likes.columns[range(1,4)]]

#csv

likes.to_csv("likes.csv",index=False)
tablota.to_csv("duplicates.csv",index=False)

likes.groupby('domain')['Shares','Likes']
