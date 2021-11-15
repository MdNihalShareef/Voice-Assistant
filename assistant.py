import pyttsx3
from pywhatkit.main import sendwhatmsg
import speech_recognition as sr
from datetime import datetime as dt
import os
import pywhatkit as pwk


engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)
engine.setProperty("rate",150)


recognizer=sr.Recognizer()
source=sr.Microphone()


dic={}
with open("paths.txt","r") as file:
	for i in file:
		if i!="\n":
			app,path=i.split("=")
			dic[app]=path


def registerPath(app):
	speak("Please Enter the path of "+app)
	dic[app]=input("Enter path of "+app+" ")
	dic[app]+="\n"
	with open("paths.txt","a") as file:
		file.write(app+"="+dic[app])


def speak(sentence):
	engine.say(sentence)	
	engine.runAndWait()

if "name" not in dic:
	speak("Hello, can i know you name ")
	dic["name"]=input("Enter your name ") + "\n"
	with open("paths.txt","a") as file:
		file.write("name="+dic["name"])


speak("Hello {}, Sam here, How can i Help you".format(dic["name"][:-1]))


def getCommand():
    speak("Accepting Command")
    try:
        with sr.Microphone() as source:	
            print("Speak now.....")
            audio=recognizer.listen(source)
            text=recognizer.recognize_google(audio)
            return text.lower()
    except:
        return None


def executCommand(cmd):
	print("Command",cmd)
	if cmd==None:
		return
	
	speak("Command Executing")
	
	if "date" in cmd:
		today=dt.today()
		month=["january","february","march","april","may","june","july","august","september","october","november","december"]
		speak("todays date is "+str(today.day)+" "+month[today.month-1]+" "+str(today.year))
	
	elif "what is your name" in cmd:
		speak("Iam Sam")

	elif "my name" in cmd:
		speak("You are "+dic["name"][:-1])
	
	
	elif "change" in cmd and "name" in cmd:
		speak("Please enter your name")
		dic["name"]=input("Enter you name ")+"\n"
		with open("paths.txt","w") as file:
			for i in dic:
				file.write(i+"="+dic[i])
			
	
	elif "change" in cmd and ("path" in cmd or "settings" in cmd):
		speak("Enter the application name ")
		name=input("App name ")
		speak("Enter new path of "+name)
		path=input("new path ")
		dic[name]=path+"\n"
		with open("paths.txt","w") as file:
			for i in dic:
				file.write(i+"="+dic[i])

	elif "whats app" in cmd or "whatsapp" in cmd:
		speak("Enter the details")
		pwk.sendwhatmsg(input("Phone no. to send "),input("Enter Message "),int(input("Enter time - hour (in 24 hour format) ")),int(input("Enter min ")))

	elif "search" in cmd or "google" in cmd:
		pwk.search(cmd[7:])
	
	elif "what is" in cmd:
		pwk.info(cmd[8:], lines=5)
	
	elif "who is" in cmd:
		pwk.info(cmd[7:], lines=5)
		
	elif "who are you" in cmd:
		speak("Iam sam, your personal assisatant , ready to help you")
	
	elif "time" in cmd:
		speak("The time is "+dt.now().strftime("%H:%M:%S"))
	
	elif "hi" in cmd  or "hey there" in cmd or "hello" in cmd or "hai" in cmd:
		speak("Hey There "+dic["name"])
	
	elif "how are you" in cmd or "how you doing" in cmd:
		speak("Iam fine")
		speak("And what about you?")
	
	elif ("good" in cmd or "fine" in cmd) and ("i am" in cmd):
		speak("Noice")
	
	elif "open" in cmd:
		if cmd[5:] not in dic:
			registerPath(cmd[5:])
		print('"'+dic[cmd[5:]][:-1]+'"')
		os.system('"'+dic[cmd[5:]][:-1]+'"')
	
	elif "exit" in cmd or "close" in cmd:
		speak("Closing the assistant")
		speak("Good bye "+dic["name"])
		exit()
	
	elif "play" in cmd:
		print(cmd[5:])
		pwk.playonyt(cmd[5:])
	
	else:
		speak("Command unclear")
while 1:
	executCommand(getCommand())
