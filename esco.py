import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

# Leer el archivo CSV
df = pd.read_csv('C:/Users/Josvaldes/Documents/Maestria/Austral/2ano/textMining/proyecto/TextMining/RECLAMOS1.csv',encoding='latin-1') 
df.dropna(subset=['problema_id', 'obsitem'], inplace=True)
# Obteniene las columnas donde se concatena varios campos junto con la observacion y el identificador unico del problema
Oitems = df['Concaobsitem'].tolist()
ids = df['problema_id'].tolist()

# Función para realizar stemming en una descripción
stemmer = SnowballStemmer('spanish')
def stem_descripcion(descripcion):
    words = nltk.word_tokenize(descripcion)
    words = [stemmer.stem(word) for word in words if word not in stopwords.words('spanish')]
    return ' '.join(words)

# Aplicar stemming al campo Oitems donde se tiene la observación del reclamo
descripciones_stemmed = [stem_descripcion(desc) for desc in Oitems]

# Leer el problemas nuevo desde el archivo CSV
Reclamo_csv = 'C:/Users/Josvaldes/Documents/Maestria/Austral/2ano/textMining/proyecto/TextMining/testesco.xlsx'  
df_Reclamo = pd.read_excel(Reclamo_csv)

# Obtener la columna de observacion item  del DataFrame
columna_problemas = 'obsitem'  
problemas_nuevos = df_Reclamo[columna_problemas].tolist()

# Crear un vectorizador TF-IDF
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(descripciones_stemmed)

# Crear una lista para almacenar los resultados
resultados = []

# Calcular la similitud coseno y los problemas_id más similares para cada nuevo reclamo
for problema_nuevo in problemas_nuevos:
    # Aplicar stemming al obsitem nuevo
    problema_nuevo_stemmed = stem_descripcion(problema_nuevo.strip())

    # Transformar la descripción de las nuevas observaciones
    problema_nuevo_vector = vectorizer.transform([problema_nuevo_stemmed])

    # Calcular la similitud coseno con nuevos casos y las observaciones existentes
    similarities = cosine_similarity(X, problema_nuevo_vector)

    # Obtener el índice de la descripción más similar
    most_similar_index = np.argmax(similarities)

    # Obtener el problema_id correspondiente a la observación más similar
    most_similar_codigo_AIS = ids[most_similar_index]

    resultados.append((most_similar_codigo_AIS, problema_nuevo.strip()))

# Crear un DataFrame a partir de los resultados
resultado_df = pd.DataFrame(resultados, columns=['problema_id', 'problema_n'])

# Guardar el DataFrame en un archivo CSV
resultado_csv = ('C:/Users/Josvaldes/Documents/Maestria/Austral/2ano/textMining/proyecto/TextMining/testresultado.csv')
resultado_df.to_csv(resultado_csv, index=False,encoding='latin-1')

print('Resultados guardados en:', resultado_csv)


