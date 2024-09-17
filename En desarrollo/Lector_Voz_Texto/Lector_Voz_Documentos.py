"""Este documento trata de leer un archivo de texto y narrarlo con voz"""

# IMPORTACIÓN DE LIBRERIAS ------------
import pyttsx3
import PyPDF2

# ruta para el archivo a probar
archivo = "C:\Repositorios GitHub\Curriculum-Carlos\En desarrollo\Lector_Voz_Texto\Informe.pdf"

# abre el archivo PDF, lo lee, le encuentra el numero de paginas y crea una lista desde 0 hasta el numero de paginas (+1, por ser este numero excluyente)
pdf_file = open(archivo, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
paginas = len(pdf_reader.pages)
lista_paginas = list(range(0,paginas+1))

# inicialización de voz
def inicializar_voz(pagina):
    
    id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'
    # inicializa la voz del lector
    engine = pyttsx3.init()
    engine.setProperty('voices', id1)
    # Para pruebas, se ha añadido la velocidad de lectura
    newVoiceRate = 400
    engine.setProperty('rate',newVoiceRate)
    
    # inicia la lectura del input que recibe en pagina
    engine.say(pagina)
    engine.runAndWait()

# en función del numero de páginas se crea un bucle equivalente a la longitud del archivo, realizando la lectura del texto en cada página
for page in lista_paginas:
    page_obj = pdf_reader.pages[page]
    texto = page_obj.extract_text()
    print(f"Pagina {page}")
    inicializar_voz(texto)
