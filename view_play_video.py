from tkinter import * 
import controller_login
from tkVideoPlayer import TkinterVideo
third_view=0
import os

import subprocess
import os
import sys
import pygame


def get_audio (file) :
	filename, ext = os.path.splitext(file)
	subprocess.call(["ffmpeg", "-y", "-i", file,file.split(".")[0]+".mp3"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

def start(canvas, file):
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
	canvas2 = Canvas(third_view, width=800, height=50)
	canvas2.pack()
	rectangle= canvas2.create_rectangle(0,0, 800,50,fill='white')
	videoplayer.play() # play the video
	pygame.mixer.music.play()

def play_video(video):
	global third_view
	third_view=Tk()
	canvas = Canvas(third_view, width=800, height=550)
	canvas.pack()
	response=controller_login.download_movie(video["Path"].split("/")[-2]+"/"+video["Path"].split("/")[-1])
	movie=response.read() 
	file=open("temp_directory/"+video["Path"].split("/")[-1], "wb")
	file.write(movie)
	file.close()
	print("response")
	print(response.status_code)
	start(canvas, "temp_directory/"+video["Path"].split("/")[-1])
	


	third_view.mainloop()