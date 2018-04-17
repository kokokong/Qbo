#-*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import requests
import ast
import cv2
import subprocess
import thread
from gtts import gTTS

	
file = "./face.png"
client_id = "6BlzHIBaB58ueA6dkN4j"
client_secret = "kPMIqQNiFy"
# url = "https://openapi.naver.com/v1/vision/face" // 얼굴감지

emotion_dict = {"angry":"화난","disgust":"역겨운","fear":"두운려",
"laugh":"웃는","neutral":"평온한","sad":"슬픈","surprise":"놀란","smile":"웃는","talking":"말하는"}

face_cascade = cv2.CascadeClassifier("/home/pi/Documents/Pythonpro/haarcascade_frontalface_alt2.xml")

def FaceRcognition(file):
    url = "https://openapi.naver.com/v1/vision/celebrity" #// 유명인 얼굴인식
    files = {'image': open(file, 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
  
    if(rescode==200):
        print(response.text)
        rt = ast.literal_eval(response.text)
        celeb = rt["faces"][0]["celebrity"]['value']
    else:
        print("Error Code:" + rescode)
       
    return celeb

def EmotionRcognition(file):
    url = "https://openapi.naver.com/v1/vision/face" #// 얼굴감지
    files = {'image': open(file, 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
		try:
			rt = ast.literal_eval(response.text)
			age = rt["faces"][0]["age"]['value'][:2]
			emotion = rt["faces"][0]["emotion"]['value']
			#celeb = rt["faces"][0]["celebrity"]['value']
		except: 
			print(response.text)
    else:
        print("Error Code:" + rescode)
    return age, emotion

def cap_img(file):
		cap = cv2.VideoCapture(0)

		print ('width: {0}, height: {1}'.format(cap.get(3),cap.get(4)))


		while(True):
			# ret : frame capture결과(boolean)
			# frame : Capture한 frame
			ret, frame = cap.read()
			if (ret):
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				faces = face_cascade.detectMultiScale(gray, 1.3, 5)
				# Draw a rectangle around the faces
				for (x, y, w, h) in faces:
					cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

				cv2.imshow('frame', frame)
				if cv2.waitKey(1) & 0xFF == ord('c'):
					cv2.imwrite(file,frame)
					break
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

		cap.release()
		cv2.destroyAllWindows()

def face_recog():
	cap_img(file)


	name = FaceRcognition(file)
	print(name)
	age, emotion =EmotionRcognition(file)
	print(emotion)




	String =  str(emotion_dict[emotion]+" 표정을 짓고 있는 당신은 "+age+"살로 추정되며 "+name+" 닮으셨군요")

	String = String.decode("utf8")
	tts = gTTS(text=String, lang='ko')
	tts.save("/home/pi/Documents/Pythonpro/audio/fr.mp3")

	print(String)

	#result = subprocess.call("mpg321 /home/pi/Documents/Pythonpro/audio/fr.mp3 -a convertQBO",shell=True)
	
if __name__ == '__main__':
	face_recog()
	
