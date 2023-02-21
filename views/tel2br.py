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
    st.markdown("<h1 style='text-align: left; color: White; margin-top: -80px;'>Telugu to Braille Conversion</h1>", unsafe_allow_html=True)
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
    "telg": [
        u"ಀ", u"ಁ", u"ం", u"ః", u"಄", u"అ", u"ఆ", u"ఇ", u"ఈ", u"ఉ", u"ఊ", u"ఋ", u"ಌ", u"಍", u"ఎ", u"ఏ", 
        u"ఐ", u"಑", u"ఒ", u"ఓ", u"ఔ", u"క", u"ఖ", u"గ", u"ఘ", u"ఙ", u"చ", u"ఛ", u"జ", u"ఝ", u"ఞ", u"ట", 						
        u"ఠ", u"డ", u"ఢ", u"ణ", u"త", u"థ", u"ద", u"ధ", u"న", u"಩", u"ప", u"ఫ", u"బ", u"భ", u"మ", u"య", 						 						
        u"ర", u"ಱ", u"ల", u"ళ", u"಴", u"వ", u"శ", u"ష", u"స", u"హ", u"క్ష", u"಻", u"಼", u"ಽ", u"ా", u"ి",  			
        u"ీ", u"ు", u"ూ", u"ృ", u"ౄ", u"೅", u"ె",u"ే", u"ై", u"೉", u"ొ", u"ో", u"ౌ", u"ౢ", u"೎", u"೏", 
        u"೐", u"೑", u"೒", u"೓", u"೔", u"ೕ", u"ೖ", u"೗", u"೘", u"೙", u"೚", u"೛", u"೜",u"్", u"ೞ", u"೟", 
        u"ౠ", u"ೡ", u"ೢ", u"ೣ", u"೤", u"೥", u"౦", u"౧", u"౨", u"౩", u"౪ ", u"౫", u"౬", u"౭", u"౮", u"౯", u"0 ", u"1 ", u"2 ", u"3 ", u"4 ", u"5 ", u"6 ", u"7 ", u"8 ", u"9 ",
        u"೰", u"ೱ", u"ೲ", u"ೳ", u"೴", u"೵", u"೶", u"೷", u"೸", u"೹", u"೺", u"೻", u"೼", u"೽", u"೾", u"೿",' ','!','"','#','$',
                '%','&','','(',')',
                '*','+',',','-','.',
                '/',' '
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
                '/',' '
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
        try:
            ind = charmap_iso15919["telg"].index(i)
            res += charmap_iso15919["Latn"][ind]
        except:
            continue
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

#print(convertText('రోడ్డేశామా లేదా! మహిళా సాఫ్ట్‌వేర్‌ ఇంజినీర్‌పై గ్యాంగ్‌'))

