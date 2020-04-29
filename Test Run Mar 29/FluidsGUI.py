# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 23:37:09 2020

@author: Bjorn Funk
"""
from PIL import Image, ImageDraw, ImageFont
import Fluids
import kinetics as tempf
import heattransfer1 as ht1

#pressureF = Fluids.function(tempf.fun('T'),ht1.fun)[0]
pressureF = Fluids.function(500,450)[0]#DELETE and use ^
#pressureC = Fluids.function(ht1.fun,ht2.fun)[0]
pressureC = Fluids.coolant(500,450)[0] #DELETE and use ^


lineWidth = 20
wordLoc = 0

image = Image.open('FluidsModel.png')
draw = ImageDraw.Draw(image)

fontA = ImageFont.truetype('arial.ttf',20)
draw.text(xy = (0,wordLoc),text = "Fuel Loop(Pa)",fill = (0,0,0),font = fontA)

for i in range(len(pressureF)):
    wordLoc += lineWidth
    pressureF[i] = round(pressureF[i])
    draw.text(xy = (0,wordLoc),text = "Pressure F" +str(i)+": "+str(pressureF[i]),fill = (0,0,0),font = fontA)

wordLoc += 2*lineWidth

draw.text(xy = (0,wordLoc),text = "Coolant Loop(Pa)",fill = (0,0,0),font = fontA)
for i in range(len(pressureC)):
    wordLoc += lineWidth
    pressureC[i] = round(pressureC[i])
    draw.text(xy = (0,wordLoc),text = "Pressure C" +str(i)+": "+str(pressureC[i]),fill = (0,0,0),font = fontA)
 
image.save('FluidsModelNew.png')
