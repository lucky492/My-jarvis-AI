
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
## print(voices)  #by default we have 2 voices male and female
engine.setProperty('voice' ,voices[0].id)  ##In my pc 0 is of a boy david and 1 is of a girl named zira
## print(voices[0].id)
engine.setProperty('rate',130)##control speaking speed

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

