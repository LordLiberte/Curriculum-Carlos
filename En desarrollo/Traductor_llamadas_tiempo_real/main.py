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
        md.audio_texto()  # Llamada a la función en modules_pr
    else:
        break
