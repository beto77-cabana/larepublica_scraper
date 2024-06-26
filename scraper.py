import requests
import lxml.html as html   #para convertir un archivo de texto de html, a un archivo especial que se puede aplicar xpath

import os       # lo vamos a utilizar para crear una carpeta con la fecha de hoy
import datetime # modulo para traer la fecha de hoy

#CONTANTES de links
HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="V_Img_Title"]/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

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
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:               #manejador contextual si el archivo se cierra mantiene todo seguro
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
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

            for link in links_to_notices:                           #Para cada link de noticia
                parse_notice(link, today)                           #funcion que extraera para cada link titulo resumen y cuerpo y lo guardara usando la fecha de hoy

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