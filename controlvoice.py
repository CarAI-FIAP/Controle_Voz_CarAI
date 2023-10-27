# Bibliotecas
import datetime
import geocoder
import pyttsx3
import pywhatkit
import requests
import serial
import speech_recognition as sr
import wikipedia
import pygame


# Declarando variáveis
audio = sr.Recognizer()
maquina = pyttsx3.init()

# Definindo parâmetros de conexão
port = "COM4"   # Conferir porta que o Arduino está conectado
rate = 9600
conn = serial.Serial(port, rate)  # Realiza conexão


def listenMic():
    comando = ''
    try:
        with sr.Microphone() as source:
            print('Ouvindo...')

            voz = audio.listen(source)
            comando = audio.recognize_google(voz, language='pt-br')
            comando = comando.lower()

            if 'bens' in comando:
                # comando = comando.replace('bens', '')
                maquina.runAndWait()

    except:
        print('Microfone não está ok.')

    return comando


def iniciar():
    maquina.say('Percurso iniciado.')
    maquina.runAndWait()
    # Enviando comando de andar pro Arduino:
    conn.write(b'1')    # Verificar se precisa realizar conversão / "case 1"
    # Tocando Vrum Vrum
    pygame.mixer.init()
    pygame.mixer.music.load('start.mp3')
    pygame.mixer.music.play()
    input()
    pygame.event.wait()


def horas():
    hora = datetime.datetime.now().strftime('%H:%M')
    maquina.say('Agora são' + hora)
    maquina.runAndWait()


def climatempo():
    g = geocoder.ip('me')
    cidade = g.address.lower().split(',')

    # link do open_weather: https://openweathermap.org/
    API_KEY = "b455a023390ad327dc9befbcce4e6793"
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade[0]}&appid={API_KEY}&lang=pt_br"

    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    # descricao = requisicao_dic['weather'][0]['description']
    temperatura = requisicao_dic['main']['temp'] - 273.15
    # print(descricao, f"{temperatura}ºC")
    maquina.say(f'Agora está fazendo {temperatura:.0f} graus celcius.', )
    maquina.runAndWait()


def musica(music):
    resultado = pywhatkit.playonyt(music)
    maquina.say('Tocando música' + music + 'no youtube')
    maquina.runAndWait()


def procuraWikipedia(word):
    wikipedia.set_lang('pt')
    resultado = wikipedia.search(word, 5)
    maquina.say(resultado)
    maquina.runAndWait()


def desligar():
    maquina.say('CarAI desligado.')
    maquina.runAndWait()
    # Enviando comando de desligar pro Arduino:
    conn.write(b'2')  # Verificar se precisa realizar conversão / "case 2"


def taskVoz():
    while True:
        comando = listenMic()

        # Fala horário atual
        if 'bens que horas são' in comando:
            horas()

        # Climatempo atual
        elif 'bens quantos graus' in comando:
            climatempo()

        # Toca música no youtube
        elif 'bens toque' in comando:
            comando = comando.replace('toque', '')
            musica(comando)

        # Pesquisa no wikipedia
        elif 'bens procure por' in comando:
            comando = comando.replace('procure por', '')
            procuraWikipedia(comando)

        # Finaliza todos os programas
        elif 'bens desligar' in comando:
            desligar()

        # Inicia percurso da pista
        elif 'bens vamos passear' in comando:
            iniciar()

        else:
            pass

    conn.close()

taskVoz()
