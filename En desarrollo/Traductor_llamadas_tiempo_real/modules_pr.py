"""Este documento contiene las funcionalidades y librerias del programa main.py"""

import pyttsx3
import speech_recognition as sr
import deepl

# función para el reconocimiento de la voz y su transformación a texto
def audio_texto():
    recogn = sr.Recognizer()
    
    with sr.Microphone() as source:
        recogn.pause_threshold = 0.5
        print('Ya puedes hablar')
        audio = recogn.listen(source)
        
        try:
            order = recogn.recognize_google(audio, language='es')
        except sr.UnknownValueError:
            print("Ups, no entendí")
            return "sigo esperando"
        except sr.RequestError:
            print("Ups, no hay servicio")
            return "sigo esperando"
        except Exception as e:  # Captura errores inesperados
            print(f"Ups, algo ha salido mal: {e}")
            return "sigo esperando"
        else:
            print("Dijiste: " + order)
            return order

# función para la traducción del mensaje enviado
def traducir(texto, api_key, idioma_destino="EN-US"):
    translator = deepl.Translator(api_key) # traductor
    try:
        resultado = translator.translate_text(texto, target_lang=idioma_destino) # traducción
        return resultado.text
    except deepl.DeepLException as error:
        print(f"Error al traducir: {error}")
        return None

# función para hablar, comentar texto suministrado
def hablar(texto):
    
    engine = pyttsx3.init()  # motor de voz
    id1 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
    voices = engine.getProperty('voices')
    engine.setProperty('voices', id1)
    engine.setProperty('rate', 150)
    # pronunciar mensaje
    engine.say(texto)  # mensaje a decir
    engine.runAndWait()
