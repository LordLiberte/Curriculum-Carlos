"""Este documento contiene las funcionalidades y librerias del programa main.py"""

import pyttsx3
import speech_recognition as sr

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
