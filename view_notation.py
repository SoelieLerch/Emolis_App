import controller_login
from tkinter import *
from functools import partial
from PIL import Image,ImageTk
import tkinter.ttk as ttk
import view_play_video2
import os
global cpt
import view_recommendation_video
cpt=-1
def clicked1(event):
	global cpt
	canvas.itemconfig(star1, fill='yellow')
	canvas2.itemconfig(star2, fill='white')
	canvas3.itemconfig(star3, fill='white')
	canvas4.itemconfig(star4, fill='white')
	cpt=0
	print(cpt)

def clicked2(event):
	global cpt
	canvas.itemconfig(star1, fill='yellow')
	canvas2.itemconfig(star2, fill='yellow')
	canvas3.itemconfig(star3, fill='white')
	canvas4.itemconfig(star4, fill='white')
	cpt=1
	print(cpt)

def clicked3(event):
	global cpt
	canvas.itemconfig(star1, fill='yellow')
	canvas2.itemconfig(star2, fill='yellow')
	canvas3.itemconfig(star3, fill='yellow')
	canvas4.itemconfig(star4, fill='white')
	cpt=2
	print(cpt)

def clicked4(event):
	global cpt
	canvas.itemconfig(star1, fill='yellow')
	canvas2.itemconfig(star2, fill='yellow')
	canvas3.itemconfig(star3, fill='yellow')
	canvas4.itemconfig(star4, fill='yellow')
	cpt=3
	print(cpt)


def notate_reco():
	global cpt
	note=controller_login.note(cpt, user["id_user"], video_ref,video_reco, rank_video)
	view_recommendation_video.recommendation_video(video_ref, user)

def notate(id_video_ref, id_video_reco, id_user, rank):
	global star1, star2, star3, star4, canvas, canvas2, canvas3, canvas4, cpt, user, video_ref, video_reco, rank_video
	view_notate=Tk()
	user=id_user
	video_reco=id_video_reco
	video_ref=id_video_ref
	rank_video=rank
	label_notation=Label(view_notate, text=str("Noter la vidéo"))
	label_notation.grid(row=0, column=0)
	canvas=Canvas(view_notate, width=50, height=50)
	canvas2=Canvas(view_notate, width=50, height=50)
	canvas3=Canvas(view_notate, width=50, height=50)
	canvas4=Canvas(view_notate, width=50, height=50)
	star1=canvas.create_polygon([25,2,10,50,48,20,2,20,40,50], outline='black', fill='')
	star2=canvas2.create_polygon([25,2,10,50,48,20,2,20,40,50], outline='black', fill='')
	star3=canvas3.create_polygon([25,2,10,50,48,20,2,20,40,50], outline='black', fill='')
	star4=canvas4.create_polygon([25,2,10,50,48,20,2,20,40,50], outline='black', fill='')	
	canvas.bind ('<Button-1>', clicked1)
	canvas2.bind ('<Button-1>', clicked2)
	canvas3.bind ('<Button-1>', clicked3)
	canvas4.bind ('<Button-1>', clicked4)
	canvas.grid(row=1, column=0)
	canvas2.grid(row=1, column=1)
	canvas3.grid(row=1, column=2)
	canvas4.grid(row=1, column=3)

	label_star1=Label(view_notate, text="Pas du tout")
	label_star2=Label(view_notate, text="Un peu")
	label_star3=Label(view_notate, text="Beaucoup")
	label_star4=Label(view_notate, text="Parfaitement")
	label_star1.grid(row=2, column=0)
	label_star2.grid(row=2, column=1)
	label_star3.grid(row=2, column=2)
	label_star4.grid(row=2, column=3)
	button_note=Button(view_notate, text="noter", command=notate_reco)
	button_note.grid(row=3, column=3)
	view_notate.mainloop()