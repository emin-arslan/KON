# What we use software language 

This project was created with Python.

![konfoto](https://user-images.githubusercontent.com/126695865/227981413-1745c921-1c86-4065-90bf-bf1217f3691b.png)

Project interface supported by PyQt5.
Also we used tesseract to read text from the image.

# What does it do

This project supplies to read text from specific area on window.
Also the project sends to telegram app the text


# How to use

1-) First of all, if you don't have tesseract , u have to install tesseract.

2-) You have to get telegram api key and bot token.

3-) Write to api key and bot token in gui.py 

4-) There is a serial key check  when you  try to open the app

5-) That keys come from database so u have to connect between database and app.(There is tag for database connection in Gui.py)

7-) We have got hotkeys ; \
    "f" : save first x and y coordinates \
    "l" : save last x and y coordinates \
    "s" : start to app \
    "p" : pause app \
    "x" : exit from app  \
    If you want to use this app , u have to use hotkeys \
