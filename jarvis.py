import os
import PyPDF2
import pyttsx3  
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
from vosk import Model ,KaldiRecognizer
import random

###package to check connection
import pyaudio
import socket

###for UI of jarvis
"""installed pyqt5 and pyqt5-tools"""
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUI import Ui_MainWindow
import sys

##sapi5 is an API from microsoft(windows) that has some voice by default to speak
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices)  #by default we have 2 voices male and female
engine.setProperty('voice' ,voices[0].id)  ##In my pc 0 is of a boy david and 1 is of a girl named zira
# print(voices[1].id)
engine.setProperty('rate',145)##control speaking speed

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("good morning lucky")
    elif hour>=12 and hour<18:
        speak("good evening Lucky!")
    speak("hello Lucky! i am jarvis and i am here to help you")
    speak("Please tell me hw i can help you")


def check_connection():
    """this is to check if any internet connection is present"""
    try:
        socket.create_connection(('Google.com',80))
        return True
    
    except OSError:
        return False

def pdf_reader():
    book = open("marketing.pdf",'rb')
    pdfreader = PyPDF2.PdfFileReader(book)
    pages = pdfreader.numPages   ##calculate no of pages
    speak(f"Total no of pages in the book is {pages}")
    speak(f"Please enter the page number you want to start from")
    pg = int(input("Please enter the page number you want to start from :") + 1)
    page = pdfreader.getPage(pg)
    text = page.extractText() ###store the extracted text
    speak(text)

"""Code of jarvis GUI starts from here"""
class MainThread(QThread):  ##Inherited QThread class
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        super().__init__()
        self.logic()
   
    def logic(self):
        wishMe()
        while True:
            if check_connection() == True:
                self.query = self.takecmd()
            else:    
                self.query = self.takeofflinecmd()

            """####logic for executing command"""
            if 'time' in self.query:
                str_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"time is {str_time}")
                print(str_time)
            
            elif 'increase volume' in self.query or 'volume up' in self.query:
                import pyautogui
                pyautogui.press("volumeup")
            elif 'decrease volume' in self.query or 'volume down' in self.query:
                import pyautogui
                pyautogui.press("volumedown")
            elif 'mute volume' in self.query or 'mute' in self.query:
                import pyautogui
                pyautogui.press("volumemute")
            elif 'play music' in self.query:
                music_dir = 'E:\\songs'
                songs = os.listdir(music_dir)##list all files of music dir
                music = random.randrange(0,len(songs)-1)
                os.startfile(os.path.join(music_dir,songs[music]))##os.startfile open the file
            elif 'Hey' in self.query:
                speak("Hey Lucky! What are you doing?")
            elif 'Thank you' in self.query or "thanks" in self.query or 'thank' in self.query:
                speak("Welcome Lucky ,How's your day")
            ####online work
            elif 'read' in self.query:
                pdf_reader()
            elif 'wikipedia' in self.query:
                speak('searching in wikipedia')
                query = query.replace("wikipedia","")
                result = wikipedia.summary(query ,sentences=1)##sentences argument says how many sentences to read from wikipedia
                speak("According to wikipedia")
                print(result)
                speak(result)
            elif 'open youtube' in self.query:
                webbrowser.open('youtube.com')
            elif 'open google' in self.query:
                webbrowser.open('google.com')
            else : 
                print("no Result")

    def takecmd(self):
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
            return "none" ##return none string if any error come
        return query.lower()    

    def takeofflinecmd(self):
        """take command in offline mode"""
        model = Model(r"vosk\\vosk-model-small-en-us-0.15")
        recognizer = KaldiRecognizer(model,16000)
        
        mic = pyaudio.PyAudio()
        stream = mic.open(rate=16000,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=8192)
        stream.start_stream()
        print("Listening......")
        data = stream.read(4096)
            
        while True:
            data = stream.read(4096)    
            if recognizer.AcceptWaveform(data):
                print("recognizing.....") 
                data2 = recognizer.Result()
                print(data2)
                return data2
                      
####to start the thread class above
start_thread = MainThread()

####this is to run Gui 
class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.startTask)
        self.ui.pushButton.clicked.connect(self.close)


    def startTask(self):
        self.ui.movie = QtGui.QMovie("jarvis2.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()

        ####copy same 3 code above if yoy have more than one gif

        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start(1000)
  
        start_thread.start()

    def showtime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser_2.setText(label_date)
        self.ui.textBrowser.setText(label_time)
   
app = QApplication(sys.argv)  
jarvis = Main()
jarvis.show()
exit(app.exec_())

