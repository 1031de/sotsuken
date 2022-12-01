from PIL import Image
from telnetlib import RCP
import streamlit as st
import numpy as np
import math
import cv2

image = cv2.imread('1124_s.jpg')
image1,image2 = st.beta_columns(2)
with image1:
    image1 = cv2.imread('1124_s.jpg')
    st.image(image1)
    
with image2:
    image2 = cv2.imread('1124_s.jpg')
    st.image(image2)

sl = st.slider('θ値', min_value=1,max_value=45)


if sl:
    height,width,_ = image.shape
    src = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
    k = sl
    k2 = math.radians(k)
    c = 3.25 #視差/2
    b = c / k2
    a = math.sqrt(b**2 + c**2)

    d = 30 # 目とスクリーンの距離(cm)
    ppi = 300        # デバイスのppiを設定する
    ppc = ppi / 2.54 # Pixels Per Centimeter (1inch = 2.54cm)
    rs = math.atan(c/b)

    deg = math.degrees(rs)
    print(rs)

    wid = width * b / a
    x = height / (1 + width * c / a / (d * ppc))
    h = (height - x) / 2 
    y1 = h
    y2 = height - h
    wx = width - wid

    tarl = np.float32([[wx, y1], [wx, y2], [width, height], [width, 0]])
    matl = cv2.getPerspectiveTransform(src,tarl)
    im = cv2.warpPerspective(image,matl,(width,height))

    tarr = np.float32([[0, 0], [0, height], [wid, y2], [wid, y1]])
    matr = cv2.getPerspectiveTransform(src,tarr)
    im2 = cv2.warpPerspective(image,matr,(width,height))

    new_image1 = im.copy()
    new_image1 = Image.fromarray(new_image1)
    image = new_image1
    print(st.image)

    new_image2 = im2.copy()
    new_image2 = Image.fromarray(new_image2)
    image = new_image2
    print(st.image)
    
from PIL import Image
from telnetlib import RCP
import streamlit as st
import numpy as np
import math

image = Image.open('1124_s.jpg')
st.image(image)

sl = st.slider('θ値', min_value=1,max_value=45)

if sl:
    height = image.height
    width = image.width
    src = (0, 0, 
           0,height,
           width, height, 
           width, 0)
        # b(立体物と画面の距離を入力してそれに応じて画像にどれだけの角度をつけたかを計算)
    k = sl
    k2 = math.radians(k)
    c = 3.25 #視差/2
    b = c / k2
    a = math.sqrt(b**2 + c**2)

    d = 30 # 目とスクリーンの距離(cm)
    ppi = 300        # デバイスのppiを設定する
    ppc = ppi / 2.54 # Pixels Per Centimeter (1inch = 2.54cm)
    rs = math.atan(c/b)

    deg = math.degrees(rs)
    print(rs)

    wid = width * b / a
    x = height / (1 + width * c / a / (d * ppc))
    h = (height - x) / 2 
    y1 = h
    y2 = height - h
    wx = width - wid

    tarl = (wx, y1, 
        wx, y2,
        width, height, 
        width, 0
    )

    image2 = src.transform(
        size=(height,width),
        method=Image.QUAD,
        data=tarl,
        resample=Image.BICUBIC,
        fill=1,
        fillcolor=None
    )

    st.image2