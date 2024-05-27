import requests
import lxml.html as html

url = 'https://www.infobae.com/economia/2024/05/13/creditos-uva-uno-de-los-bancos-privados-mas-grandes-del-pais-se-sumo-a-la-oferta-de-prestamos-hipotecarios/'
response = requests.get(url)
parsed = html.fromstring(response.content)
#paragraphs = parsed.xpath('//div[@class="body-article"]/*')
paragraphs = parsed.xpath('//p[@class="paragraph"] | //ul[@class="list"]')
for p in paragraphs:
    text = p.xpath('string()')
    print(text)