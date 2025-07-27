import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import yt_dlp
from click import style

import analayzer
from dotenv import load_dotenv


load_dotenv()



def comparar_imagenes(img1, img2):
    return img1.resize((256, 256)).tobytes() == img2.resize((256, 256)).tobytes()

result = ""
if "comparacion" not in st.session_state:
    st.session_state.comparacion = False
    st.session_state.full_result = False
    st.session_state.loader= False
    st.session_state.portada = False

st.title("Analizador de Miniaturas de YouTube")

url = st.text_input("Introduce la URL del vídeo de YouTube")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Analisis completo"):
        st.session_state.loader = True
        if url:
            result = analayzer.full_analisis(url)
            st.session_state.full_result = True
            st.session_state.loader = False
        else:
            st.error("Por favor, introduce una URL válida de YouTube")
with col2:
    if st.button("Analizar Portada"):
        if url:
            miniatura_url = miniatura_url = analayzer.get_video_info(url).get("thumbnail")
            imagen = analayzer.descargar_imagen(miniatura_url)
            result = analayzer.thumbnail_analysis(url)
            st.session_state.portada = True
            st.image(imagen, caption="Miniatura del vídeo", use_container_width=True)
        else:
            st.error("Por favor, introduce una URL válida de YouTube")

with col3:
    if st.button("Comparar portadas"):
        if url:
            st.session_state.mostrar_comparacion = True
        else:
            st.error("Por favor, introduce una URL válida de YouTube")

if not result and st.session_state.loader:
    st.write("Analizando...")
    html_code="""
<style> .loader {
  height: 15px;
  aspect-ratio: 5;
  display: grid;
  --_g: no-repeat radial-gradient(farthest-side,#fff 94%,#fff);
}
.loader:before,
.loader:after {
  content: "";
  grid-area: 1/1;
  background:
    var(--_g) left,
    var(--_g) right;
  background-size: 20% 100%;
  animation: l32 1s infinite; 
}
.loader:after { 
  background:
    var(--_g) calc(1*100%/3),
    var(--_g) calc(2*100%/3);
  background-size: 20% 100%;
  animation-direction: reverse;
}
@keyframes l32 {

  80%,100% {transform:rotate(.5turn)}
}
</style>

<div style="display: flex; justify-content: center; align-items: center; height: 10vh;">
  <div class="loader"></div>
</div>
"""
    st.markdown(html_code, unsafe_allow_html=True)


if st.session_state.comparacion and url:
    miniatura_url = analayzer.get_video_info(url).get("thumbnail")
    imagen1 = analayzer.descargar_imagen(miniatura_url)
    comparacion = st.text_input("Introduce la URL del vídeo de YouTube")
    ejecutar = st.button("Comparar")
    if comparacion:
        miniatura_url = analayzer.get_video_info(comparacion).get("thumbnail")
        imagen2 = analayzer.descargar_imagen(miniatura_url)
        st.image([imagen1, imagen2], caption=["Miniatura", "Imagen subida"], width=300)
        result = analayzer.thumbnail_analysis_versus(url)
        if ejecutar:
            iguales = comparar_imagenes(imagen1, imagen2)
            if iguales:
                st.success("Las imágenes son iguales (visualmente muy parecidas)")
            else:
                st.warning("Las imágenes son diferentes")


if result:
    if st.session_state.full_result:
        st.subheader("🧠 Análisis de la miniatura")
        st.write(result.get("thumb_analysis"))
        st.subheader("🤖 Análisis del contenido")
        st.write(result.get("content_analysis"))

    elif  st.session_state.portada:
        st.subheader("🧠 Análisis de la miniatura")
        st.write(result)
    elif st.session_state.comparacion:
        st.subheader("🧠 Análisis de la comparación")
        st.write(result)