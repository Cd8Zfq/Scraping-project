from splinter import Browser
import selenium
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import matplotlib.pyplot as plt
import time
import string
import random

navigateur=Browser("chrome")
def rafraichir():
    navigateur.reload()
def fermer_popup():
    if navigateur.is_element_present_by_css('div[aria-label="Fermer"]', wait_time=10):
        navigateur.find_by_css('div[aria-label="Fermer"]').first.click()
    
def nettoyer_indesirables(texte,liste):
    for offre in liste:
        if texte in offre["Nom"].lower():
            liste.remove(offre)
    return liste
url_base="https://web.facebook.com/marketplace/marrakesh/search?"
prix_min=800
nom_pc="laptop"
url=f"minPrice={prix_min}&query={nom_pc}"
full_url=url_base+url
navigateur.visit(full_url)
fermer_popup()
print("Début de la pause")
time.sleep(40)
print("Fin de la pause")
nb_descente=4
for _ in range(nb_descente):
    navigateur.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.randint(2,10))
html=navigateur.html
soupe_html=soup(html,'html.parser')
navigateur.quit()
liste_noms_div=soupe_html('img',class_="xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3")
liste_noms=[nom.get('alt') for nom in liste_noms_div]
liste_prix_div=soupe_html.find_all('span',class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u")
liste_prix_raw=[prix.text.strip() for prix in liste_prix_div]
liste_liens_div=soupe_html('a',class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1s688f x1lku1pv")
liste_liens=[lien.get('href') for lien in liste_liens_div]
liste_prix=[[prix for prix in prix_raw if prix.isnumeric()] for prix_raw in liste_prix_raw]
liste_prix=[''.join(prix) for prix in liste_prix]
liste_dict_offres=[]
min_length=min(len(liste_noms),len(liste_prix),len(liste_liens))
for i in range(min_length):
    dict_offres={}
    dict_offres["Nom"]=liste_noms[i]
    dict_offres["Prix"]=liste_prix[i]
    dict_offres["Lien"]="https://web.facebook.com"+liste_liens[i]
    liste_dict_offres.append(dict_offres)
# Retire les annonces contenant des mots indésirables
#liste_dict_offres=nettoyer_indesirables("pc",liste_dict_offres)
# Create a DataFrame from the list of dictionaries containing offers
offres_pd=pd.DataFrame(liste_dict_offres)
print("z")