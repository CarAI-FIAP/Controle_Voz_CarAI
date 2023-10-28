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
import os


# Declarando variáveis
audio = sr.Recognizer()
maquina = pyttsx3.init()

# Definindo parâmetros de conexão
port = "COM3"   # Conferir porta que o Arduino está conectado
rate = 9600
conn = serial.Serial(port, rate)  # Realiza conexão


# Função para escutar o que o usuário está dizendo
def listenMic():
    comando = ''
    try:
        with sr.Microphone() as source:
            print("Ajustando para ruído ambiente. Aguarde...")
            audio.adjust_for_ambient_noise(source, duration=3)  # Ajusta para ruído de fundo
            print("Pronto para ouvir! Fale algo...")
            voz = audio.listen(source)
            print("Capturando áudio...")
            comando = audio.recognize_google(voz, language='pt-BR').lower()
            comando = comando.lower()


            if 'bens' in comando:
                # comando = comando.replace('bens', '')
                maquina.runAndWait()

    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
        return ""
    except sr.RequestError:
        print("Houve um problema ao tentar usar a API do Google.")
        return ""
    return comando

#
# def listenMic():
#     comando = ''
#     try:
#         with sr.Microphone() as source:
#             print('Ouvindo...')
#
#             voz = audio.listen(source)
#             comando = audio.recognize_google(voz, language='pt-br')
#             comando = comando.lower()
#
#             if 'alexa' in comando:
#                 print(comando)
#                 comando = comando.replace('alexa', '')
#                 maquina.runAndWait()
#
#     except:
#         print('Microfone não está ok.')
#
#     return comando

def vrum():
    # Tocando Vrum Vrum
    # pygame.mixer.init()
    # pygame.init()
    # pygame.mixer.music.load('start.mp3')
    # pygame.mixer_music.play()
    # pygame.event.wait()

    pygame.init()
    if os.path.exists('start.mp3'):
        pygame.mixer.music.load('start.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1)

        clock = pygame.time.Clock()
        clock.tick(10)

        while pygame.mixer.music.get_busy():
            pygame.event.poll()
            clock.tick(10)
    else:
        print('O arquivo musica.mp3 não está no diretório do script Python')

def iniciar():
    # Enviando comando de andar pro Arduino:
    conn.write(b'1')  # Verificar se precisa realizar conversão / "case 1"

    maquina.say('Percurso iniciado.')
    maquina.runAndWait()



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

def pipi():
    # Tocando pipi
    # pygame.mixer.init()
    # pygame.mixer.music.load('stop.mp3')
    # pygame.mixer.music.play()
    # input()
    # pygame.event.wait()

    pygame.init()
    if os.path.exists('stop.mp3'):
        pygame.mixer.music.load('stop.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1)

        clock = pygame.time.Clock()
        clock.tick(10)

        while pygame.mixer.music.get_busy():
            pygame.event.poll()
            clock.tick(10)
    else:
        print('O arquivo musica.mp3 não está no diretório do script Python')


def desligar():
    # Enviando comando de desligar pro Arduino:
    conn.write(b'2')  # Verificar se precisa realizar conversão / "case 2"

    maquina.say('CarAI desligado.')
    maquina.runAndWait()

def bibi():
    pygame.init()
    if os.path.exists('Buzina.mp3'):
        pygame.mixer.music.load('Buzina.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1)

        clock = pygame.time.Clock()
        clock.tick(10)

        while pygame.mixer.music.get_busy():
            pygame.event.poll()
            clock.tick(10)
    else:
        print('O arquivo musica.mp3 não está no diretório do script Python')


def taskVoz():
    while True:
        comando = listenMic()

        # Fala horário atual
        if 'horas' in comando:
            horas()

        # Climatempo atual
        elif 'quantos graus' in comando:
            climatempo()

        # Toca música no youtube
        elif 'toque' in comando:
            comando = comando.replace('toque', '')
            musica(comando)

        # Pesquisa no wikipedia
        elif 'procure por' in comando:
            comando = comando.replace('procure por', '')
            procuraWikipedia(comando)

        # Finaliza todos os programas
        elif 'desligar carro' in comando:
            desligar()
            pipi()

        # Inicia percurso da pista
        elif 'iniciar percurso' in comando:
            iniciar()
            vrum()

        # Inicia percurso da pista
        elif 'buzina' in comando:
            bibi()

        else:
            print("Não entendi")
            pass

    conn.close()

taskVoz()
