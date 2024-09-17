"""Este documento trata de leer un archivo de texto y narrarlo con voz"""

import pyttsx3
import PyPDF2
import os

archivo = "C:\Repositorios GitHub\Curriculum-Carlos\En desarrollo\Lector_Voz_Texto\Informe.pdf"

# inicialización de voz
def inicializar_voz(texto):
    
    id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'
    engine = pyttsx3.init()
    engine.setProperty('voices', id1)
    
    engine.say(texto)
    engine.runAndWait()
    
def read_pdf(archivo):
    pdf_file = open(archivo, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    page_obj = pdf_reader.pages[0]
    texto = page_obj.extract_text()
    return texto

texto_leer = read_pdf(archivo)
inicializar_voz(texto_leer)
    
