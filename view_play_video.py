from tkinter import * 
import controller_login
from tkVideoPlayer import TkinterVideo
third_view=0
import os
import datetime
import subprocess
import threading
import os
import sys
import pygame
import time
import signal
import view_recommendation_video
import PySide6.QtWidgets as QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QPushButton,QLabel, QGraphicsView, QGraphicsScene,QGraphicsRectItem,QGraphicsTextItem
from PySide6.QtGui import QPalette, QColor
import vlc
import gc
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QBrush, QColor, QPen
import sys
import threading
duration=0
tk2=0
class Canvas(QGraphicsView):
    def __init__(self, id_video):
        super(Canvas, self).__init__()

        self.scene = QGraphicsScene(self)
        self.setFixedSize(1000, 500)
        self.setScene(self.scene)

        # Créer un stylo pour dessiner sur le canevas
        self.pen = QPen(Qt.black)
        self.pen.setWidth(0)

        # Initialiser le mode de dessin à False
        self.drawing = False
        self.id_video=id_video
        self.draw_rectangle()
    def draw_rectangle(self):
    	self.label_item = QGraphicsTextItem()
    	self.label_item.setPos(0, 20)  # Initial position for the label
    	self.label_item.setPlainText("Joie")
    	self.scene.addItem(self.label_item)
    	self.label_item2 = QGraphicsTextItem()
    	self.label_item2.setPos(0, 70)  # Initial position for the label
    	self.label_item2.setPlainText("Colère")
    	self.scene.addItem(self.label_item2)
    	self.label_item3 = QGraphicsTextItem()
    	self.label_item3.setPos(0, 130)  # Initial position for the label
    	self.label_item3.setPlainText("Dégoût")
    	self.scene.addItem(self.label_item3)
    	self.label_item4 = QGraphicsTextItem()
    	self.label_item4.setPos(0, 190)  # Initial position for the label
    	self.label_item4.setPlainText("Peur")
    	self.scene.addItem(self.label_item4)
    	self.label_item5 = QGraphicsTextItem()
    	self.label_item5.setPos(0, 250)  # Initial position for the label
    	self.label_item5.setPlainText("Tristesse")
    	self.scene.addItem(self.label_item5)
    	self.label_item6 = QGraphicsTextItem()
    	self.label_item6.setPos(0, 310)  # Initial position for the label
    	self.label_item6.setPlainText("Surprise")
    	self.scene.addItem(self.label_item6)
    	self.label_item7 = QGraphicsTextItem()
    	self.label_item7.setPos(0, 360)  # Initial position for the label
    	self.label_item7.setPlainText("Neutre")
    	self.scene.addItem(self.label_item7)
    	transcripts_text=[]
    	self.begin=[]
    	self.end=[]
    	self.emotions=[]
    	response=[]
    	i=0
    	response=controller_login.find_transcripts(self.id_video, 100, i)
    	response=response.json()
    	print(len(response))
    	j=0
    	while(j<len(response)):
    		transcripts_text.append(response[j]["text"])
    		self.begin.append(response[j]["begin_utterance"])
    		self.end.append(response[j]["end_utterance"])
    		response2=controller_login.get_labels(response[j]["id_transcript"])
    		response2=response2.json()
    		k=0
    		em=[]
    		while(k<len(response2)):
    			em.append(response2[k]["name"])
    			k=k+1
    		self.emotions.append(em)
    		j=j+1
    	time_end=self.end[-1]
    	self.rectangles_joie=[]
    	i=0
    	while(i<len(self.begin)):
    		print("begin")
    		print(self.begin[i])
    		print(self.end[i])
    		print(self.emotions[i])
    		if self.end[i]==self.begin[i]:
    			self.end[i]=self.end[i]+1
    		rect = QGraphicsRectItem(self.begin[i]*730/time_end+70,0,(self.end[i]-self.begin[i])*730/time_end,50)
    		rect.setPen(self.pen)
    		self.rectangles_joie.append(rect)
    		self.scene.addItem(rect)
    		i=i+1
    	self.rectangles_colere=[]
    	i=0
    	while(i<len(self.begin)):
    		print("begin")
    		print(self.begin[i])
    		print(self.end[i])
    		print(self.emotions[i])
    		if self.end[i]==self.begin[i]:
    			self.end[i]=self.end[i]+1
    		rect = QGraphicsRectItem(self.begin[i]*730/time_end+70,60,(self.end[i]-self.begin[i])*730/time_end,50)
    		rect.setPen(self.pen)
    		self.rectangles_colere.append(rect)
    		self.scene.addItem(rect)
    		i=i+1
    	self.rectangles_degout=[]
    	i=0
    	while(i<len(self.begin)):
    		print("begin")
    		print(self.begin[i])
    		print(self.end[i])
    		print(self.emotions[i])
    		if self.end[i]==self.begin[i]:
    			self.end[i]=self.end[i]+1
    		rect = QGraphicsRectItem(self.begin[i]*730/time_end+70,120,(self.end[i]-self.begin[i])*730/time_end,50)
    		rect.setPen(self.pen)
    		self.rectangles_degout.append(rect)
    		self.scene.addItem(rect)
    		i=i+1
    	self.rectangles_peur=[]
    	i=0
    	while(i<len(self.begin)):
    		print("begin")
    		print(self.begin[i])
    		print(self.end[i])
    		print(self.emotions[i])
    		if self.end[i]==self.begin[i]:
    			self.end[i]=self.end[i]+1
    		rect = QGraphicsRectItem(self.begin[i]*730/time_end+70,180,(self.end[i]-self.begin[i])*730/time_end,50)
    		rect.setPen(self.pen)
    		self.rectangles_peur.append(rect)
    		self.scene.addItem(rect)
    		i=i+1
    	self.rectangles_tristesse=[]
    	i=0
    	while(i<len(self.begin)):
    		print("begin")
    		print(self.begin[i])
    		print(self.end[i])
    		print(self.emotions[i])
    		if self.end[i]==self.begin[i]:
    			self.end[i]=self.end[i]+1
    		rect = QGraphicsRectItem(self.begin[i]*730/time_end+70,240,(self.end[i]-self.begin[i])*730/time_end,50)
    		rect.setPen(self.pen)
    		self.rectangles_tristesse.append(rect)
    		self.scene.addItem(rect)
    		i=i+1
    	self.rectangles_surprise=[]
    	i=0
    	while(i<len(self.begin)):
    		print("begin")
    		print(self.begin[i])
    		print(self.end[i])
    		print(self.emotions[i])
    		if self.end[i]==self.begin[i]:
    			self.end[i]=self.end[i]+1
    		rect = QGraphicsRectItem(self.begin[i]*730/time_end+70,300,(self.end[i]-self.begin[i])*730/time_end,50)
    		rect.setPen(self.pen)
    		self.rectangles_surprise.append(rect)
    		self.scene.addItem(rect)
    		i=i+1
    	self.rectangles_neutre=[]
    	i=0
    	while(i<len(self.begin)):
    		print("begin")
    		print(self.begin[i])
    		print(self.end[i])
    		print(self.emotions[i])
    		if self.end[i]==self.begin[i]:
    			self.end[i]=self.end[i]+1
    		rect = QGraphicsRectItem(self.begin[i]*730/time_end+70,360,(self.end[i]-self.begin[i])*730/time_end,50)
    		rect.setPen(self.pen)
    		self.rectangles_neutre.append(rect)
    		self.scene.addItem(rect)
    		i=i+1


