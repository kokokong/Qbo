# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7

# NOTE: this example requires PyAudio because it uses the Microphone class

# install TTs google
# sudo pip install gTTS 

import speech_recognition as sr
import subprocess
import pipes
import json
import apiai
import time
import yaml
import os
import wave
from face_recog import face_recog
from gtts import gTTS

class QBOtalk:
	def __init__(self):
		config = yaml.safe_load(open("/home/pi/Documents/config.yml"))

		CLIENT_ACCESS_TOKEN = '85feb3751ea24fe8a812a8231cf9c14b' #token change
		#CLIENT_ACCESS_TOKEN = config["tokenAPIai"]
		print "TOKEN: " + CLIENT_ACCESS_TOKEN
		#	You can enter your token in the next line
		#       CLIENT_ACCESS_TOKEN = '3f738f7e64d24d51b126f442b1513d7a'
		# obtain audio from the microphone
		self.r = sr.Recognizer()
		self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
		self.Response = "hello"
		self.GetResponse = False
		self.GetAudio = False
		self.strAudio = ""
		self.terminal = False
		self.config = config

		for i, mic_name in enumerate (sr.Microphone.list_microphone_names()):
			if(mic_name == "dmicQBO_sv"):
				self.m = sr.Microphone(i)
		with self.m as source:        
			self.r.adjust_for_ambient_noise(source)

	def Decode(self, audio):
		try:
			str = self.r.recognize_google(audio)
			print(str)
			if any(s in str for s in ("catch","touch")):
				face_recog()
				str_resp = ""
				str = ""
				return str_resp
			else:
				if "bye" in str:
					self.terminal=True
				print "LISTEN: " + str
				request = self.ai.text_request()
				request.lang = 'es'
				request.query = str
				response = request.getresponse()
				jsonresp = response.read()
				data = json.loads(jsonresp)
				str_resp = data["result"]["fulfillment"]["speech"]

		except sr.UnknownValueError:
			str_resp = ""
		except sr.RequestError as e:
			str_resp = "Could not request results from Speech Recognition service"
		return str_resp



	def SpeechText(self, text_to_speech):
		try:
			speak = "espeak -ven+f3 \"" + text_to_speech + "\" --stdout  | aplay -D convertQBO"
		
			print(text_to_speech)

			#tts = gTTS(text = text_to_speech, lang = 'en')
			#tts.save("/home/pi/Documents/say.wav") #tts audio file save
			print "QBOtalk: " + text_to_speech
			print(speak)
			result = subprocess.call(speak, shell = True) #speak sound
		except:
			pass
			
	def callback(self, recognizer, audio):
		try:
			self.Response = self.Decode(audio)
			self.GetResponse = True
			print("Google say ")
			#self.SpeechText(self.Response)
		except:
			return   
		
	def callback_listen(self, recognizer, audio):
		print("callback listen")
		try:
			#strSpanish = self.r.recognize_google(audio,language="es-ES")
			with open("microphone-results.wav", "wb") as f:
				f.write(audio.get_wav_data())
				if (self.config["language"] == "spanish"):
						self.strAudio = self.r.recognize_google(audio, language="es-ES")
				else:
						self.strAudio = self.r.recognize_google(audio)

				self.strAudio = self.r.recognize_google(audio)
				self.GetAudio = True
				print("listen: " + self.strAudio)
				#print("listenSpanish: ", strSpanish)
				#self.SpeechText(self.Response)
		except:
			print("callback listen exception")
			self.strAudio = ""
			return

	def Start(self):
		hello = subprocess.call("mpg321 /home/pi/Documents/Pythonpro/audio/hello.mp3 -a convertQBO",shell=True)
		print("Say something!")
		self.r.operation_timeout = 100
		with self.m as source:
			audio = self.r.listen(source = source, timeout = 3)

		# recognize speech using Google Speech Recognition

		Response = self.Decode(audio)
		self.SpeechText(Response)
		
	def StartBack(self):
		with self.m as source:
			self.r.adjust_for_ambient_noise(source)

		print("start background listening")
		print("Say Something!")
		return self.r.listen_in_background(self.m, self.callback)

	def StartBackListen(self):
		with self.m as source:
			self.r.adjust_for_ambient_noise(source)

		print("start background only listening")

		return self.r.listen_in_background(self.m, self.callback_listen)



if __name__ == "__main__":
	qbo = QBOtalk()
	qbo.Start()

	while True:
		print("start background listening")

		listen_thd = qbo.StartBack()
		if qbo.terminal == True:
			break
		for _ in range(100):
			if qbo.GetResponse:
				listen_thd(wait_for_stop = True)
				print("Qbo Response :",qbo.Response)
				qbo.SpeechText(qbo.Response)
				qbo.GetResponse = False
				break
			time.sleep(0.1)
		print("End listening")

