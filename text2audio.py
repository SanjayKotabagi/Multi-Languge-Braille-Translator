from gtts import gTTS
import os


def convert2speech(text,lang):
    try:
        myobj = gTTS(text=text, slow=False)
        myobj.save("audio.ogg")
        return "audio.ogg"
    except:
        return False
