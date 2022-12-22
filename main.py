from PIL import Image, ImageDraw, ImageFont
import math
import streamlit as st
import numpy as np

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?+~<>i!lI;:,\"^`'. "[::-1]
# chars = "#Wo- "[::-1]
charArray = list(chars)
charArray.reverse()
charLength = len(charArray)
interval = charLength/256

st.session_state['scale'] = 0.1

oneCharWidth = 10
oneCharHeight = 18

st.set_page_config(layout="wide")

def main():
    initSessionState()
    file=st.file_uploader("Select Image", type=None, accept_multiple_files=False, disabled=False, label_visibility="visible")
    st.session_state['scale']=st.slider('scalefactor',min_value=0.01, max_value=0.99, value=st.session_state['scale'], step=0.01, label_visibility="visible")
    if(file!=None):
        if(file.type!='image/png' and file.type!='image/jpeg'):
            file=None
            st.write("please use png or jpg")
        st.session_state['file']=file
        st.session_state['img']=Image.open(file)  
        st.session_state['output']=asciiArt(st.session_state['img'],st.session_state['scale'])
 
        drawpage()
          
def initSessionState():
    if 'file' not in st.session_state:
        st.session_state['file'] = 'value'
    if 'img' not in st.session_state:
        st.session_state['img'] = 'value'

def drawpage():
    with st.container():
        left,mid,right=st.columns([4,1,4])
        with left:
            st.image(st.session_state['img'])
        with right:
            try:
                st.image(Image.fromarray(np.uint8(st.session_state['output'])))
            except:
                pass

def getChar(inputInt):
    return charArray[math.floor(inputInt*interval)]

def asciiArt(im,scaleFactor):
    fnt = ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf', 15)
    width, height = im.size
    im = im.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
    width, height = im.size
    pix = im.load()

    outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = (30, 30, 30))
    d = ImageDraw.Draw(outputImage)

    for i in range(height):
        for j in range(width):
            try:
                r, g, b, o = pix[j, i]
            except:
                r,g,b=pix[j, i]
            h = int(r/3 + g/3 + b/3)
            pix[j, i] = (h, h, h)
            d.text((j*oneCharWidth, i*oneCharHeight), getChar(h), font = fnt, fill = (r, g, b))
    return outputImage
    
main()
