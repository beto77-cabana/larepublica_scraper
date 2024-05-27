#TRATAMIENTO DE TEXTO DE LAS NOTICAS DE INFOBAE
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from nltk.stem import SnowballStemmer

# Descargar recursos de nltk necesarios
nltk.download('punkt')
nltk.download('stopwords')

# Función para unir todos los textos en un solo documento
def unify_texts(directory):
    full_text = ""
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                full_text += file.read() + " "
    return full_text

# Función para tokenizar y limpiar el texto
def process_text(text):
    stop_words = set(stopwords.words('spanish'))  # Asegúrate de elegir el idioma correcto de tus stop words
    words = word_tokenize(text.lower())
    cleaned_text = [word for word in words if word.isalpha() and word not in stop_words]
    return cleaned_text

# Función para obtener los términos más frecuentes
def get_most_common_terms(text, num_terms=100):
    count = Counter(text)
    return count.most_common(num_terms)

# Función para aplicar stemming
def stem_text(words):
    # Stemming con SnowballStemmer para español
    stemmer = SnowballStemmer('spanish')
    stemmed_words = [stemmer.stem(word) for word in words]
    return stemmed_words

# Usar las funciones definidas
directory = 'H:/larepublica_scraper/14-05-2024'  # Folder with text files
unified_text = unify_texts(directory)
processed_text = process_text(unified_text)
most_common_terms = get_most_common_terms(processed_text)

# Aplicar stemming
stemmed_text = stem_text(processed_text)
most_common_stemmed_terms = get_most_common_terms(stemmed_text)

# Mostrar resultado palabras comunes
print("{0:30}{1:30}".format("PALABRAS","Frecuencia"))
print("-"*40)
for word, frequency in most_common_terms:
    print("{0:20}{1:20}".format(word, frequency))

# Mostrar resultado Stemming mas comunes
print("{0:30}{1:30}".format("Stemming","Frecuencia"))
print("-"*40)

for word, frequency in most_common_stemmed_terms:
    print("{0:20}{1:20}".format(word, frequency))