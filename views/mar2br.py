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



    needaudio = False
    st.markdown("<h1 style='text-align: left; color: White; margin-top: -80px;'>Marati to Braille Conversion</h1>", unsafe_allow_html=True)
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
        string_data = st.text_area("ಪರಿವರ್ತಿಸಲು ಪಠ್ಯವನ್ನು ನಮೂದಿಸಿ")
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

charmap_iso15919 = {
    "Knda": [ 
        u"ಀ", u"ॅ",u"ं",u"ः", u"಄", u"अ", u"आ", u"इ", u"ई", u"उ", u"ऊ", u"ಋ", u"ಌ", u"಍", u"ए", u"ऐ", 
        u"ಐ", u"಑", u"ओ", u"औ", u"ಔ", u"क",u"ख",u"ग",u"घ",u"ङ", u"च",u"छ",u"ज",u"झ",u"ञ", u"ट", 
        u"ठ",u"ड",u"ढ",u"ण",u"त",u"थ",u"द",u"ध",u"न", u"಩", u"प",u"फ",u"ब",u"भ",u"म",u"य",
        u"र", u"ಱ", u"ल", u"ಳ", u"಴",u"व",u"श",u"ष",u"स",u"ह", u"಺", u"಻", u"಼", u"ಽ", u"ा",u"ि", 
        u"ी",u"ु",u"ू", u"೅",u"े",u"ै",u"्", u"೉", u"ो",u"ौ", u"ೌ", u"್", u"೎", u"೏", 
        u"೐", u"೑", u"೒", u"೓", u"೔", u"ೕ", u"ೖ", u"೗", u"೘", u"೙", u"೚", u"೛", u"೜", u"ೝ", u"ೞ", u"೟", 
        u"ೠ", u"ೡ", u"ೢ", u"ೣ", u"೤", u"೥", u"०",u"१",u"२",u"३",u"४",u"५",u"६",u"७",u"८",u"९", u"0 ", u"1 ", u"2 ", u"3 ", u"4 ", u"5 ", u"6 ", u"7 ", u"8 ", u"9 ",
        u"೰", u"ೱ", u"ೲ", u"ೳ", u"೴", u"೵", u"೶", u"೷", u"೸", u"೹", u"೺", u"೻", u"೼", u"೽", u"೾", u"೿",' ','!','"','#','$',
                '%','&','','(',')',
                '*','+',',','-','.',
                '/',' ','ॉ'
    ],
    "Latn": [
        u" ", u"m̐ ", u"ṁ ", u"ḥ ", u" ", u"a ", u"ā ", u"i ", u"ī ", u"u ", u"ū ", u"ṛ ", u"ḷ ", u"ê ", u"e ", u"ē ", 
        u"ai ", u"ô ", u"o ", u"ō ", u"au ", u"k ", u"kh ", u"g ", u"gh ", u"ṅ ", u"c ", u"ch ", u"j ", u"jh ", u"ñ ", u"ṭ ", 
        u"ṭh ", u"ḍ ", u"ḍh ", u"ṇ ", u"t ", u"th ", u"d ", u"dh ", u"n ", u"ṉ ", u"p ", u"ph ", u"b ", u"bh ", u"m ", u"y ", 
        u"r ", u"ṟ ", u"l ", u"ḷ ", u"ḻ ", u"v ", u"ś ", u"ṣ ", u"s ", u"h ", u" ", u" ", u" ", u"' ", u"ā ", u"i ",
        u"ī ", u"u ", u"ū ", u"ṛ", u"ṝ ", u"ê ", u"e ", u"ē ", u"i ", u"ô ", u"o ", u"ō ", u"u ", u" ", u" ", u" ", 
        u"oṃ ", u" ", u" ", u" ", u" ", u" ", u" ", u" ", u"q ", u"ḵẖ ", u"ġ ", u"z ", u"ṛ ", u"ṛh ", u"f ", u"ẏ ", 
        u"ṝ ", u"ḹ ", u"ḷ ", u"ḹ ", u". ", u".. ", u"0 ", u"1 ", u"2 ", u"3 ", u"4 ", u"5 ", u"6 ", u"7 ", u"8 ", u"9 ", u"0 ", u"1 ", u"2 ", u"3 ", u"4 ", u"5 ", u"6 ", u"7 ", u"8 ", u"9 ", 
        u"… ", u" ", u" ", u" ", u" ", u" ", u" ", u" ", u" ", u" ", u" ", u" ", u" ", u" ", u" ", u"",' ','!','"','#','$',
                '%','&','','(',')',
                '*','+',',','-','.',
                '/',' ','⠭'
    ],
}


words = ['a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'ē', 'ai', 'o', 'ō', 'au', 'r̥', 'r̥̄', 
        'k', 'kh', 'g', 'gh', 'ṅ', 
        'c', 'ch', 'j', 'jh', 'ñ', 
        'ṭ', 'ṭh', 'ḍ', 'ḍh', 'ṇ', 
        't', 'th', 'd', 'dh', 'n', 
        'p', 'ph', 'b', 'bh', 'm', 
        'y', 'r', 'l', 'ḷ', 'v', 
        'ś', 'ṣ', 's', 'h', 'kṣ', ' ',
        'ṁ', 'ṛ',
        '!','"','#','$',
                '%','&','','(',')',
                '*','+',',','-','.',
                '/',' ','1','2','3','4','5','6','7','8','9','0']

braille = ['⠁', '⠜', '⠊', '⠔', '⠥', '⠳', '⠢', '⠑', '⠌', '⠭', '⠕', '⠪', '⠐⠗', '⠠⠗', 
        '⠅', '⠨', '⠛', '⠣', '⠬', 
        '⠉', '⠡', '⠚', '⠴', '⠒', 
        '⠾', '⠺', '⠫', '⠿', '⠼', 
        '⠞', '⠹', '⠙', '⠮', '⠝', 
        '⠏', '⠖', '⠃', '⠘', '⠍', 
        '⠽', '⠗', '⠇', '⠸', '⠧', 
        '⠩', '⠯', '⠎', '⠓', '⠅⠈⠯', ' ',
        '⠰','⠐⠗',
        '⠖','⠠⠶','⠸⠹','⠈⠎',
                '⠨⠴','⠈⠯','⠄','⠐⠣','⠐⠜',
                '⠐⠔','⠐⠖','⠠','⠤','⠲',
                '⠸⠌', ' ','⠼⠁','⠼⠃','⠼⠉','⠼⠙','⠼⠑','⠼⠋','⠼⠛','⠼⠓','⠼⠊','⠼⠚']



ascii_braille = {}
arrayLength = len(words)
counter = 0


while counter < arrayLength:
    ascii_braille[words[counter]] = braille[counter]
    counter = counter + 1


def convert2bril(text):
    final_string = ''
    for char in text.split():
        char = char.lower()
        try:
            final_string = final_string + ascii_braille[char]
        except:
            continue
    return final_string

def convertText(text):
    res = ''
    for i in text:
        print(i)
        ind = charmap_iso15919["Knda"].index(i)
        res += charmap_iso15919["Latn"][ind]
    res = convert2bril(res)
    return res



def convertFile(fileToConvert):
  if type(fileToConvert) is not str:
    raise TypeError("Please provide a valid file name")
  file = open(fileToConvert, "r")
  lines = file.readlines()
  convertedText = ''
  for line in lines:
    convertedText += convertText(line)
  return convertedText  

#print(convertText('हा सर्व कचरा स्त्री मुक्ती संघटनेच्या पुनर्वापर केंद्राकडे देण्यात आला'))