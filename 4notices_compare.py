#CUALES SON LAS 2 NOTICIAS MAS PARECIDAS
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Descargar recursos de nltk necesarios
nltk.download('punkt')
nltk.download('stopwords')

# Función para leer los textos de las noticias
def read_texts(directory):
    texts = []
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                texts.append(file.read())
                filenames.append(filename)
    return texts, filenames

# Función para tokenizar y limpiar el texto
def process_text(text):
    stop_words = set(stopwords.words('spanish'))
    words = word_tokenize(text.lower())
    cleaned_text = [word for word in words if word.isalpha() and word not in stop_words]
    return ' '.join(cleaned_text)

# Función para encontrar noticias similares
def find_similar_articles(texts, filenames):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    similar_articles = []
    for idx, similarities in enumerate(similarity_matrix):
        for similar_idx, sim_score in enumerate(similarities):
            if idx != similar_idx:  # Evitar comparar con sí mismo
                similar_articles.append((filenames[idx], filenames[similar_idx], sim_score))
    
    return similar_articles

# Directorio con los archivos de texto de las noticias
#directory = 'H:/larepublica_scraper/15-05-2024'    #AQUI SE INDICA LA CARPETA DE LOS ARCHIVOS A COMPARAR
directory = 'H:/larepublica_scraper/compara'

# Leer y procesar los textos de las noticias
texts, filenames = read_texts(directory)
processed_texts = [process_text(text) for text in texts]

# Encontrar artículos similares
similar_articles = find_similar_articles(processed_texts, filenames)

# Imprimir artículos similares
print("{0:40}{1:40}{2:10}".format("Noticia", "Noticia Similar", "Similitud"))
print("-" * 90)
max_score_index = None
max_score = -1
for idx, (article1, article2, score) in enumerate(similar_articles):
    print("{0:40}{1:40}{2:.2f}".format(article1, article2, score))
    if score > max_score:
        max_score = score
        max_score_index = idx

if max_score_index is not None:
    print("\nÍndice con el puntaje más alto:", max_score_index)
    print("Artículo 1:", similar_articles[max_score_index][0])
    print("Artículo 2:", similar_articles[max_score_index][1])
    print("Similitud:", similar_articles[max_score_index][2])
else:
    print("No se encontraron similitudes.")