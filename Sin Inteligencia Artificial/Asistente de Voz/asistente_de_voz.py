import pyttsx3
import speech_recognition as sr
import pywhatkit
import pyjokes
import webbrowser
import datetime
import wikipedia
import os

# opciones de voz/idioma
id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'


# escuchar nuestro microfono y devolver audio como texto
def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as source:

        # tiempo de espera
        r.pause_threshold = 0.5

        # informar comienzo de grabación
        print("Ya puedes hablar")

        # guardar lo que escuche
        audio = r.listen(source)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language='es')

            # imprimir en pantalla para desarrollador
            print('Dijiste: ' + pedido)

            # devolver a pedido
            return pedido

        # en caso de fallo en reconocer audio
        except sr.UnknownValueError:
            # prueba de que no comprendió el audio
            print("Ups, no entendí")

            # devolver error
            return "sigo esperando"

        # en caso de no poder resolver el pedido
        except sr.RequestError:
            # prueba de que no comprendió el audio
            print("Ups, no hay servicio")

            # devolver error
            return "sigo esperando"

        # error inesperado
        except:
            # prueba de que no comprendió el audio
            print("Ups, algo ha salido mal")

            # devolver error
            return "sigo esperando"


# funcion para que el asistente sea escuchado
def hablar(mensaje):

    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voices', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el día de la semana
def pedir_dia():

    calendario_dias = {0: 'lunes',
                       1: 'martes',
                       2: 'miercoles',
                       3: 'jueves',
                       4: 'viernes',
                       5: 'sabado',
                       6: 'domingo'}

    # crea variable datos de hoy
    dia = datetime.date.today()

    # crear variable para el dia de semana
    dia_semana = dia.weekday()
    hablar(f'Hoy es {calendario_dias[dia_semana]}')


# informar de la hora
def pedir_hora():

    # crear variable con datos de la hora
    hora = datetime.datetime.now()

    # decir la hora
    hablar(f'Son las {hora.hour}:{hora.minute}')


# saluda al inicio
def saludo_inicial():

    hora = datetime.datetime.now()

    if 6 > hora.hour < 13:
        momento = "Buenos días!"
    elif 13 <= hora.hour < 20:
        momento = "Buenas tardes!"
    else:
        momento = "Buenas noches!"

    # saludar en funcion del día
    hablar(f"{momento} Soy Raili, tu asistente personal. Si tienes cualquier duda, puedes consultar "
           f"con comando de voz 'Ayuda'. ¿En que puedo ayudarte?")


# busca en google
def busca_google(peticion):
    hablar(f'Buscando la mejor información: {peticion}')
    pywhatkit.search(peticion)


# pone la canción en Youtube
def escuchar_musica(peticion):
    hablar(f'Buscando: {peticion}')
    pywhatkit.playonyt(peticion)


def enviar_msg(peticion, msg):
    date = datetime.datetime.now()
    hora = date.hour
    minuto = date.minute
    pywhatkit.sendwhatmsg(f"+34{peticion}", f"{msg}. Mensaje enviado desde mi asistente de voz.",
                          hora, minuto+2)

# CENTRO DE PEDIDOS ----------------------------------------------------------------------------------------------------


def centro_pedidos():

    # variable de corte
    comenzar = True

    while comenzar:

        # activar el micro y guardar el pedido
        pedido = transformar_audio_en_texto().lower()

        if 'eres' in pedido:
            saludo_inicial()
            continue

        if 'hola' in pedido:
            hablar('Buenas, estoy aquí para ayudarte en lo que necesites, prueba a decir: "abre el navegador"')
            continue

        if 'abrir' or 'buscar' or 'busca' in pedido:
            if 'youtube' in pedido:
                hablar('Con gusto, estoy abriendo youtube')
                webbrowser.open('https://www.youtube.com')
                continue
            elif 'spotify' in pedido:
                hablar('Con gusto, estoy abriendo spotify')
                os.system('spotify')
            """elif 'google' or 'navegador' in pedido:
                hablar('Con gusto, estoy abriendo google')
                webbrowser.open('https://www.google.com')
                continue"""

        elif 'escuchar música' in pedido:
            hablar('Dime la canción o albúm')
            pedido = transformar_audio_en_texto().lower()
            escuchar_musica(pedido)

        if 'qué día es' in pedido:
            pedir_dia()
            continue

        if 'qué hora es' in pedido:
            pedir_hora()
            continue

        if 'busca en internet' in pedido:
            hablar('A ello voy')
            pedido = pedido.replace('busca en internet', '')
            busca_google(pedido)
            continue

        lista_emociones_p = ['genial', 'bien', 'alegre', 'emocionado']
        lista_emociones_n_i = ['regular', 'mal', 'ansioso', 'nervioso', 'triste', 'disgustado']
        lista_emociones_m = ['enfadado']

        for emocion in lista_emociones_n_i:
            if emocion in pedido:
                hablar(f'No te preocupes por sentirte {emocion}, seguro que todo irá a mejor. Yo estoy aquí para lo '
                       f'que necesites.')
                continue

        for emocion in lista_emociones_p:
            if emocion in pedido:
                hablar(f'Me alegro de que estés {emocion}, hoy será un gran día, estoy para lo que necesites!')
                continue

        for emocion in lista_emociones_m:
            if emocion in pedido:
                hablar(f'No te preocupes por sentirte {emocion}, seguro que todo irá a mejor. Yo estoy aquí para lo '
                       f'que necesites.')
                continue

        if 'busca en wikipedia' in pedido:
            pedido = pedido.replace('busca en wikipedia', '')
            hablar(f'Buscando {pedido} en wikipedia')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=3)
            hablar('He encontrado esto en Wikipedia')
            hablar(resultado)
            continue

        if 'ayuda' in pedido:
            hablar("""Puedo realizar estas acciones:
            1. Buscar en google: comando 'Busca en internet'
            2. Buscar en Youtube: comando 'Busca en youtube'
            3. Que hora es: comando 'Que hora es'
            4. Que dia es: comando 'Que dia es'
            5. Me puedes decir como te sientes
            6. Buscar música: comando 'escuchar musica'
            7. Busca en wikipedia: comando 'busca en wikipedia'
            8. Abrir el navegador: comando 'abre el navegador'
            9. Saludarte: comando 'Hola'""")

        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pedido = pedido.replace('reproducir', '')
            pywhatkit.playonyt(pedido)
            continue

        elif 'envía un mensaje' in pedido:
            hablar("Dime el numero de telefono")
            numero = transformar_audio_en_texto()
            hablar("¿Que desea enviar?")
            mensaje = transformar_audio_en_texto()
            enviar_msg(numero, mensaje)
            continue

        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue

        elif 'whatsapp' in pedido:
            hablar("Abriendo Whatsapp Web")
            url = "https://web.whatsapp.com/"
            webbrowser.open(url)

        elif 'adiós' in pedido:
            hablar("Encantada, me voy a descansar!")
            break

        elif 'gracias' in pedido:
            hablar('De nada, encantada de ayudarte.')
            break

        elif 'Nada' in pedido:
            hablar('De acuerdo, espero poder ayudarte más adelante')
            break


centro_pedidos()
