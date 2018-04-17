# -*- coding: utf-8 -*-

from gtts import gTTS

text_to_speech = "hello i am Q-bo"
tts = gTTS(text = text_to_speech, lang = 'en')
tts.save("/home/pi/Documents/hello.wav") #tts audio file save