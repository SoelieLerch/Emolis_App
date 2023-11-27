from PySide6.QtWidgets import QApplication, QMainWindow,QLabel, QPushButton, QToolButton, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene,QGraphicsRectItem,QGraphicsTextItem
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtGui import QFont, QColor, QPen
from PySide6.QtCore import Qt
import PySide6.QtWidgets as QtWidgets
from functools import partial
global cpt, bool_before, bool_next, button_next, button_before
import os
import vlc
import controller_login
import threading
cpt=0
bool_before=False
bool_next=True
button_next=0
button_before=0
from PIL import Image
import view_play_video
class View_list_videos(QMainWindow):
    def __init__(self,user,cpt2):
        super().__init__()
        cpt=cpt2
        # Set window properties
        self.setWindowTitle("New Window")
        self.setGeometry(0, 0, 1500, 1000)  # (x, y, width, height)
        global user_indentity
        user_indentity=user
        self.title_view = QLabel("Choisissez une vidéo pour voir les émotions en temps réel", self)
        self.title_view.setGeometry(10, 0, 500, 30)
        response=controller_login.find_all_videos(20,cpt)
        response=response.json()
        if  len(response)>20:
            del response[-1]
        i=0
        self.buttons=[]
        self.labels_title=[]
        images=[]
        dir = 'temp_directory'
        if os.path.exists(dir)==False:
            os.makedirs(dir)
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        column=0
        row=0
        while(i<len(response)):
            if i%4==0 and i>3:
                column=column+1
                row=0
            response_picture=controller_login.download_picture("pictures/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
            print("response pictures")
            image_path = "temp_directory/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg"  # Replace with the actual path to your image file
            image=Image.open(response_picture)
            image.save(image_path)
            isExist = os.path.exists("temp_directory")
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs("temp_directory")
            # Create a button with an image
            self.buttons.append(QPushButton(self))
            self.buttons[i].setGeometry(200*row+40, column*150+30, 125, 100)  # (x, y, width, height)
            # Load an image using QPixmap
            image = Image.open(image_path)
            image = image.resize((125,100))
            #Convert the image to PhotoImage
            image = image.save(image_path)
            pixmap = QPixmap(image_path)
            # Set the image as the icon for the button
            self.buttons[i].setIcon(pixmap)
            self.buttons[i].setIconSize(pixmap.size())
            # Connect a slot to the button click event
            self.buttons[i].clicked.connect(partial(self.play, response[i]))
            self.labels_title.append(QLabel(response[i]["Title"], self))
            self.labels_title[i].setGeometry(200*row+40, column*150+130, 400, 30)
            row=row+2
            i=i+1
        if response[0]["id_video"]!=1:
            self.button_next= QToolButton(self)
            self.button_next.setGeometry(6*240-100,column*150+170,50,50)  # (x, y, width, height)
            self.button_next.setObjectName('Right.TButton')
            self.button_next.setFont(QFont('', 50, QFont.Bold))
            self.button_next.setProperty('width', 1)
            self.button_next.setProperty('arrowcolor', QColor('blue'))
            self.button_next.setArrowType(Qt.LeftArrow)
            self.button_next.clicked.connect(partial(self.before, cpt-1))
        response2=controller_login.find_all_videos(20,cpt+1)
        response2=response2.json()
        if response2!=[]:
            self.button_before= QToolButton(self)
            self.button_before.setGeometry(6*240,column*150+170,50,50)  # (x, y, width, height)
            self.button_before.setObjectName('Right.TButton')
            self.button_before.setFont(QFont('', 50, QFont.Bold))
            self.button_before.setProperty('width', 1)
            self.button_before.setProperty('arrowcolor', QColor('blue'))
            self.button_before.setArrowType(Qt.RightArrow)
            self.button_before.clicked.connect(partial(self.next, cpt+1))

    def play(self,file):
        self.window3 =view_play_video.View_play_video(file, user_indentity)
        self.window3.show()
        self.close()

    def next(self, cpt2):
        self.close()
        window=View_list_videos(user_indentity, cpt2)
        window.show()
        print("next", cpt2)
    def before(self, cpt2):
        self.close()
        window=View_list_videos(user_indentity, cpt2)
        window.show()
        print("before", cpt2)