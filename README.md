# Controle de Voz - CarAI

![Static Badge](https://img.shields.io/badge/version-v.0.0.1-green)
![Static Badge](https://img.shields.io/badge/author-Laura_Sorato-blue)

## :warning: Importante:

Referência: https://www.youtube.com/watch?v=36RIoJeV95M

Bibliotecas utilizadas:
- SpeechRecognition: https://pypi.org/project/SpeechRecognition/
- PyAudio: https://pypi.org/project/PyAudio/
- Pyttsx3: https://pypi.org/project/pyttsx3/
- Wikipedia: https://pypi.org/project/wikipedia/
- Pywhatkit: https://pypi.org/project/pywhatkit/

<hr>

## :pencil2: Exemplo: Enviando comando para Arduino

### Passo 1 - Importando bibliotecas
```
# Bibliotecas
import datetime
import requests
import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit
import geocoder
import serial
```

### Passo 2 - Declarando variáveis

```
# Declarando variáveis
audio = sr.Recognizer()
maquina = pyttsx3.init()

# Definindo parâmetros de conexão
port = "COM4"   # Conferir porta que o Arduino está conectado
rate = 9600
conn = serial.Serial(port, rate)  # Realiza conexão
```

### Passo 3 - Configurando microfone

```
def listenMic():
    comando = ''
    try:
        with sr.Microphone() as source:
            print('Ouvindo...')

            voz = audio.listen(source)
            comando = audio.recognize_google(voz, language='pt-br')
            comando = comando.lower()

            if 'alexa' in comando:
                print(comando)
                comando = comando.replace('alexa', '')
                maquina.runAndWait()

    except:
        print('Microfone não está ok.')

    return comando
```

### Passo 4 - Definindo funções

```
def vamosPassear():
    maquina.say('Percurso iniciado.')
    maquina.runAndWait()
    # Enviando comando de andar pro Arduino:
    conn.write(b'1')    # Verificar se precisa realizar conversão


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
    resultado = wikipedia.summary(word, 2)
    maquina.say(resultado)
    maquina.runAndWait()


def finaliza():
    maquina.say('Programa encerrado.')
    maquina.runAndWait()
```

### Passo 5 - Configurando função de escuta "ALL THE TIME"

```
def taskVoz():
    while True:
        comando = listenMic()

        # Fala horário atual
        if 'que horas são' in comando:
            horas()

        # Climatempo atual
        elif 'graus' in comando:
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
        elif 'finaliza' in comando:
            funcao = finaliza()
            return funcao
            break

        # Inicia percurso da pista
        elif 'vamos passear' in comando:
            vamosPassear()

        else:
            maquina.say('Desculpe, utilize um comando válido')
            maquina.runAndWait()
    
    conn.close()
```

### Passo 6 - Rodando código

```
taskVoz()
```
