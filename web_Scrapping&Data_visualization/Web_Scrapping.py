import locale
import pandas as pd
from scrapy import Selector
import requests

L=[0]*7
site='https://www.babelio.com'
url1='https://www.babelio.com/decouvrir.php'
html1=requests.get(url1).content
sel1=Selector(text=html1)
locale.setlocale(locale.LC_ALL, 'nl_NL')
a='//*[@id="page_corps"]/div/div[4]/div[4]/div[*]/a/@href'
urrl=sel1.xpath(a).extract()
for i in range(4,len(urrl)-1):
    html2=requests.get(site+urrl[i]).content
    sel2=Selector(text=html2)
    u=sel2.xpath('//*[@id="page_corps"]/div[1]/div[5]/a/@href').extract()
    url3=site+u[0]
    html3=requests.get(url3).content
    sel3=Selector(text=html3)
    dd='//*[@id="page"]/div[2]/div[*]/a[1]/h2/text()'
    Title=sel3.xpath(dd).extract()
    f='//*[@id="page"]/div[2]/div[*]/a[2]/h3/text()'
    Author=sel3.xpath(f).extract()
    refpath='//*[@id="page"]/div[2]/div[*]/a[1]/@href'
    refRating=sel3.xpath(refpath).extract()
    Rating=[]
    Note=[]
    cpt=0
    for j in range(len(refRating)):
        url4=site+refRating[j]
        html4=requests.get(url4).content
        sel4=Selector(text=html4)
        q='//*[@id="histogramme"]/div[1]/div[1]/text()'
        q1=sel4.xpath(q).extract()
        q2=sel4.xpath('//*[@id="page_corps"]/div/div[3]/div[2]/div[1]/div[2]/span[3]/a/span/text()').extract()
        if len(q1)==0 or len(q2)==0 :
            Title.pop(j-cpt)
            Author.pop(j-cpt)
            cpt+=1



        else:
            try:
                Note.append(int(q2[0]))
                Rating.append(locale.atof(q1[0].strip()))
            except:

                Title.pop(j-cpt)
                Author.pop(j-cpt)
                cpt+=1

    L[i-4]={'Title':Title,'Author':Author,'Rating':Rating,'Note':Note}

thriller=pd.DataFrame(L[0])
bdessiné=pd.DataFrame(L[1])
manga=pd.DataFrame(L[2])
jeunesse=pd.DataFrame(L[3])
jeuneadlt=pd.DataFrame(L[4])
imaginaire=pd.DataFrame(L[5])
amour=pd.DataFrame(L[6])

#conctaner tous les datframes en un seul
import matplotlib.pyplot as plt
N=[thriller,bdessiné,jeuneadlt,imaginaire,amour]
M=[['thriller'],['bdessiné'],['jeuneadlt'],['imaginaire'],['amour']]
i=0
for frame in N:
    frame['genre']=M[i]*len(frame)
    i=i+1
thriller
books=pd.concat(N)
#conctaner tous les datframes en un seul
import matplotlib.pyplot as plt
N=[thriller,bdessiné,jeuneadlt,imaginaire,amour]
M=[['thriller'],['bdessiné'],['jeuneadlt'],['imaginaire'],['amour']]
i=0
for frame in N:
    frame['genre']=M[i]*len(frame)
    i=i+1
thriller
books=pd.concat(N)
books
#tracer la distribution du rating pour chaque categorie
genre=books['genre'].tolist()
rate1=books['Rating'].tolist()
plt.scatter(genre,rate1)
pd.set_option('display.max_rows', None)
#classer les livres en se basant sur la note
books.sort_values('Note',ascending=False)
#tracer la distribution du new rating pour chaque categorie
books['NewRating']=books['Rating']*books['Note']/271
rate2=books['NewRating'].tolist()
plt.scatter(genre,rate2)
