import pyttsx3
ttsengine = pyttsx3.init()

def speak_text(text):
    if text:
        print(text)
        # ttsengine.say(text)
        # ttsengine.runAndWait()


