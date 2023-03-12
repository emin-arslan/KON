import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import time
import cv2
import pyautogui
import numpy as np
from PIL import Image
from pytesseract import pytesseract
import requests
from threading import Thread
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.Qt import Qt
import pymongo
from PyQt5.QtWidgets import *
from datetime import datetime
from PyQt5.QtGui import QIcon

#Base variables
path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
bot_token = ""#bot token giriniz
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

#DB Connection
client = pymongo.MongoClient("connectionstring")
db = client.KON
col = db["serialkeys"]


#MessageBox
def show_critical_messagebox(text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
    
        # setting message for Message Box
        msg.setText(text)
        
        # setting Message box window title
        msg.setWindowTitle("Geçersiz Giriş")

        msg.setWindowIcon(QtGui.QIcon('close.ico'))
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        # start the app
        retval = msg.exec_()

#serial key check from database
def key_check(text):
    x = col.find_one({"serial_key": text })
    if x is not None:
        isKeyExpired =   abs  ( x['first_date'] -datetime.now() ) .days >= x['total_day']

        if isKeyExpired or not x['active']: 
            return -1 #kod süresi doldu.
        
        else:
            return ( x['total_day'] -  abs ( x['first_date'] -datetime.now() ) .days  ) #kod süresi geri dönüşü
    
    else:
        return -2 # girilen key hatalı


checkStatus = True
total_time = 0
temp_variable = ""
temp_time = 0
open = True 
leftday = 0
active = True
gb_serialkey =""
chat_id = ""
kAdi =""

# chat_id textfile check serialkey check from textfile [ BURDAKI SORUN ÇOZULMEDI TXT'DE SERIAL KEY OLDUGUNDA OKUYAMIYORUZ.]
##textfile=0
serialkey=""
def check_empty_line(file_path):
    global serialkey
    global gb_serialkey
    global chat_id
    with __builtins__.open(file_path) as file:
        lines = file.readlines()
        if len(lines) == 0:
            print("Dosya boş")
        elif not lines[0].strip():
            print("1. satır boş")
        elif len(lines) > 1 and not lines[1].strip():
            print("2. satır boş")
        else:
            print("everything is ok.")
            serialkey = lines[2]
            chat_id = lines[0]
            kAdi = lines[1]
            gb_serialkey = serialkey




#write to chat_id txt for serialkeys
def write_to_txt(s_Key):
    gb_serialkey = s_Key
    with __builtins__.open("chat_id.txt", 'r') as file:
        lines = file.readlines()
        print(len(lines))
        if len(lines) > 2: 
            lines[2] = s_Key 
        else:
            lines.append("\n"+"\n"+s_Key)
    with __builtins__.open("chat_id.txt", 'w') as file:
        file.writelines(lines)
    return True

#kullanıcı adı , telegram_ id form
class MyDialog(QDialog):
    global chat_id
    global kAdi
    def on_button_clicked(self):
        with __builtins__.open("chat_id.txt", 'r') as f:
            lines = f.readlines()

        lines[1] = str(self.lineedit_1.text()) +"\n"
        lines[0] = str(self.lineedit_2.text()) + "\n"
        chat_id = lines[0]
        kAdi = lines[1]
        with __builtins__.open("chat_id.txt", "w") as f:
            f.writelines(lines)
        show_critical_messagebox('Ayarlarınız kaydedildi.')

    def __init__(self):
        super().__init__()


        self.layout = QVBoxLayout()
        
        self.label_1 = QLabel("İstediğiniz bir kullanıcı adı :")
        self.layout.addWidget(self.label_1)
        
        self.lineedit_1 = QLineEdit()
        self.layout.addWidget(self.lineedit_1)
        
        self.label_2 = QLabel("Telegram chat id:")
        self.layout.addWidget(self.label_2)
        
        self.lineedit_2 = QLineEdit()
        self.layout.addWidget(self.lineedit_2)

        self.button = QPushButton("Kaydet")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.on_button_clicked )
        

        self.setLayout(self.layout)  



