"""Este documento trata de leer un archivo de texto y narrarlo con voz"""

import pyttsx3
import PyPDF2

# Ruta para el archivo a probar
archivo = r"C:\Repositorios GitHub\Curriculum-Carlos\Sin Inteligencia Artificial\Lector_Voz_Texto\HOLODOMOR 1932.pdf"

# Abre el archivo PDF y lo lee
try:
    pdf_file = open(archivo, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    paginas = len(pdf_reader.pages)
except FileNotFoundError:
    print("El archivo no fue encontrado.")
    exit()

# Inicialización del motor de voz
def inicializar_voz(pagina):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Establecer la voz (asegúrate de que el índice es válido)
    engine.setProperty('voice', voices[0].id)  # Cambia el índice si quieres otra voz; 0 = español, 1 = inglés
    
    # Ajuste de la velocidad de lectura
    engine.setProperty('rate', 200)  # Puedes ajustar la velocidad, aumentar el numero aumenta la velocidad
    
    # Inicia la lectura del input que recibe en página
    engine.say(pagina)
    engine.runAndWait()

# Bucle para leer cada página del PDF
for page in range(paginas):
    page_obj = pdf_reader.pages[page]
    texto = page_obj.extract_text()
    
    if texto:  # Solo si se extrajo texto
        print(f"Página {page + 1}")
        inicializar_voz(texto)

# Cierra el archivo PDF después de leerlo
pdf_file.close()
