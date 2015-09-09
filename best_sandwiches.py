from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv
import re
BASE_URL='http://www.chicagomag.com'
url=open('best_sandwiches.txt','r').read()
soup=BeautifulSoup(url,'lxml')
div_class=soup.findAll('div',{"class":"sammy"})

#print div_class
with open("src-best-sandwiches.tsv", "w") as f:
    fieldnames = ("rank", "sandwich", "restaurant", "price",
                    "address", "phone", "website")
    output = csv.writer(f, delimiter="\t")
    output.writerow(fieldnames)
    for link in div_class:
        url=link.a['href']
        if 'http' not in url:
            url=BASE_URL+url
        
        dsoup=BeautifulSoup(urlopen(url).read(),'lxml')
        
        rank= link.text.split()[0]
        S=link.text.split('<br/>')
        sandwich=link.b.text
        restaurant=link.a.text.split('\n')[1].strip()
        print restaurant
        p_class=dsoup.find('p',{"class":"addy"})
        ptext=p_class.text
        ptext=ptext.split(',')   # what if no web address is given
        website=''
        phone=''
        price=''
        address=''
        if len(ptext)!=2:
            website=ptext[-1].strip()
            phone=ptext[-2].strip()
        else:
            phone=ptext[-1].strip()
        for each in ptext[0]:
            if each==' ':
                break
            price+=each
        price=price[0:-1].strip() # last char is '.' so leave it and strip the whitespaces
        address=ptext[0][len(price)+2:].strip()

        rank=re.sub(u"(\u2018|\u2019|\xe8|\xe9)", "'", rank)
        sandwich=re.sub(u"(\u2018|\u2019|\xe8|\xe9)", "'", sandwich)
        restaurant=re.sub(u"(\u2018|\u2019|\xe8|\xe9)", "'",restaurant)
        price=re.sub(u"(\u2018|\u2019|\xe8|\xe9)", "'", price)
        phone=re.sub(u"(\u2018|\u2019|\xe8|\xe9)", "'", phone)
        address=re.sub(u"(\u2018|\u2019|\xe8|\xe9)", "'", address)
        website=re.sub(u"(\u2018|\u2019|xe8|\xe9)", "'", website)
        
        output.writerow([rank, sandwich, restaurant, price,
                         address, phone, website])

print "Done writing file" 
