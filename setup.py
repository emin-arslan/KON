# Python program to take
# screenshots

import numpy as np
import cv2
import pyautogui
import keyboard
import time
from PIL import Image
from pytesseract import pytesseract
import telegram
import requests
import json
import tkinter as tk
from tkinter import *
from PIL import *
from PIL import ImageTk, Image
from threading import Thread
import sys

[X1, X2] = 10, 100
[Y1, Y2] = 10, 100
backgroundcolor = '#2E4E5A'
form = tk.Tk()
form.title('Knight Online Notification')
etiket = tk.Label(text='Knight Online Notification', bg = backgroundcolor, fg = "#FFFFFF", pady= 10 , font= ('Helvetica 8 bold'))
etiket.pack()

with open('chat_id.txt') as f:
    lines = f.readlines()

f.close()

checkStatus = True
mystrX1=StringVar()
mystrX2=StringVar()
mystrY1=StringVar()
mystrY2=StringVar()
total_time = 0
temp_time = 0
total_count = 0
checkThread = 0
temp_variable = ""

chat_id = lines[0]

bot_token = '' #bot token 
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



#labels
Label(form, text= "X1:", font= ('Helvetica 8 bold'), bg= backgroundcolor, fg='#FFFFFF', ).place(x = 20, y = 40)
Label(form, text= "Y1:", font= ('Helvetica 8 bold'), bg= backgroundcolor, fg='#FFFFFF').place(x = 70, y = 40)
Label(form, text= "X2:", font= ('Helvetica 8 bold'), bg= backgroundcolor, fg='#FFFFFF').place(x = 20, y = 80)
Label(form, text= "Y2:", font= ('Helvetica 8 bold'), bg= backgroundcolor, fg='#FFFFFF').place(x = 70, y = 80)

#end labels


#texts
x1KordinatText = tk.Entry(form,textvariable=mystrX1,state=DISABLED)

y1KordinatText = tk.Entry(form,textvariable=mystrY1,state=DISABLED)
x2KordinatText = tk.Entry(form,textvariable=mystrX2,state=DISABLED)
y2KordinatText = tk.Entry(form,textvariable=mystrY2,state=DISABLED)

x1KordinatText.pack(pady = 10)
y1KordinatText.pack(pady = 10)
x2KordinatText.pack(pady = 10)
y2KordinatText.pack(pady = 10)

x1KordinatText.place( width = 30, x = 40, y = 40)
y1KordinatText.place (width = 30, x = 90, y = 40)
x2KordinatText.place( width = 30, x = 40, y = 80)
y2KordinatText.place (width = 30, x = 90, y = 80)

logs = tk.Listbox()
logs.config(bg=backgroundcolor , fg='#FFFFFF' , font= ('Helvetica 8 bold') )
logs.pack()
logs.place(width = 150, x = 130 , y = 40, height=60 )

#end texts

#image panel
img = ImageTk.PhotoImage(Image.open("image1.png"))
image = img
panel = tk.Label(form, image=img,relief="groove" , width= 190, height= 30 , bg=backgroundcolor )
panel.pack(side = BOTTOM, pady=12)
# end image panel

# Image refresh function
def callback():
    img2 = ImageTk.PhotoImage(Image.open("image1.png"))
    panel.configure(image=img2)
    panel.image = img2

# check key press funciton
def key_press(event):
    global checkThread
    global checkStatus

    if event.char == 'f':
        [X1, Y1] = pyautogui.position()
        mystrX1.set(X1)
        mystrY1.set(Y1)
        logs.insert(0,'X1,Y1 kaydedildi.')

    elif event.char == 'l':
        [X2, Y2] = pyautogui.position()
        mystrX2.set(X2)
        mystrY2.set(Y2)
        logs.insert(0,'X2,Y2 kaydedildi.')

    elif event.char == 's':
        logs.insert(0,'Program başlatildi.')
        logs.insert(0,'Görseli kontrol edin.')
        checkStatus = True
        total_time = 0
        temp_variable = ""
        temp_time = 0
        Thread(target = image_check).start()
   
    elif event.char == 'p':
        checkStatus = False
        logs.insert(0,'Program durduruldu.')
        total_time = 0
        temp_variable = ""
        temp_time = 0
        total_count = 0
        
    elif event.char == 'x':
        logs.insert(0,'Program kapatiliyor.')
        checkStatus = False
        sys.exit(0)

