from tkinter import * 
import controller_login
from tkVideoPlayer import TkinterVideo
third_view=0
import os
import datetime
import subprocess
import os
import sys
import pygame
import time
import signal
duration=0
tk2=0
def ok():
	global tk2
	tk2.destroy()

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
    	if durate>=begin[i]and durate<=end[i]:
    		print(emotions[i])
    		canvas2.itemconfig(emotion_text, text=emotions[i])
    		break
    	i=i+1
    print(videoplayer.current_duration())
    duration.set(videoplayer.current_duration())
def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)
def seek(value):
    """ used to seek a specific timeframe """
    videoplayer.seek(int(value))



def start(canvas, file, title, id_video):
	global tk2, duration, videoplayer, end_time, progress_slider, end, begin, emotions, emotion_text, canvas2
	canvas2 = Canvas(third_view, width=800, height=50)
	rectangle_emotion=canvas2.create_rectangle(0,0, 800, 50)
	emotion_text=canvas2.create_text(400, 25, text="")
	canvas2.pack()
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
	videoplayer.play() # play the video
	pygame.mixer.music.play()
	duration=IntVar(canvas)
	progress_slider = Scale(canvas, variable=duration, from_=0, to=0, orient="horizontal", command=seek)
	progress_slider.pack()
	end_time = Label(canvas, text=str(datetime.timedelta(seconds=0)))
	end_time.pack(side="left")
	videoplayer.bind("<<Duration>>", update_duration)
	videoplayer.bind("<<SecondChanged>>", update_scale)
	videoplayer.bind("<<Ended>>", video_ended )
	
	transcripts_text=[]
	begin=[]
	end=[]
	emotions=[]
	response=[]
	i=0
	while(len(response))==50:
		response=controller_login.find_transcripts(id_video, 50, i)
		response=response.json()
		j=0
		while(j<len(response)):
			transcripts_text.append(response[j]["text"])
			begin.append(response[j]["begin_utterance"])
			end.append(response[j]["end_utterance"])
			response2=controller_login.get_emotions(1)
			response2=response2.json()
			k=0
			em=[]
			while(k<len(response2)):
				em.append(response2[k]["name"])
				k=k+1
			emotions.append(em)
			j=j+1
	response=controller_login.find_transcripts(id_video, 50, i)
	response=response.json()
	j=0
	while(j<len(response)):
		transcripts_text.append(response[j]["text"])
		begin.append(response[j]["begin_utterance"])
		end.append(response[j]["end_utterance"])
		response2=controller_login.get_emotions(response[j]["id_transcript"])
		response2=response2.json()
		k=0
		em=[]
		while(k<len(response2)):
			em.append(response2[k]["name"])
			k=k+1
		emotions.append(em)
		j=j+1
	j=1
	while(j<len(begin)):
		k=0
		while(k<len(emotions[j])):
			if emotions[j][k] in emotions[j-1] and emotions[j]==emotions[j-1]:
				del emotions[j][k]
			k=k+1
		if begin[j]<end[j-1]:
			del begin[j]
			end[j-1]=end[j]
			del end[j]
			transcripts_text[j-1]=transcripts_text[j-1]+"\n"+transcripts_text[j]
			del transcripts_text[j]
			emotions[j-1]=emotions[j-1]+emotions[j]
			emotions[j-1]=list(dict.fromkeys(emotions[j-1]))
			del emotions[j]
		j=j+1
	time_end=end[-1]

	
	third_view.mainloop()

def play_video(video):
	canvas=0
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
	start(canvas, "temp_directory/"+video["Path"].split("/")[-1], video["Title"], video["id_video"])
	third_view.mainloop()