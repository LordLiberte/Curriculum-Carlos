"""Este documento trata de leer un archivo de texto y narrarlo con voz"""

import pyttsx3
import PyPDF2

archivo = "C:\Repositorios GitHub\Curriculum-Carlos\En desarrollo\Lector_Voz_Texto\Informe.pdf"

pdf_file = open(archivo, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
paginas = len(pdf_reader.pages)
lista_paginas = list(range(0,paginas+1))

# inicialización de voz
def inicializar_voz(pagina):
    
    id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'
    engine = pyttsx3.init()
    engine.setProperty('voices', id1)
    newVoiceRate = 700
    engine.setProperty('rate',newVoiceRate)
    
    engine.say(pagina)
    engine.runAndWait()

for page in lista_paginas:
    page_obj = pdf_reader.pages[page]
    texto = page_obj.extract_text()
    print(f"Pagina {page}")
    inicializar_voz(texto)
