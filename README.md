# Análisis de Sarcasmo en Comentarios de YouTube

## Equipo
**Los Trastornados**

- González Hernández Diego  
- Junco Martínez Bruno Salvador  
- Miranda Ferreyra Uriel  
- Santiago Illoldi Francisco Javier  
- Valdez García Paola Sarai  

---

## Descripción
Este proyecto consiste en el desarrollo de un sistema capaz de detectar automáticamente si un comentario contiene sarcasmo o no, utilizando técnicas de Procesamiento de Lenguaje Natural (NLP) y modelos de aprendizaje automático.

El objetivo principal es mejorar la interpretación del lenguaje en redes sociales, donde el sarcasmo puede alterar el significado real de los comentarios y dificultar su análisis.

---

## Objetivo
Desarrollar e implementar un sistema que permita identificar sarcasmo en texto, comparando diferentes modelos de aprendizaje automático y evaluando su desempeño mediante métricas estándar.

---

## Planteamiento del problema
En plataformas como YouTube, los usuarios suelen utilizar sarcasmo en sus comentarios. Esto representa un reto para los sistemas de análisis de texto, ya que el significado literal no siempre coincide con la intención real del mensaje.

Por ello, este proyecto busca desarrollar un modelo capaz de reconocer patrones de sarcasmo en lenguaje natural.

---

## Metodología

El desarrollo del proyecto se divide en las siguientes etapas:

### 1. Recolección de datos
Se utiliza un dataset de comentarios etiquetados como sarcasmo o no sarcasmo.

### 2. Preprocesamiento de texto
- Conversión a minúsculas  
- Eliminación de caracteres especiales  
- Limpieza de texto  

### 3. Representación del texto
- Bag of Words  
- TF-IDF  
- Similitud de coseno  

### 4. Entrenamiento de modelos
Se entrenan diferentes algoritmos para comparar su rendimiento.

---

## Modelos utilizados

- Naive Bayes  
- SVM (Support Vector Machine)  
- KNN (K-Nearest Neighbors)  
- Perceptrón Multicapa (MLPClassifier)  

---

## Evaluación del modelo

Para medir el rendimiento de los modelos se utilizan las siguientes métricas:

- Accuracy  
- Precision  
- Recall  
- F1-score  
- Matriz de confusión  

---

## Implementación

Se desarrolla una interfaz sencilla, donde el usuario puede ingresar un comentario y el sistema predice si contiene sarcasmo o no.

---

