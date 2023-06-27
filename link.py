from flask import Flask, render_template, request
import threading
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

app = Flask(__name__)

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'lia' in command:
                command = command.replace('lia', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'how to ' in command:
        make = command
        pywhatkit.playonyt(make)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
        talk('please say the command again')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/execute", methods=['POST'])
def execute():
    threading.Thread(target=run_alexa).start()
    return "Command executed"


if __name__ == '__main__':
    app.run(debug=True, port=5001)
