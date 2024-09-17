"""Este documento trata de leer un archivo de texto y narrarlo con voz"""

import pyttsx3
import ocrmypdf
import os

ruta = os.getcwd()
archivo = "\Lector_Voz_Texto\Informe.pdf"
ruta_archivo = ruta + archivo

# inicialización de voz
def inicializar_voz(texto):
    
    id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'
    engine = pyttsx3.init()
    engine.setProperty('voices', id1)
    
    engine.say(texto)
    engine.runAndWait()

def ocr_texto(documento):
    global ruta
    input_pdf = documento
    output_pdf = ruta + "\\Lector_Voz_Texto\\Informe2.pdf"
    ocrmypdf.ocr(input_pdf, output_pdf, language='spa', optimize=3)

ocr_texto(ruta_archivo)
