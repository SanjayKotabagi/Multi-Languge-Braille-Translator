import streamlit as st
from io import StringIO
import os
import base64
import speech_recognition as sr
import text2audio as ta


def load_view():

    if 'inputtype' not in st.session_state:
        st.session_state['inputtype'] = 'Locally'
        
    if 'convert' not in st.session_state:
        st.session_state['convert'] = 'False'

    if 'needaudio' not in st.session_state:
        st.session_state['needaudio'] = 'False'



    needaudio = False
    st.markdown("<h1 style='text-align: left; color: White; margin-top: -80px;'>English to Braille Conversion</h1>", unsafe_allow_html=True)
    string_data = ""
    if st.button("Get text Locally"):
        st.session_state.inputtype = 'Local'  
    if st.button("Get text From Keyboard"):
        st.session_state.inputtype = 'Keyboard'
    
    if st.session_state.inputtype == 'Local':
        file = st.file_uploader("Choose a file")
        if file is not None:
            stringio = StringIO(file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            st.write(string_data)
        if st.button("Convert"):
            st.session_state.convert = True
            
    elif st.session_state.inputtype == 'Keyboard':
        string_data = st.text_area("Enter Text to convert")
        if st.button("Convert"):
            st.session_state.convert = True

  
    if st.session_state.convert == True:
        res = convertText(string_data)
        st.subheader(res)

    if st.button("Get Audio"):
        needaudio = True
    
    if needaudio == True:
        aud = ta.convert2speech(string_data,'kn')
        audio_file = open(aud, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/ogg')



#---------------------------> 

characterUnicodes = {'a': '\u2801', 'b': '\u2803', 'k': '\u2805', 'l': '\u2807', 'c': '\u2809', 'i': '\u280A',
'f': '\u280B', 'm': '\u280D', 's': '\u280E', 'p': '\u280F', 'e': '\u2811', 'h': '\u2813', 'o': '\u2815', 'r': '\u2817',
'd': '\u2819', 'j': '\u281A', 'g': '\u281B', 'n': '\u281D', 't': '\u281E', 'q': '\u281F', 'u': '\u2825', 'v': '\u2827',
'x': '\u282D', 'z': '\u2835', 'w': '\u283A', 'y': '\u283D', 'num': '\u283C', 'caps': '\u2820', '.': '\u2832',
"'": '\u2804', ',': '\u2802', '-': '\u2824', '/': '\u280C', '!' : '\u2816', '?': '\u2826', '$': '\u2832', ':': '\u2812',
';': '\u2830', '(': '\u2836', ')': '\u2836', ' ': ' ', '1': '\u2801', '2': '\u2803', '3': '\u2809', '4': '\u2819',
'5': '\u2811', '6': '\u280B', '7': '\u281B', '8': '\u2813', '9': '\u280A', '0': '\u281A'}

numberPunctuations = ['.', ',', '-', '/', '$']
escapeCharacters = ['\n', '\r', '\t']

def convertText(textToConvert):
  if type(textToConvert) is not str:
    raise TypeError("Only strings can be converted")
  return convert(textToConvert)

def convertFile(fileToConvert):
  if type(fileToConvert) is not str:
    raise TypeError("Please provide a valid file name")
  file = open(fileToConvert, "r")
  lines = file.readlines()
  convertedText = ''
  for line in lines:
    convertedText += convert(line)
  return convertedText  

def convert(textToConvert):
  isNumber = False
  convertedText = ''
  for character in textToConvert:
    if character in escapeCharacters:
      convertedText += character
      continue
    if character.isupper():
      convertedText += characterUnicodes.get('caps')
      character = character.lower()
    if character.isdigit():
      if not isNumber:
        isNumber = True
        convertedText += characterUnicodes.get('num')
    else:
      if isNumber and character not in numberPunctuations:
        isNumber = False
    convertedText += characterUnicodes.get(character)
  return convertedText

#print(convert('We thought youd like to know that weve dispatched your item'))
