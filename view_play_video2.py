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
import view_notation


duration=0
tk2=0
def ok():
	global tk2
	tk2.destroy()

def notate():
	third_view.destroy()
	view_notation.notate(id_video_ref, video_reco, user, rank_video)


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



def start(canvas, file, title, id_video, login, video_ref, rank):
	global tk2, duration, videoplayer, end_time, progress_slider, end, begin, emotions, canvas2, rectangles_joie, rectangles_colere, rectangles_surprise, rectangles_neutre, rectangles_degout, rectangles_tristesse, rectangles_peur, emotion_text, id_video_ref, user, video_reco, rank_video
	rank_video=rank
	id_video_ref=video_ref
	video_reco=id_video
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
	button_reco=Button(canvas, text="Noter",command=notate)
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

def play_video(video_ref, video, user, rank):
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
	start(canvas, "temp_directory/"+video["Path"].split("/")[-1], video["Title"], video["id_video"], user, video_ref, rank)
	third_view.mainloop()