"Archivo principal donde se desarrolla el programa de traducción de voz"

from dotenv import load_dotenv
import os
import modules_pr as md 

# Cargar variables de entorno
load_dotenv()

# Obtener API_KEY de DeepL
api_key = os.getenv('API_KEY_DeepL')

# Ciclo de entrada
while True:
    iniciar = input("Desea traducir algo por voz? [Si/No] ")
    if iniciar.lower() == "si":  # Uso lower() para evitar problemas con mayúsculas
        texto = md.audio_texto()  # Llamada a la función en modules_pr, guardamos en una variable para poder traducir
        traduccion = md.traducir(texto, api_key)
        md.hablar(traduccion)
    else:
        break
