
from PySide6.QtWidgets import QApplication, QMainWindow,QLabel, QPushButton, QToolButton, QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene,QGraphicsRectItem,QGraphicsTextItem
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtGui import QFont, QColor, QPen
from PySide6.QtCore import Qt
import PySide6.QtWidgets as QtWidgets
from functools import partial
global cpt, bool_before, bool_next, button_next, button_before
import os
import view_recommendation_video
import vlc
import controller_login
import threading
import view_recommendation_video
from PIL import Image
import view_list_videos, view_play_video2

class View_Recommendation_video(QMainWindow):
    def __init__(self,id_video, user):
        super().__init__()
        global forth_view, user_identity, video_ref
        video_ref=id_video
        user_identity=user
        self.setWindowTitle("New Window")
        self.setGeometry(0, 0, 1500, 600) 
        if user["physio"]==False :
        	user=controller_login.login_user("lambda")
        	user=user.json()
        response=controller_login.get_first_ranks(id_video, user["id_user"], 12)
        response=response.json()
        self.title_view = QLabel("Choisissez une vidéo recommandée pour voir les émotions en temps réel", self)
        self.title_view.setGeometry(10, 0, 500, 30)
        i=0
        self.buttons=[]
        self.labels_title=[]
        images=[]
        dir = 'temp_directory'
        for f in os.listdir(dir):
        	os.remove(os.path.join(dir, f))
        column=0
        row=0
        while(i<len(response)):
        	if i%4==0 and i>3:
        		column=column+1
        		row=0
        	response_picture=controller_login.download_picture("pictures/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
        	image_path = "temp_directory/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg"
        	print("response pictures")
        	image=Image.open(response_picture)
        	image.save(image_path)
        	isExist = os.path.exists("temp_directory")
        	if not isExist:
        		# Create a new directory because it does not exist
        		os.makedirs("temp_directory")
        	image = Image.open(image_path)
        	image = image.resize((125,100))
        	#Convert the image to PhotoImage
        	image = image.save(image_path)
        	self.buttons.append(QPushButton(self))
        	self.buttons[i].setGeometry(200*row+40, column*150+30, 125, 100)  # (x, y, width, height)
        	pixmap = QPixmap(image_path)
        	# Set the image as the icon for the button
        	self.buttons[i].setIcon(pixmap)
        	self.buttons[i].setIconSize(pixmap.size())
        	# Connect a slot to the button click event
        	self.buttons[i].clicked.connect(partial(self.play, response[i], i))
        	self.labels_title.append(QLabel(response[i]["Title"], self))
        	self.labels_title[i].setGeometry(200*row+40, column*150+130, 400, 30)
        	row=row+2
        	i=i+1
        self.button_return=QPushButton("Retour aux vidéos de références", self)
        self.button_return.setGeometry(30, 500, 300, 30)  # (x, y, width, height)
        # Connect button click signal to the login slot
        self.button_return.clicked.connect(self.return_menu)
    def return_menu(self):
    	window=view_list_videos.View_list_videos(user_identity,0)
    	window.show()
    	self.close()
    def play(self, video, rank):
    	view_play=view_play_video2.View_play_video(video, user_identity, rank)
    	self.close()