# Read to image funciton
def image_check():
    global checkStatus
    global total_time
    global total_count
    global temp_variable
    global temp_time
    global image
    global X1,Y1,X2,Y2
    [X1, X2] = x1KordinatText.get(), x2KordinatText.get()
    [Y1, Y2] = y1KordinatText.get(), y2KordinatText.get()
    while checkStatus:
        image = pyautogui.screenshot(region=(X1, Y1,int(X2)-int(X1),int(Y2)-int(Y1)) )
        image = cv2.cvtColor(np.array(image),
                cv2.COLOR_RGB2BGR)
        cv2.imwrite("image1.png", image)
        path_to_image = 'image1.png'
        pytesseract.tesseract_cmd = path_to_tesseract
        img = Image.open(path_to_image)
        
        callback()
        
        try:
            text = pytesseract.image_to_string(img)
        except ValueError:
            data = {
            "chat_id": chat_id,
            "text": "Merhaba, Hesabinda oyundan düştüğü tespit edildi lütfen kontrol et.Program durduruldu."
            }


        if  total_time % 300 == 0 and total_time >= 300:
            data = {
            "chat_id": chat_id,
            "text": "Merhaba, toplamda "+str(total_time/60)+" dakikadir kutu alamadin. Lütfen hesabini kontrol et."
            }
            logs.insert(0,'5 dk mesaji gönderildi.')
            response = requests.post(url, json=data)


        if temp_variable!=text:
            temp_variable = text
            temp_time = 0
            total_count = 0
            total_time = 0
        else:
            temp_time = temp_time + 10
            total_time = total_time  + 10
            #logs.insert(0,temp_time)
        if temp_time >= 120:   
            if total_count < 1:
                total_count = total_count + 1
                data = {
                "chat_id": chat_id,
                    "text": "Merhaba "+lines[1]+", "+str(temp_time)+" saniyedir kutu alamiyorsun. Eğer 5dk içerisinde başka kutu alamazsan tekrar bilgilendiriliceksin."
                        }
                logs.insert(0,'120 sn mesaji gönderildi.')
                response = requests.post(url, json=data)
            temp_time = 0
        time.sleep(10)

  
# form attributes things  
form.attributes("-alpha", 0.9)
form.overrideredirect(1)      
lastClickX = 0
lastClickY = 0

def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

def Dragging(event):
    x, y = event.x - lastClickX + form.winfo_x(), event.y - lastClickY + form.winfo_y()
    form.geometry("+%s+%s" % (x , y))

def hide():
    form.withdraw()

def on_enter(e):
    myButton['background'] = 'green'

def on_leave(e):
    myButton['background'] = 'red'


form.bind('<KeyPress>',key_press)
form.geometry('300x150+500+300')
form.maxsize(300,150)
form.minsize(300,150)
form.overrideredirect(True)
form.attributes('-topmost', True)
form.bind('<Button-1>', SaveLastClickPos)
form.bind('<B1-Motion>', Dragging)
form['background']=backgroundcolor
Button(form, text="-", command=hide, width=2, height=1, bg=backgroundcolor,fg="#FFFFFF" ,font= ('Helvetica 8 bold'), borderwidth=1, cursor="hand2" , activebackground="#2497E9") .place(x=256,y=0)
myButton= Button(form, text="X", command=form.destroy, width=2, height=1, bg=backgroundcolor, fg="#FFFFFF" ,font= ('Helvetica 8 bold'), borderwidth=1, cursor="hand2", activebackground="#f00").place(x=278,y=0)
form.mainloop()     








