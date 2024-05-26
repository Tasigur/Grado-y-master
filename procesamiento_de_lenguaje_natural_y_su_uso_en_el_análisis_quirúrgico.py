# -*- coding: utf-8 -*-
"""PROCESAMIENTO DE LENGUAJE NATURAL  Y SU USO EN EL ANÁLISIS QUIRÚRGICO.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/147h_E49M2j6asVY4G69qkTy8-56MWfq2
"""

import pandas as pd
import numpy as np
import seaborn as sns
import scipy
import matplotlib
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import re
import string
from scipy import stats as ss

data = pd.read_csv("ARCHIVOLABEL.csv")
data.head()
col_name=list(data.columns)
data.columns = ['infeccion', 'ID',"texto"]

plt.hist(data["infeccion"])

data["infeccion"].value_counts()

"""Como podemos comprobar en las dos celdas anteriores, las clases se encuentran completamente desbalanceadas.

## Preprocesado

Para eliminar los signos de puntuación, las tildes y los caracteres distintos a ASCII, implementamos las siguientes tres funciones:
"""

def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?¿\]\%', ' ', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub('\w*\d\w*', '', text)
    return text
def clean_text_round2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = re.sub('[‘’“”…«»]', '', text)
    text = re.sub('\n', ' ', text)
    return text
def eliminar_tilde(text):
    text=text.replace("á","a")
    text=text.replace("é","e")
    text=text.replace("í","i")
    text=text.replace("ó","o")
    text=text.replace("ú","u")
    return text

for k in range(0,len(data['texto'])):
    clean1=clean_text_round1(data['texto'][k])
    clean2=clean_text_round2(clean1)
    data['texto'][k]=eliminar_tilde(clean2)

"""Posteriormente, tokenizamos nuestro texto y mostramos en pantalla algunos ejemplos de "stopwords" para el castellano y las palabras que con mayor frecuencia se repiten en nuestro conjunto de datos:"""

import nltk
nltk.download('punkt')
nltk.download('stopwords')
print("")
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


texto = data.texto.str.cat(sep=' ')

#function to split text into word
tokens = word_tokenize(texto)

vocabulary = set(tokens)
print("Cantidad de palabras distintas: ", len(vocabulary))


stop_words = set(stopwords.words('spanish'))
print("Ejemplos de stopwords:", list(stop_words)[0:10])
tokens = [w for w in tokens if not w in stop_words]
frequency_dist = nltk.FreqDist(tokens)
print("Diez palabras con mayor frecuencia: ", sorted(frequency_dist,key=frequency_dist.__getitem__, reverse=True)[0:10])

"""## Implementación de modelos

Aquí tomamos como variable de salida (y) los datos recogidos en la columna "infeccion" y como variable de entrada (x) los datos recogidos en la columna "texto".

Importamos todas las funciones que necesitaremos para la implementación de estos modelos.
"""

X=data["texto"]
y=data["infeccion"]

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from imblearn.over_sampling import SMOTE

"""### Sin oversampling

Pasamos a crear los modelos sin emplear oversampling. En primer lugar crearemos un modelo Multinomial y en segundo lugar crearemos un modelo SGD (descenso por gradiente estocástico).
"""

#MODELO MULTINOMIAL SIN SMOTE
for k in range(5):
  print("Prueba ", k+1)
  print("")

  X_train, X_test, y_train, y_test = train_test_split(
    X, y,stratify=y, test_size=0.35, random_state=k)

  vectorizer = TfidfVectorizer()
  train_vectors = vectorizer.fit_transform(X_train)
  test_vectors = vectorizer.transform(X_test)

  clf =  MultinomialNB().fit(train_vectors, y_train)
  predicted = clf.predict(test_vectors)

  print(accuracy_score(y_test,predicted))
  print(confusion_matrix(y_test,predicted))
  print(classification_report(y_test,predicted))

#MODELO SGD SIN SMOTE
for k in range(5):
  print("Prueba ", k+1)
  print("")

  X_train, X_test, y_train, y_test = train_test_split(
    X, y,stratify=y, test_size=0.35, random_state=k)

  vectorizer = TfidfVectorizer()
  train_vectors = vectorizer.fit_transform(X_train)
  test_vectors = vectorizer.transform(X_test)

  clf =  SGDClassifier().fit(train_vectors, y_train)
  predicted = clf.predict(test_vectors)

  print(accuracy_score(y_test,predicted))
  print(confusion_matrix(y_test,predicted))
  print(classification_report(y_test,predicted))

"""### Con oversampling

Dado que tenemos un conjunto de datos muy desbalanceado, siento el 86% de la clase "no infección quirúrgica" y solo el 14% de la clase "infección quirúrgica", aplicaremos oversampling para igualar la cantidad de muestras de una clase y otra en el conjunto de train. Esto permitirá a nuestro modelo aprender de la misma forma a clasificar ambas clases.

Repetimos el proceso seguido anteriormente, crearemos un modelo Multinomial y otro modelo SGD.
"""

#MODELO MULTINOMIAL CON SMOTE
for k in range(5):
  print("Prueba ", k+1)
  print("")

  X_train, X_test, y_train, y_test = train_test_split(
    X, y,stratify=y, test_size=0.35, random_state=k)

  vectorizer = TfidfVectorizer()
  train_vectors = vectorizer.fit_transform(X_train)
  test_vectors = vectorizer.transform(X_test)

  X_resample, y_resampled = SMOTE().fit_resample(train_vectors, y_train)

  clf =  MultinomialNB().fit(X_resample, y_resampled)
  predicted = clf.predict(test_vectors)

  print(accuracy_score(y_test,predicted))
  print(confusion_matrix(y_test,predicted))
  print(classification_report(y_test,predicted))

#MODELO SGD CON SMOTE
for k in range(5):
  print("Prueba ", k+1)
  print("")

  X_train, X_test, y_train, y_test = train_test_split(
    X, y,stratify=y, test_size=0.35, random_state=k)

  vectorizer = TfidfVectorizer()
  train_vectors = vectorizer.fit_transform(X_train)
  test_vectors = vectorizer.transform(X_test)

  X_resample, y_resampled = SMOTE().fit_resample(train_vectors, y_train)

  clf =  SGDClassifier().fit(X_resample, y_resampled)
  predicted = clf.predict(test_vectors)

  print(accuracy_score(y_test,predicted))
  print(confusion_matrix(y_test,predicted))
  print(classification_report(y_test,predicted))

"""## Conclusión

Hemos creado un algoritmo predictor, que a partir de texto libre es capaz de determinar si un paciente tiene o no infección en el sitio quirúrgico.

A pesar de las pocas muestras, y muy desbalanceadas, con las que hemos trabajado, los resultados finales y las prestaciones de los modelos son muy buenas. Lo cual, nos hace pensar que mejorando obteniendo un volumen de datos mayor, balanceados y de mejor calidad, este proyecto podría llevarse acabo y ser de gran utilidad en un entorno de la realidad del hospital.
"""

