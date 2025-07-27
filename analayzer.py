from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import httpx
import base64
from io import BytesIO
from pydantic import BaseModel, Field
from langchain_community.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import TransformChain
from langchain.schema import SystemMessage, HumanMessage
import yt_dlp
from PIL import Image
import requests
import io
import openai
import os

debug = True

def full_analisis(video_url, model="gpt-4o"):
    info = get_video_info(video_url)
    transcript= get_video_transcript(info.get("id"))
    video_content_messages = [
        SystemMessage(content="Actúa como un experto en contenido de YouTube con 15 años de experiencia muy crítico. Analiza la siguiente transcripción de un video junto con su título y, si se proveen, datos adicionales como título y vistas. Extrae conclusiones útiles sobre el enfoque del contenido, su claridad, valor para el público, y posibles oportunidades de mejora. Responde con un resumen del análisis, puntos fuertes, debilidades detectadas, y sugerencias prácticas para mejorar futuros videos."),
        HumanMessage(content=f" titulo:{info.get('title')},autor: {info.get('uploader')}, vistas: {info.get('view_count')}, canal: {info.get('channel_url')} transcripción:{transcript}")
    ]
    llm = ChatOpenAI(model=model, temperature=0)
    response = llm.invoke(video_content_messages)
    content_analysis = response.content

    if debug:
        print("#### content analisis ####")
        print(content_analysis)

    thumb_analysis = thumbnail_analysis(video_url)

    return {"content_analysis": content_analysis, "thumb_analysis": thumb_analysis}


def descargar_imagen(url):
    respuesta = requests.get(url)
    return Image.open(BytesIO(respuesta.content))

def encode_image_to_base64(image: Image.Image, format="JPEG"):
    with io.BytesIO() as output:
        image.convert("RGB").save(output, format=format)
        return base64.b64encode(output.getvalue()).decode("utf-8")

def thumbnail_analysis(video_url, model="gpt-4o"):
    try:
        thumbnail = get_video_info(video_url).get('thumbnail')
        img = descargar_imagen(thumbnail)
        b64_image = encode_image_to_base64(img, format="JPEG")
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": "actúa como un experto en contenido de YouTube con 15 años de experiencia muy crítico. naliza esta miniatura de vídeo de YouTube. ¿Qué transmite visualmente?  Responde con un resumen del análisis, puntos fuertes, debilidades detectadas, y sugerencias prácticas para mejorar futuros videos."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_image}"
                            }
                        }
                    ]
                }
            ]
        )
        if debug:
            print("#### thumbnail analisis ####")
            print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error al enviar la imagen a GPT-4o: {str(e)}")

def thumbnail_analysis_versus(video_url1, video_url2):
    try:
        thumbnail1 = thumbnail_analysis(video_url1)
        thumbnail2 = thumbnail_analysis(video_url2)
        video_content_messages = [
            SystemMessage(content="Actúa como un experto en contenido de YouTube con 15 años de experiencia muy crítico. Compara estas dos criticas miniaturas de vídeo de YouTube. ¿Qué transmite visualmente?  Responde con un resumen del análisis, lista lomejora de la primera imagen, lista lo mejor de al segunda, y detalla las diferencias entre ambas e idica cual es mejor"),
            HumanMessage(content=f"critica miniatura 1: {thumbnail1}, critica miniatura 2: {thumbnail2}")
        ]
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        response = llm.invoke(video_content_messages)
        content_analysis = response.content

        if debug:
            print("#### comparison analisis ####")
            print(content_analysis)

        return  content_analysis

    except Exception as e:
        raise Exception(f"Error al comparar portadas: {str(e)}")

# def descargar_imagen(url):
#     respuesta = requests.get(url)
#     return Image.open(BytesIO(respuesta.content))

def get_video_info(video_url) -> dict:
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "forcejson": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
        if debug:
            datos = {
                "titulo": info.get("title"),
                "autor": info.get("uploader"),
                "descripcion": info.get("description"),
                "fecha_publicacion": info.get("upload_date"),
                "duracion_segundos": info.get("duration"),
                "vistas": info.get("view_count"),
                "canal": info.get("channel_url"),
                "miniatura": info.get("thumbnail"),
                "video_id": info.get("id")
            }
            print(datos)
        return info
    except Exception as e:
       raise  Exception (f"Error al obtener la información del video: {str(e)}")

def get_video_transcript(video_id,preferred_langs=['es', 'en']) -> str:
    try:
        t=YouTubeTranscriptApi().fetch(video_id, languages=['es'])
        text_formater = TextFormatter()
        text = text_formater.format_transcript(t)
        if debug:
            print("#### transcipción ####")
            print(text)
        return text

    except Exception as e:
        raise Exception(f"No se pudo obtener la transcripción: {str(e)}")
