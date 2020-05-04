#importing libraries
import bs4
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
import time 
import requests 

#links containg links of articles in every page in l
links=[]
types=[]

#Defining the url of the website to scrape(1st page)
uClient = ureq("http://news.tunisiatv.tn/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1")

#parses html into a soup data structure to traverse html
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

#searching containers of articles
containers = page_soup.find_all("div", {"class": "view-content"})
c=containers[2].find_all("div", {"class": "elemArticleThumbs"})
  
#appending  links and types of the articles  of the 1st page ONLY
for i in c:
  
  links.append(i.find("div",{"class":"photo"}).find_all('a')[1]['href'])
  types.append(i.find("div",{"class":"photo"}).find_all('a')[0].text)

#par_text containing the text of all the articles 
par_text=[]
#par_title containing the title of all articles
par_title=[]
#l containg links of pages of news that we'll be scraping
l=[]
i=0

#putting the links of pages in l begining with 2nd page to 25th page:(1st page was treated separetly in the begining)
for j in range (0,25):
  l.append("http://news.tunisiatv.tn/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1?page="+str(j+1))

#Let the webscraping begin!
for k in l :
  uClient = ureq(k)

 # parses html into a soup data structure to traverse html
  page_soup = soup(uClient.read(), "html.parser")
  uClient.close()
  containers = page_soup.find_all("div", {"class": "view-content"})
  #finding the articles of the page
  c=containers[1].find_all("div", {"class": "elemArticleThumbs"})
  #FINALLY appending links and types
  for i in c:
    links.append(i.find("div",{"class":"photo"}).find_all('a')[1]['href'])
    types.append(i.find("div",{"class":"photo"}).find_all('a')[0].text)

i=0

for url in links:
  #geeting every URL in links
  note_resp=requests.get(url)
  if note_resp.status_code== 200: #everything is OKAY
    print('URL #{0}: {1}'.format(i+1,url))
    
  # get HTML from webpage      
  note_html=note_resp.content
 #convert HTML to beautiful soup object
  note_soup=soup(note_html,'lxml')
      #find titles
  note_titles=note_soup.find_all('h1',class_='title1')
      #find pargraphs:
  note_pars=note_soup.find_all('div',class_='field-item even')
      #get text from titiles:
  t1=[t.text for t in note_titles]
      #get text from parag:
  t=[p.text for p in note_pars]
    #append text from each p tag and put it in lists
  par_text.append(t)
  par_title.append(t1)
  i=i+1

#cleaning the text of articles  (deleting extra info)
for i in range(len(par_text)):
  del (par_text[i][1])
par_text

# Import pandas to create our dataframe 
import pandas as pd


df=pd.DataFrame(list(zip(links,par_title,par_text,types)),columns=['links','title','texte','types'])


# Create and download the csv file
df.to_csv('Desktop',encoding='utf-8-sig')


