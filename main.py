from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import os
import re
import emoji

app = FastAPI()

# Modelo de datos para la solicitud
class SarcasmRequest(BaseModel):
    comentario: str
    modelo: str = "Naive Bayes"

# Intentar cargar los modelos
modelos = {}
vectorizer = None
try:
    if os.path.exists("vectorizer.pkl"):
        vectorizer = joblib.load("vectorizer.pkl")
        modelos["Naive Bayes"] = joblib.load("modelo_nb.pkl")
        modelos["SVM"] = joblib.load("modelo_svm.pkl")
        modelos["KNN"] = joblib.load("modelo_knn.pkl")
        modelos["MLP"] = joblib.load("modelo_mlp.pkl")
except Exception as e:
    print("No se encontraron los modelos. Corre la última celda del Notebook.")

# Función sencilla de limpieza idéntica a la del Notebook
def limpiar_texto_basico(texto):
    if not isinstance(texto, str): return ""
    texto = texto.lower()
    emojis_en_texto = [c['emoji'] for c in emoji.emoji_list(texto)]
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto)
    texto = re.sub(r'@\w+', '', texto)
    texto = re.sub(r'[^a-záéíóúñ0-9\s]', '', texto)
    palabras = texto.split() # Stopwords se omiten por rapidez en API
    texto_limpio = " ".join(palabras)
    if emojis_en_texto:
        texto_limpio += "     " + " ".join(emojis_en_texto)
    return texto_limpio.strip()

@app.post("/analizar")
def analizar_sarcasmo(req: SarcasmRequest):
    if not vectorizer or req.modelo not in modelos:
        return {"error": "Modelos no encontrados. Por favor exporta tus modelos en el Jupyter Notebook primero."}
    
    texto_procesado = limpiar_texto_basico(req.comentario)
    if not texto_procesado:
        return {"error": "El comentario está vacío o carece de palabras válidas."}
        
    try:
        vec = vectorizer.transform([texto_procesado])
        modelo_seleccionado = modelos[req.modelo]
        
        # Predecir clase
        pred_class = int(modelo_seleccionado.predict(vec)[0])
        
        # Obtener probabilidades si el modelo las soporta
        prob_sarcasmo = 0.0
        prob_no_sarcasmo = 0.0
        
        if hasattr(modelo_seleccionado, "predict_proba"):
            probs = modelo_seleccionado.predict_proba(vec)[0]
            prob_no_sarcasmo = float(probs[0])
            prob_sarcasmo = float(probs[1])
        else:
            # Para SVM o KNN si no devuelven probs
            prob_sarcasmo = 1.0 if pred_class == 1 else 0.0
            prob_no_sarcasmo = 1.0 if pred_class == 0 else 0.0
            
        return {
            "sarcasmo": bool(pred_class == 1),
            "prob_sarcasmo": prob_sarcasmo,
            "prob_no_sarcasmo": prob_no_sarcasmo,
            "texto_procesado": texto_procesado,
            "modelo_usado": req.modelo
        }
    except Exception as e:
        return {"error": f"Error del servidor: {str(e)}"}

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")
