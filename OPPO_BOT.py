import json 
import time
from bs4 import BeautifulSoup
import requests 

#This code we help to extract smartphones informations from the official OPPO website to use it to build a chatbot 

time.sleep(2)
#Extract Information
website = requests.get('https://www.oppo.com/tn/smartphones/')
soup = BeautifulSoup(website.text, 'html.parser')

time.sleep(2)
#extract smartphones names
findnames = soup.findAll('div',class_='title')
Names = []
for name in findnames:
    if(len(name.text) > 0):
        Names.append(name.text)

time.sleep(3)
#Get images urls for each smartphone
for name in Names:
    findimages = soup.findAll('img',alt=name)
    img_sources = [a.get('data-src') for a in findimages]

#
#Now we have names of smartphones and links of theirs images
#


#For each image w try to press "découvrir" boutton to show more information about that smartphones
time.sleep(3)
plus_url = []
findbtn = soup.findAll('span',class_='learn-more btn')
for btn in findbtn:
    btn = btn.find('a')
    url = btn.get('href')
    plus_url.append(url)

parts = ['size','memory','display','camera','video','battery','biometrics','chips','sensors','network','connectivity','system','position','box']
parts_fr = ['taille', 'memoire', 'affichage', 'appareil photo', 'video', 'batterie', 'biometrie', 'puces', 'capteurs', 'reseau', 'connectivite', 'systeme' , 'position', 'boite']

#for each url of smartphone we will visit it and try to extract useful information
time.sleep(3)
caracs = []
for ur in plus_url:
    
    name = ur.split('/')[-2]
    if '-' in name:
        name = name.replace('-',' ')
    
    ur = ur + 'specs/'
    website1 = requests.get(ur)
    soup1 = BeautifulSoup(website1.text, 'html.parser')
    
    time.sleep(3)
    for k in range(len(parts)):
        carac = dict()
        #tag
        tag = name + ' ' + parts[k]
        tag_l = []
        tag_l.append(tag)
        #pattern
        pattern = 'Quelles sont les caractéristiques de ' + parts_fr[k] + ' de ' + name + ' ?'
        pat_l = []
        pat_l.append(pattern)
        #context
        context = [""]
        #responses
        resp = []
        c1 = soup1.findAll('section',class_ = parts[k])
        for elt in c1:
            dv = elt.findAll('span',class_ = 'desc')
            for sp in dv:
                resp.append(sp.text)

        #collect_data
        carac['tag'] = tag_l
        carac['patterns'] = pat_l
        carac['responses'] = resp
        carac['context'] = context
        #Append to list total        
        caracs.append(carac)
        
    time.sleep(3)

fich = dict()
fich['intents'] = caracs

#Now , we will convert this list of lists into json file to use it in the creation of the chatbot
with open("C:/Users/hp/Desktop/OPPO_BOT/intents.json", "w" ,encoding='ascii') as file:
    json.dump(fich, file)

file.close()


