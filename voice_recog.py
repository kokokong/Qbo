from __future__ import print_function
import speech_recognition as sr


def voice_recog():
	r = sr.Recognizer()
	for i, mic_name in enumerate (sr.Microphone.list_microphone_names()):
		if(mic_name == "dmicQBO_sv"):
			m = sr.Microphone(i)
	with m as source:        
		r.adjust_for_ambient_noise(source)

	r.operation_timeout = 100
	print(m)

	with m as source:
		print("Say something!")
		audio = r.listen(source = source)

	stt = r.recognize_google(audio)
	return stt
