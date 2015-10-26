
#Script to find duplicates in python using the urlparse library
import urllib2
from urllib2 import urlopen
import hashlib
from bs4 import BeautifulSoup
import pprint
import unicodedata
import csv
from py_bing_search import PyBingSearch
import pandas as pd
import numpy as np
from random import randint
from collections import Counter

#url1='http://peacefulwarriors.net/can-gmos-help-feed-the-world/'
#url2='http://www.greenmedinfo.com/blog/can-gmos-help-feed-world'

#URL's to look in 
urls1=pd.read_csv("crawl-oli.csv", sep=',',header=None)
urls2=pd.read_csv("crawl-akram.csv", sep=',',header=None)

#We get the values
urls1=urls1[0].values
urls1=urls1[1:(len(urls1)-1)]
urls1=list(urls1)
urls2=urls2[0].values
urls2=urls2[1:(len(urls2)-1)]
urls2=list(urls2)

#Concatanate the two lists
urls=urls1+urls2

#Useful
def txt_md5(txt):
    return hashlib.md5(txt).hexdigest()

MAX_FILE_SIZE=1024*1024*1024 

def cut(str):
	strsplit=str.split()
	return " ".join(strsplit[0:min(len(strsplit)-1,20)])

#Function to get 5 random statements of each url
def rand_statements(url):
	req=urllib2.Request(url,headers={'User-Agent' : "Magic Browser"})
	c=urllib2.urlopen(req)
	r=c.read(MAX_FILE_SIZE)
	soup=BeautifulSoup(r)
	body=soup.find('body').text 
	body=unicodedata.normalize('NFKD', body).encode('ascii','ignore')
	body=body.splitlines()
	body=[i for i in body if i!='']
	body=[x for x in body if len(x)>70]
	body=map(cut,body)
	if len(body)<5:
		indexes=range(0,len(body))
	else:
		indexes=[randint(0,len(body)-1) for i in range(0,5)]
	return ['"'+body[i]+'"' for i in indexes]

#Now the request
bing = PyBingSearch('1lQ7z/Ye5Qo/vuWoEuznwGUDQX841pfEkLC77SBTNCs')


#Function 
def request_urls(url):
	statements=rand_statements(url)
	list_duplicates=[]
	for statement in statements:
		result_list, next_uri = bing.search(statement, limit=50,format='json')
		results=[unicodedata.normalize('NFKD',result_list[i].url).encode('ascii','ignore') for i in range(0,len(result_list))]
		list_duplicates=list_duplicates+results
	#Get the frequencies of each url we get
	return Counter(list_duplicates).most_common()

#We run for all the urls
final_list=[]
for url in urls:
	try: 
		duplicates=request_urls(url)
		duplicates=[duplicate+(url,) for duplicate in duplicates]
		#convert to pandas dataframe
		duplicates=pd.DataFrame(duplicates, columns=['url_statement', 'counts', 'url_duplicates'])
		final_list=final_list+[duplicates]
	except:
		'This url '+url+' has cookies permissions fucked up'
		
#we put the list in a big ass dataframe
tablota=pd.concat(final_list)
tablota.to_csv("tablota1.csv")


