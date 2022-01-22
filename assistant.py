import pyttsx3
import speech_recognition as sr
from datetime import datetime as dt
import os
import pywhatkit as pwk
import smtplib
from email.mime.text import MIMEText


engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)
engine.setProperty("rate",150)


recognizer=sr.Recognizer()
source=sr.Microphone()


dic={}
users={}
with open("paths.txt","r") as file:
	for i in file:
		if i!="\n":
			app,path=i.split("=")
			dic[app]=path


def sendMail():
	server=smtplib.SMTP("smtp.gmail.com",587)
	server.ehlo()
	server.starttls()
	server.login(input("Enter Email "),input("Eneter Password "))
	server.sendmail(input("Enter username "),input("Enter reciever email "),input("Enter message "))


def registerPath(app):
	speak("Please Enter the path of "+app)
	dic[app]=input("Enter path of "+app+" ")
	dic[app]+="\n"
	with open("pathsS","a") as file:
		file.write(app+"="+dic[app])

def login():
	speak("Enter name and password")
	uname=input("Enter the name ")
	pwd=input("Enter password ")
	if uname in users and pwd==users[uname]:
		return [True,uname,pwd]
	return [False,uname,pwd]

def speak(sentence):
	engine.say(sentence)	
	engine.runAndWait()

with open("users.txt","r") as file:
	l=file.read().split("\n")
	for i in l:
		k=i.split("-")
		users[k[0]]=k[1]

speak("Hello, This is Robin")


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
	print(cmd)
	if cmd==None:
		return
	
	speak("Command Executing")
	
	if "date" in cmd:
		today=dt.today()
		month=["january","february","march","april","may","june","july","august","september","october","november","december"]
		speak("todays date is "+str(today.day)+" "+month[today.month-1]+" "+str(today.year))
	
	elif "what is your name" in cmd:
		speak("Iam Robin")

	elif "my name" in cmd:
		speak("You are "+dic["name"])
	
	elif "mail" in cmd or "email" in cmd:
		sendMail()		
	
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

	elif "time" in cmd:
		speak("The time is "+dt.now().strftime("%H:%M:%S"))
	
	elif "search" in cmd or "google" in cmd:
		pwk.search(cmd[7:])
	
	elif "what is" in cmd:
		pwk.info(cmd[8:], lines=5)
	
	elif "who is" in cmd:
		pwk.info(cmd[7:], lines=5)
		
	elif "who are you" in cmd:
		speak("Iam Robin, your personal assisatant , ready to help you")
	
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
		#print('"'+dic[cmd[5:]][:-1]+'"')
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

l=login()
if l[0]:
	dic["name"]=l[1]
	speak("Hello "+dic["name"])
	#executCommand("send email")
	while 1:
		executCommand(getCommand())
else:
	speak("Invalid details")
	server=smtplib.SMTP("smtp.gmail.com",587)
	server.ehlo()
	server.starttls()
	server.login("amaansmd1@gmail.com","Foodworld2")
	k="User : "+l[1]+" Password: "+l[2]+" Tried to access the assistant"
	msg = MIMEText(k, 'plain', 'utf-8')
	server.sendmail("amaansmd1", "nihalshareef782@gmail.com",msg.as_string())
	print(type(msg.as_string()))
	exit(0)
