# EXTRACCION DE 10 LINK DE INFOBAE/ECONOMIA, Y SU TITULO, RESUME, DIRECC DE IMAGEN Y CUERPO
import requests
import lxml.html as html   #para convertir un archivo de texto de html, a un archivo especial que se puede aplicar xpath
import os       # lo vamos a utilizar para crear una carpeta con la fecha de hoy
import datetime # modulo para traer la fecha de hoy

#CONTANTES de links
HOME_URL = 'https://www.infobae.com/economia/'

XPATH_LINK_TO_ARTICLE = '//a[starts-with(@href, "/economia") and @class="headline-link"]/@href'
XPATH_TITLE = '//h1/text()'
XPATH_SUMMARY = '//h2[@class="article-subheadline left "]/text()'
XPATH_BODY = '//p[@class="paragraph"] | //div[@class="headline-wrapper"] | //ul[@class="list"]/li'
XPATH_IMAGE = '//div[@class="visual__image"]/img/@src'

def parse_notice(link, today):                                                           #Recibe link y fecha de hoy
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                title = title.replace('\n', '')
                title = title.replace(':', ' ')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                image = parsed.xpath(XPATH_IMAGE)
                body = parsed.xpath(XPATH_BODY)

            except IndexError:
                return
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:               #manejador contextual si el archivo se cierra mantiene todo seguro
                f.write("Título:\n")
                f.write(title)
                f.write('\n\n')
                f.write("Resumen:\n")
                f.write(summary)
                f.write('\n\n')
                f.write("Imágenes:\n")
                for p in image:
                    text=str(p)
                    image_addres=text[:-5]
                    f.write(image_addres)
                    
                    f.write('\n')
                f.write('\n\n')
                f.write("Cuerpo de la Noticia:\n")
                for p in body:
                    text = p.xpath('string()')
                    f.write(text)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():  #extraer links de las noticias
    try:                                                            #para trabajar de manera segura 
        response = requests.get(HOME_URL)                           #la resp va a ser el doc html y todo lo que involucra a http, por ej las caberas
        if response.status_code == 200:                             #Comienza la logica para traer los links
            home = response.content.decode('utf-8')                 #Devuelve el doc html de la resp, decode es metodo q transforma los caract especiales
            parsed = html.fromstring(home)                          #transforma el doc html a un archivo especial para poder hacer XPath
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')      #
            if not os.path.isdir(today):                            #si no existe una carpeta con la fecha de hoy
                os.mkdir(today)
            cont=0
            for link in links_to_notices:
                                           #Para cada link de noticia
                link='https://www.infobae.com'+link
                parse_notice(link, today)                           #funcion que extraera para cada link titulo resumen y cuerpo y lo guardara usando la fecha de hoy
                cont= cont+1
                if cont==11:
                    break

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():      #funcion ppal que corre cdo se ejecute el archivo
    parse_home()

#DEFINIMOS EL ENTRY POINT DE MI ARCHIVO DE PYTHON 
#dandername doble guion bajo al ppio y final de name
#dandermain

if __name__ == '__main__':
    run()