class FramelessWindow(QtWidgets.QWidget):
    
    check_empty_line("chat_id.txt")

    def on_button_clicked(self):
        dialog = MyDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            data1 = dialog.line_edit1.text()
            data2 = dialog.line_edit2.text()
            print(data1, data2)
    def __init__(self):
        global f
        global x
        global leftday
        global gb_serialkey
        global open
        global serialkey
        global k

        super().__init__()
        self.setWindowIcon(QtGui.QIcon('mainicon.png'))
        self.setWindowOpacity(0.9)
        
        while (open):
            print(serialkey)
            if serialkey == "":
                
                text, ok = QtWidgets.QInputDialog.getText(self, 'Serial Key', 'Serial Key giriniz:')

                if ok == True and text !='':

                    if key_check(text) == -1:
                        show_critical_messagebox('Kodun süresi doldu.Uzatmak için konotification.com !')

                    elif key_check(text) >=0:
                        leftday = key_check(text)
                        open = False
                        gb_serialkey = text
                        if write_to_txt(text):
                            pass 
                        else:
                            print('hata')

                    elif key_check(text) == -2:
                        show_critical_messagebox('Girmiş olduğunuz key hatalı!')

                elif ok == False:
                    sys.exit(0)

                else :
                    show_critical_messagebox('Lütfen key giriniz.')
            else:

                if key_check(serialkey) == -1:
                    show_critical_messagebox('Kodun süresi doldu.Uzatmak için konotification.com !')
                    serialkey = ""
                elif key_check(serialkey) >= 0:
                    leftday = key_check(serialkey)
                    gb_serialkey = serialkey
                    open = False
                elif key_check(serialkey) == -2:
                    show_critical_messagebox('Kayıtlı key hatalı veya süresi geçmiş.Lütfen yeni key alınız.')
                    serialkey = ""



        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 300, 300)
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 20, 20)

        self.setMask(QtGui.QRegion(path.toFillPolygon().toPolygon()))

        self.is_dragging = False
        
        myFont=QtGui.QFont("Roboto ",10)
        myFont.setBold(True)    

        self.logo = QtWidgets.QLabel(self)
        self.logo.setGeometry(self.width() - 35, 5, 30, 30)
        self.logo.setPixmap(QtGui.QPixmap("error.png"))
        self.logo.mousePressEvent = self.close

        # self.settingspng = QtWidgets.QLabel(self)
        # self.settingspng.setGeometry(self.width() -62, 5, 30, 30)
        # self.settingspng.setPixmap(QtGui.QPixmap("settings.png"))
        self.button =QtWidgets.QPushButton(self)
        self.button.clicked.connect(self.on_button_clicked)
        self.button.setGeometry(self.width() -62, 5, 30, 30)
        self.button.setIcon(QIcon("settings.png"))
        self.button.setFlat(True)
        #self.setCentralWidget(self.button)
        #self.button.setGeometry(10, 10, 10, 10)



       
       


    #LABELS & TEXTBOXS
        self.X1label= QtWidgets.QLabel("X1:", self)
        self.X1label.setGeometry(28,85,30,25)
        self.X1label.setStyleSheet('color: #9B9191')
        self.X1label.setFont(myFont)

        self.Y11label= QtWidgets.QLabel("Y1:", self)
        self.Y11label.setGeometry(90,85,30,25)
        self.Y11label.setStyleSheet('color: #9B9191')
        self.Y11label.setFont(myFont)

        
        self.label = QtWidgets.QLabel('Knight Online Notification', self)
        self.label.setGeometry(int(self.width() / 2)-80,25,200,20)
        self.label.setFont(myFont)

        self.seriallabel = QtWidgets.QLabel('Serial Key kalan süre: '+ str(leftday), self)
        self.seriallabel.setGeometry(int(self.width() / 2)-80, self.height() - 20 ,170,20)
        self.seriallabel.setStyleSheet("color: #9B9191")
        self.seriallabel.setFont(myFont)

        self.textboxX1=QtWidgets.QLineEdit(self)
        self.textboxX1.setGeometry(50,85,30,25)
        self.textboxX1.setStyleSheet("border: 2px solid #9B9191;")
        self.textboxX1.setEnabled(False)

        self.textboxY1=QtWidgets.QLineEdit(self)
        self.textboxY1.setGeometry(115,85,30,25)
        self.textboxY1.setStyleSheet("border: 2px solid #9B9191;")
        self.textboxY1.setEnabled(False)


        self.X2label= QtWidgets.QLabel("X2:", self)
        self.X2label.setGeometry(28,135,30,25)
        self.X2label.setStyleSheet('color: #9B9191')
        self.X2label.setFont(myFont)

        self.Y21label= QtWidgets.QLabel("Y2:", self)
        self.Y21label.setGeometry(90,135,30,25)
        self.Y21label.setStyleSheet('color: #9B9191')
        self.Y21label.setFont(myFont)


        self.textboxX2=QtWidgets.QLineEdit(self)
        self.textboxX2.setGeometry(50,135,30,25)
        self.textboxX2.setStyleSheet("border: 2px solid #9B9191;")
        self.textboxX2.setEnabled(False)

        self.textboxY2=QtWidgets.QLineEdit(self)
        self.textboxY2.setGeometry(115,135,30,25)
        self.textboxY2.setStyleSheet("border: 2px solid #9B9191;")
        self.textboxY2.setEnabled(False)
    #END LABELS & TEXBOXS      
    #listbox

        self.listWidget =QtWidgets.QLineEdit(self)
        self.listWidget.setStyleSheet("border: 2px solid #9B9191;")
        self.listWidget.setGeometry(170,70,120,100)
        self.listWidget.setEnabled(False)
        #self.listwidget.show()


        self.pic = QtWidgets.QLabel(self)
        self.pic.setGeometry(60, 120, 200, 200)
        self.pic.setPixmap(QtGui.QPixmap("image1.png"))

        self.logo = QtWidgets.QLabel(self)
        self.logo.setGeometry(0,0, 60, 60)
        self.logo.setPixmap(QtGui.QPixmap("mainicon.png"))
        self.logo.setScaledContents(True);
     



    #Kısa yol tuş algılama , shorcut key press check
    def keyPressEvent(self, event):
            
            if event.key() == Qt.Key_F:
                [X1, Y1] = pyautogui.position()
                self.textboxX1.setText(str(X1))
                self.textboxY1.setText(str(Y1))
                self.listWidget.setText("X1, Y1 kaydedildi.")

            elif event.key() == Qt.Key_L:
                [X2, Y2] = pyautogui.position()
                self.textboxX2.setText(str(X2))
                self.textboxY2.setText(str(Y2))
                self.listWidget.setText("X2, Y2 kaydedildi.")

            elif event.key() == Qt.Key_S:
                self.listWidget.setText("Program başlatildi.")
                checkStatus = True
                total_time = 0
                temp_variable = ""
                temp_time = 0
                Thread(target = self.image_check).start()
        
            elif event.key() == Qt.Key_P:
                self.listWidget.setText(" Program durduruldu.")
                checkStatus = False
                total_time = 0
                temp_variable = ""
                temp_time = 0
                total_count = 0
                
            elif event.key() == Qt.Key_X:
                checkStatus = False
                self.close(self)
                sys.exit(self)
                
    #drag drop move functions            
    #Left mouse button press check and dragging true
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPos() - self.pos()
            event.accept()
  
    #left mouse button press and drag
    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.is_dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    #Left mouse button press check and dragging false
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.is_dragging = False

    #Form colors
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor("#D9D9D9"), 5))
        painter.fillRect(0, 0, self.width(), 50, QtGui.QColor("#D9D9D9"))
        painter.drawRect(0, 0, self.width(), 50)