def MyThread():

    global playing
    playing=True
    time_current=0
    while(playing):
    	durate=incvalue()
    	print(durate)
    	print(canvas.begin[time_current])
    	print(canvas.end[time_current])
    	if durate>canvas.end[time_current]  and time_current<len(canvas.begin):
    		time_current=time_current+1
    	if "Joie" in canvas.emotions[time_current]:
    		brush_color = QColor(255, 255, 0)
    		canvas.rectangles_joie[time_current].setBrush(brush_color)
    	if "Colère" in canvas.emotions[time_current]:
    		brush_color = QColor(255, 0, 0)
    		canvas.rectangles_colere[time_current].setBrush(brush_color)
    	if "Tristesse" in canvas.emotions[time_current]:
    		brush_color = QColor(0, 0,255)
    		canvas.rectangles_tristesse[time_current].setBrush(brush_color)
    	if "Dégoût" in canvas.emotions[time_current]:
    		brush_color = QColor(107, 142,35)
    		canvas.rectangles_degout[time_current].setBrush(brush_color)
    	if "Peur" in canvas.emotions[time_current]:
    		brush_color = QColor(128, 0,128)
    		canvas.rectangles_peur[time_current].setBrush(brush_color)
    	if "Surprise" in canvas.emotions[time_current]:
    		brush_color = QColor(255, 165,0)
    		canvas.rectangles_surprise[time_current].setBrush(brush_color)
    	if "Neutre" in canvas.emotions[time_current]:
    		brush_color = QColor(128, 128,128)
    		canvas.rectangles_neutre[time_current].setBrush(brush_color)




def incvalue():
	time_current=player.get_time()//1000
	return time_current


def recommendation():
	global window, playing
	playing=False
	myThread.join(1)
	if myThread.is_alive():
		print("alive")
	else :
		print("no alive")
	player.pause()
	player.stop()
	player.release()
	window.close()
	#destruction du player
	view_recommendation_video.recommendation_video(id_video_ref, user)





def start(file, title, id_video, login):
	global window, user, id_video_ref, progressBar, player, myThread, canvas
	id_video_ref=id_video
	user=login
	Instance = vlc.Instance()
	player = Instance.media_player_new()
	Media = Instance.media_new(file)
	player.set_media(Media)
	vlcApp = QtWidgets.QApplication([])
	window =  QWidget()
	window.resize(800,1000)
	vlcWidget = QtWidgets.QFrame()
	vlcWidget.resize(800,500)
	layout= QVBoxLayout()
	layout.addWidget(vlcWidget)
	button_reco =  QPushButton("Recommandation")
	button_reco.setFixedSize(150,50)
	button_reco.clicked.connect(recommendation)
	layout.addWidget(button_reco)
	canvas=Canvas(id_video)
	layout.addWidget(canvas)
	window.setLayout(layout)
	window.show()
	player.set_nsobject(vlcWidget.winId())
	player.play()
	myThread=threading.Thread(target=MyThread)
	myThread.start()
	vlcApp.exec_()

def play_video(video, user):
	canvas=0
	response=controller_login.download_movie(video["Path"].split("/")[-2]+"/"+video["Path"].split("/")[-1])
	movie=response.read() 
	file=open("temp_directory/"+video["Path"].split("/")[-1], "wb")
	file.write(movie)
	file.close()
	print("response")
	print(response.status_code)
	start("temp_directory/"+video["Path"].split("/")[-1], video["Title"], video["id_video"], user)