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

form = tk.Tk()
form.title('Knight Online Notification')
etiket = tk.Label(text='Knight Online Notification')
etiket.pack()



#labels
x1KordinalLbl = tk.Label(text="X1:")
y1KordinalLbl = tk.Label(text="Y1:")
x2KordinalLbl = tk.Label(text="X2:")
y2KordinalLbl = tk.Label(text="Y2:")

x1KordinalLbl.pack(side = "left")
y1KordinalLbl.pack(side = "left")

x1KordinalLbl.place(x = 20, y = 40)
y1KordinalLbl.place(x = 70, y = 40)

x2KordinalLbl.pack(side = "left")
y2KordinalLbl.pack(side = "left")

x2KordinalLbl.place(x = 20, y = 80)
y2KordinalLbl.place(x = 70, y = 80)
#end labels


#texts
x1KordinatText = tk.Entry()
y1KordinatText = tk.Entry()
x2KordinatText = tk.Entry()
y2KordinatText = tk.Entry()

x1KordinatText.pack(pady = 10)
y1KordinatText.pack(pady = 10)
x2KordinatText.pack(pady = 10)
y2KordinatText.pack(pady = 10)

x1KordinatText.place( width = 30, x = 40, y = 40)
y1KordinatText.place (width = 30, x = 90, y = 40)
x2KordinatText.place( width = 30, x = 40, y = 80)
y2KordinatText.place (width = 30, x = 90, y = 80)
#end texts


form.geometry('500x200')
form.wm_attributes('-alpha',0.9)

def key_press(event):

    if event.char == 'i':
        [X1, Y1] = pyautogui.position()
        x1KordinatText.insert(0,X1)
        y1KordinatText.insert(0,Y1)

    elif event.char == 's':
        [X2, Y2] = pyautogui.position()
        x2KordinatText.insert(0,X2)
        y2KordinatText.insert(0,Y2)
        
def key_released(e):
    pass

form.bind('<KeyPress>',key_press)
form.bind('<KeyRelease>',key_released )

form.mainloop()


while not keyboard.is_pressed('i'):
    pass

while not keyboard.is_pressed('i'):
    pass
    
total_time = 0
temp_time = 0
total_count = 0
temp_variable = ""
bot_token = '5964072304:AAH76k8bg8jH36ByMqwLUNoPFN3qedAYbZs'
chat_id = '2008213254'

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"


[X2, Y2] = pyautogui.position()

path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

while not keyboard.is_pressed('x'):

    image = pyautogui.screenshot(region=(X1, Y1, 200,20))
    image = cv2.cvtColor(np.array(image),
					cv2.COLOR_RGB2BGR)
    cv2.imwrite("image1.png", image)
    path_to_image = 'image1.png'
    time.sleep(3)
    pytesseract.tesseract_cmd = path_to_tesseract
    img = Image.open(path_to_image)
    
    try:
        text = pytesseract.image_to_string(img)
    except ValueError:
        data = {
            "chat_id": chat_id,
            "text": "Merhaba, Hesabinda oyundan düştüğü tespit edildi lütfen kontrol et.Program durduruldu."
            }
        response = requests.post(url, json=data)
        break


    if total_time % 300 == 0 and total_time >= 300:
        data = {
            "chat_id": chat_id,
            "text": "Merhaba, toplamda "+str(total_time/60)+" dakikadir kutu alamadin. Lütfen hesabini kontrol et."
            }
        response = requests.post(url, json=data)


    if temp_variable!=text:
        temp_variable = text
        temp_time = 0
        total_count = 0
        

    else:
        temp_time = temp_time + 3
        print(temp_time)
        if temp_time >= 60:
            
            if total_count >= 1:
                total_time = total_time + temp_time
            
            else:
                total_count = total_count + 1
                data = {
                "chat_id": chat_id,
                    "text": "Merhaba, "+str(temp_time)+" saniyedir kutu alamiyorsun. Eğer 5dk içerisinde başka kutu alamazsan tekrar bilgilendiriliceksin."
                        }
                response = requests.post(url, json=data)
            temp_time = 0
            
           








