# -*- coding: utf-8 -*-
"""directinfo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-cJh0axprUdwijWJ0HCRz7uN56ECBfQM
"""

#importing libraries
import bs4
from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup
import requests

#list of links of every article in different pages
links=[]
#list of types of every article 
types=[]
#list of titles of every article in different pages
titles=[]

links_pages=[]
for i in range (2):
  links_pages.append("https://directinfo.webmanagercenter.com/lessentiel/page/"+str(i+1)+"/")

#for every page , we 'll extract the information that we need
for l in links_pages :
  #parses html into a soup data structure to traverse html
  myurl=req(l)
  page_s=soup(myurl.read(),"html.parser")
  myurl.close()
  #searching containers of articles
  containers=page_s.find("div",{"class":"td-transition-content-and-menu td-content-wrap"})
  c=containers.find_all("div",{"class":"td-module-thumb"})
  for container in c:
    #appending urls of every article to links
    links.append(container.find('a')['href'])
    #appending titles to titles
    titles.append(container.find('a')['title'])

#here we'll enter every link , searching for the text of the article
article=[]
for l in links:
  #parses html into a soup data structure to traverse html
  myurl=req(l)
  page_s=soup(myurl.read(),"html.parser")
  myurl.close()
  #searching for the article container 
  article_container=page_s.find("div",{"class":"td-post-content"})
  #in our case we'll concatenate paragraphs to have the full text
  ch=""
  for i in article_container.find_all('p'):
    ch=ch+i.text
  article.append(ch)

# Import pandas to create our dataframe 
import pandas as pd
import numpy as np


df=pd.DataFrame(list(zip(links,titles,article)),columns=['link','title','article'])
df['type']=np.nan

# Create and download the csv file
df.to_csv('directinfos_scraping.csv', index = False)