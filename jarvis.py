import pyttsx3  
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from vosk import Model ,KaldiRecognizer
import random

###package to check connection
import pyaudio
import socket


###sapi5 is an API from microsoft(windows) that has some voice by default to speak
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)  #by default we have 2 voices male and female
engine.setProperty('voice' ,voices[0].id)  ### in my pc 0 is of a boy david and 1 is of a girl named zira
# print(voices[0].id)


def checkinternetconnection():
    """check internet connection"""
    try:
        socket.create_connection("1.1.1.1",53)
        return True
    except:
        pass
        return False


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


####logic for executing command
def logic(query):
     ####logic for executing command
    if 'wikipedia' in query:
        speak('searching in wikipedia')
        query = query.replace("wikipedia","")
        result = wikipedia.summary(query ,sentences = 1) ####sentences argument says how many sentences to read from wikipedia
        speak("According to wikipedia")
        print(result)
        speak(result)

    elif 'open youtube' in query:
        webbrowser.open('youtube.com')
    
    elif 'open google' in query:
        webbrowser.open('google.com')

    elif 'play music' in query:
        music_dir = 'E:\\songs'
        songs = os.listdir(music_dir)   #####list all files of music dir
        music = random.randrange(0,len(songs)-1)
        os.startfile(os.path.join(music_dir,songs[music]))  #### os.startfile open the file
            
    elif 'time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"time is {str_time}")
        
    elif 'one' in query:
        print("hello sir how's your day")
        speak("No sir! you are not no one")

    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("good evening sir!")
    elif hour>=12 and hour<18:
        speak("good mornig sir!")
    else : speak("good morning sir!")
    speak("hello sir! i am jarvis and i am here to help you")


def takeofflinecmd():
    """take command in offline mode"""
    model = Model(r"C:\\Users\\user\Jarvis AI\\vosk\\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model,16000)
    
    mic = pyaudio.PyAudio()
    stream = mic.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=8192)
    stream.start_stream()
    print("Listening......")

    data = stream.read(4069)
        
    while True:
        data = stream.read(4096)    
        if recognizer.AcceptWaveform(data):
            print("recognizing.....") 
            data2 = recognizer.Result()
            print(data2)
            print(type(data2))
            logic(data2)
       

def takecmd():
    """ It take microphone input from user and return string output """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 2
        r.energy_threshold = 200
        audio = r.listen(source)
    try:
        print("Recognising....")
        query = r.recognize_google(audio,language='en-in')
        print(f"You said : {query}\n")
    
    except Exception as e:
        print("say again please....")
        return "none"   ##return none string if any error come
    
    return query    
        
        

if __name__ == "__main__": 
    wishMe()
    while True: 
        if checkinternetconnection == True:
            query = takecmd().lower()
            logic(query)
        else :
            takeofflinecmd() 
            
            

        
