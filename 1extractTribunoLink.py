#EXTRACCION DE LINK DEL TRIBUNO, DE PRIMER Y SEGUNDO NIVEL
import requests
import lxml.html as html
import os

def extract_links(url, nivel,linked1): 
       response = requests.get(url)
       parsed = html.fromstring(response.content)
       #paragraphs = parsed.xpath('//div[@class="body-article"]/*')
       links_sin_https = parsed.xpath('//a[not(starts-with(@href, "https:")) and starts-with(@href, "/")]/@href')
       links_with_https = parsed.xpath('//a[starts-with(@href, "https://eltribunodejujuy.com/")]/@href')
       links_1=set(["hola","san"])
       links_1.clear()
       for p in links_sin_https:
        links_1.add('https://eltribunodejujuy.com'+p)
       for p in links_with_https:
        links_1.add(p)
       with open(f'linksTribuno/{nivel}.txt', 'a', encoding='utf-8') as f:               #manejador contextual si el archivo se cierra mantiene todo seguro
           for link in links_1:
            if link not in linked1:
               f.write(link)
               f.write('\n')
               linked1.add(link)

url = 'https://eltribunodejujuy.com/'
nivel="nivel1"
linked1=set(["hola","san"])
linked1.clear()
extract_links(url, nivel,linked1)
with open(f'linksTribuno/{nivel}.txt', 'r', encoding='utf-8') as f:
    for linea in f:
        enlace = linea.strip()
        extract_links(enlace, "nivel2", linked1)