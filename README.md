# 🧠 Analizador de Competencia en YouTube

Esta aplicación permite analizar vídeos de YouTube desde tres enfoques clave:

1. **Análisis completo del contenido**
2. **Análisis visual de la miniatura (portada)**
3. **Comparación entre miniaturas**

Funciona mediante Streamlit y utiliza modelos de lenguaje avanzados como GPT-4o, así como la transcripción automática de los vídeos.

---

## ⚙️ Instalación

Clona el repositorio y asegúrate de tener Python 3.9 o superior.

1. Instala las dependencias:

```bash
pip install -r requirements.txt
```

2. Crea un archivo `.env` en la raíz del proyecto con tu clave de OpenAI:

```
OPENAI_API_KEY=tu_clave_aquí
```

---

## 🚀 Cómo usar

Ejecuta la aplicación con Streamlit:

```bash
streamlit run app.py
```

---

## 🎯 Funcionalidades

### 1. 🔍 Análisis completo

Pulsa el botón **"Análisis completo"** tras introducir la URL de un vídeo de YouTube. Esto realiza:

- Extracción de metadatos del vídeo (título, vistas, canal, autor…)
- Transcripción automática (si está disponible)
- Análisis del contenido textual mediante GPT-4o
- Análisis de la miniatura visual del vídeo

El resultado incluye dos secciones:

- **🧠 Análisis de la miniatura**  
- **🤖 Análisis del contenido**

---

### 2. 🖼️ Análisis de miniatura

Pulsa **"Analizar Portada"** para obtener un análisis visual de la miniatura del vídeo.

Este análisis responde a preguntas como:

- ¿Qué transmite visualmente la portada?
- ¿Cuáles son sus puntos fuertes y débiles?
- ¿Cómo podría mejorarse desde una perspectiva profesional de marketing y contenido?

---

### 3. 🆚 Comparar portadas

Pulsa **"Comparar portadas"** y proporciona dos URLs de vídeos distintos. La herramienta:

- Descarga ambas miniaturas
- Analiza visualmente cada una con GPT-4o
- Compara sus puntos fuertes, debilidades y diferencias
- Indica cuál es más efectiva y si son visualmente similares

---

## 📦 Estructura del proyecto

```
.
├── app.py               # Interfaz de Streamlit
├── analayzer.py         # Lógica del análisis
├── requirements.txt     # Dependencias necesarias
└── .env                 # Clave de OpenAI (no se incluye por seguridad)
```

---

## 📄 Licencia

Este proyecto puede usarse y modificarse libremente para fines personales o educativos. Para uso comercial, consulta primero con el autor.