#image check
    def image_check(self):
        global gb_serialkey
        global checkStatus
        global total_time
        global total_count
        global temp_variable
        global temp_time
        global image
        global X1,Y1,X2,Y2
        X1 = self.textboxX1.text()
        X2 = self.textboxX2.text()
        Y1 = self.textboxY1.text()
        Y2 = self.textboxY2.text()
        print("serial key=" + gb_serialkey)
        while checkStatus and key_check(gb_serialkey) > 0:
            print(key_check(gb_serialkey))
            # myquery = { "serial_key": { gb_serialkey } }
            # newvalues = { "$set": { "online": 'True' } }
            # col.update_one(myquery, newvalues)
            image = pyautogui.screenshot(region=(X1, Y1,int(X2)-int(X1),int(Y2)-int(Y1)) )
            image = cv2.cvtColor(np.array(image),
                    cv2.COLOR_RGB2BGR)
            cv2.imwrite("image1.png", image)
            path_to_image = 'image1.png'
            pytesseract.tesseract_cmd = path_to_tesseract
            img = Image.open(path_to_image)
            
            self.pic.setPixmap(QtGui.QPixmap("image1.png"))
            
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
                "text": "Merhaba "+kAdi+", toplamda "+str(total_time/60)+" dakikadir kutu alamadin. Lütfen hesabini kontrol et."
                }
                #self.listwidget.insert(0,'5 dk mesaji gönderildi.')
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
                        "text": "Merhaba "+kAdi+", "+str(temp_time)+" saniyedir kutu alamiyorsun. Eğer 5dk içerisinde başka kutu alamazsan tekrar bilgilendiriliceksin."
                            }
                    ##self.listwidget.insert(0,'120 sn mesaji gönderildi.')
                    response = requests.post(url, json=data)
                temp_time = 0
            time.sleep(10)

        self.listWidget.setText(' Süreniz bitmiş olabilir.')
        self.seriallabel.setText('Serial Key kalan süre: '+ str(key_check(gb_serialkey) ))
# end image check


app = QtWidgets.QApplication(sys.argv)
window = FramelessWindow()
window.show()

sys.exit(app.exec_())
