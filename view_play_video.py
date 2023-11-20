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
<<<<<<< HEAD
	third_view.destroy()
	view_recommendation_video.recommendation_video(id_video_ref, user)


def get_audio (file) :
	filename, ext = os.path.splitext(file)
	subprocess.call(["ffmpeg", "-y", "-i", file,file.split(".")[0]+".mp3"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

def update_duration(event):
    """ updates the duration after finding the duration """
    duration = videoplayer.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration
def update_scale(event):
    """ updates the scale value """

    durate=videoplayer.current_duration()
    i=0
    while(i<len(begin)):
    	print(begin[i])
    	print(end[i])
    	if begin[i]<=durate and end[i]>=durate:
    		canvas2.itemconfig(emotion_text, text=emotions[i])
    		j=0
    		while(j<len(emotions[i])):
    			if emotions[i][j]=="Colère":
    				canvas2.itemconfig(rectangles_colere[i], fill='red')
    			if emotions[i][j]=="Joie":
    				canvas2.itemconfig(rectangles_joie[i], fill='yellow')
    			if emotions[i][j]=="Tristesse":
    				canvas2.itemconfig(rectangles_tristesse[i], fill='blue')
    			if emotions[i][j]=="Dégoût":
    				canvas2.itemconfig(rectangles_degout[i], fill='green')
    			if emotions[i][j]=="Peur":
    				canvas2.itemconfig(rectangles_peur[i], fill='purple')
    			if emotions[i][j]=="Surprise":
    				canvas2.itemconfig(rectangles_surprise[i], fill='orange')
    			if emotions[i][j]=="Neutre":
    				canvas2.itemconfig(rectangles_neutre[i], fill='grey')
    			j=j+1
    		break
    	i=i+1

    duration.set(videoplayer.current_duration())
def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    progress_slider.set(0)
def seek(value):
    """ used to seek a specific timeframe """
    videoplayer.seek(int(value))



def start(canvas, file, title, id_video, login):
	global tk2, duration, videoplayer, end_time, progress_slider, end, begin, emotions, canvas2, rectangles_joie, rectangles_colere, rectangles_surprise, rectangles_neutre, rectangles_degout, rectangles_tristesse, rectangles_peur, emotion_text, id_video_ref, user
	id_video_ref=id_video
	user=login
	canvas2 = Canvas(third_view, width=800, height=350)
	if not file.split(".")[0]+ ".mp3" in os.listdir("temp_directory"):
		get_audio(file)
	pygame.init()
	pygame.mixer.init()
	print(file.split(".")[0]+".mp3")
	pygame.mixer.music.load(file.split(".")[0]+".mp3")
	# root.geometry("640x480")
	videoplayer = TkinterVideo(master=canvas, scaled=False)
	videoplayer.load(file)
	videoplayer.set_size((800,500))
	videoplayer.bind("<<Loaded>>", lambda e: e.widget.config(width=800, height=500))
	videoplayer.pack()
	time_begin=time.time()
	duration=IntVar(canvas)
	progress_slider = Scale(canvas, variable=duration, from_=0, to=0, orient="horizontal", command=seek)
	progress_slider.pack()
	end_time = Label(canvas, text=str(datetime.timedelta(seconds=0)))
	end_time.pack(side="left")
	button_reco=Button(canvas, text="Recommandation",command=recommendation)
	button_reco.pack()
	videoplayer.bind("<<Duration>>", update_duration)
	videoplayer.bind("<<SecondChanged>>", update_scale)
	videoplayer.bind("<<Ended>>", video_ended )
	
	transcripts_text=[]
	begin=[]
	end=[]
	emotions=[]
	response=[]
	i=0
	while(len(response))==100:
		response=controller_login.find_transcripts(id_video, 100, i)
		response=response.json()
		j=0
		while(j<len(response)):
			transcripts_text.append(response[j]["text"])
			begin.append(response[j]["begin_utterance"])
			end.append(response[j]["end_utterance"])
			response2=controller_login.get_labels(response[j]["id_transcript"])
			response2=response2.json()
			k=0
			em=[]
			while(k<len(response2)):
				em.append(response2[k]["name"])
				k=k+1
			emotions.append(em)
			j=j+1
		i=i+1
	response=controller_login.find_transcripts(id_video, 100, i)
	response=response.json()
	print(len(response))

	j=0
	while(j<len(response)):
		transcripts_text.append(response[j]["text"])
		begin.append(response[j]["begin_utterance"])
		end.append(response[j]["end_utterance"])
		response2=controller_login.get_labels(response[j]["id_transcript"])
		response2=response2.json()
		k=0
		em=[]
		while(k<len(response2)):
			em.append(response2[k]["name"])
			k=k+1
		emotions.append(em)
		j=j+1
	emotion_text=canvas2.create_text(400, 10, text="")
	time_end=end[-1]
	rectangles_joie=[]
	i=0
	while(i<len(end)):
		rectangles_joie.append(canvas2.create_rectangle(begin[i]*800/time_end, 0,end[i]*800/time_end,50, outline=""))
		i=i+1
	canvas2.create_text(50, 25, text="Joie")
	rectangles_colere=[]
	i=0
	while(i<len(end)):
		rectangles_colere.append(canvas2.create_rectangle(begin[i]*800/time_end, 50,end[i]*800/time_end,100,outline="" ))
		i=i+1
	canvas2.create_text(50, 75, text="Colère")
	rectangles_degout=[]
	i=0
	while(i<len(end)):
		rectangles_degout.append(canvas2.create_rectangle(begin[i]*800/time_end, 100,end[i]*800/time_end,150, outline="" ))
		i=i+1
	canvas2.create_text(50, 125, text="Dégoût")
	rectangles_peur=[]
	i=0
	while(i<len(end)):
		rectangles_peur.append(canvas2.create_rectangle(begin[i]*800/time_end, 150,end[i]*800/time_end,200,outline="" ))
		i=i+1
	canvas2.create_text(50, 175, text="Peur")
	rectangles_tristesse=[]
	i=0
	while(i<len(end)):
		rectangles_tristesse.append(canvas2.create_rectangle(begin[i]*800/time_end, 200,end[i]*800/time_end,250,outline="" ))
		i=i+1
	canvas2.create_text(50, 225, text="Tristesse")
	rectangles_surprise=[]
	i=0
	while(i<len(end)):
		rectangles_surprise.append(canvas2.create_rectangle(begin[i]*800/time_end, 250,end[i]*800/time_end,300,outline="" ))
		i=i+1
	rectangles_neutre=[]
	canvas2.create_text(50, 275, text="Surprise")
	i=0
	while(i<len(end)):
		rectangles_neutre.append(canvas2.create_rectangle(begin[i]*800/time_end, 300,end[i]*800/time_end,350,outline="" ))
		i=i+1
	canvas2.create_text(50, 325, text="Neutre")
	canvas2.pack()
	videoplayer.play() # play the video
	pygame.mixer.music.play()
	third_view.mainloop()
=======
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
>>>>>>> 71e1d0e3c830168cc0e775c7d2c7e4305238377d

def play_video(video, user):
	canvas=0
	response=controller_login.download_movie(video["Path"].split("/")[-2]+"/"+video["Path"].split("/")[-1])
	movie=response.read() 
	file=open("temp_directory/"+video["Path"].split("/")[-1], "wb")
	file.write(movie)
	file.close()
	print("response")
	print(response.status_code)
<<<<<<< HEAD
	start(canvas, "temp_directory/"+video["Path"].split("/")[-1], video["Title"], video["id_video"], user)
	third_view.mainloop()
=======
	start("temp_directory/"+video["Path"].split("/")[-1], video["Title"], video["id_video"], user)
>>>>>>> 71e1d0e3c830168cc0e775c7d2c7e4305238377d
