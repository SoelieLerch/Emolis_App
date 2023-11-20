import controller_login
from tkinter import *
from functools import partial
from PIL import Image,ImageTk
import tkinter.ttk as ttk
import view_play_video2, view_list_videos
import os
def play(video, rank):
	global forth_view
	forth_view.destroy()
	view_play_video2.play_video(video_ref, video, user_identity, rank)

def return_menu():
	forth_view.destroy()
	view_list_videos.display_all_videos(user_identity)  

def recommendation_video(id_video, user):
	global forth_view, user_identity, video_ref
	video_ref=id_video
	user_identity=user
	forth_view = Tk()
	if user["physio"]==False :
		user=controller_login.login_user("lambda")
		user=user.json()
	response=controller_login.get_first_ranks(id_video, user["id_user"], 12)
	response=response.json()
	title_view = Label ( forth_view, text="Choisissez une vidéo recommandée pour voir les émotions en temps réel" )
	title_view.grid(column=1, row=0)
	i=0
	buttons=[]
	labels_title=[]
	images=[]
	dir = 'temp_directory'
	for f in os.listdir(dir):
		os.remove(os.path.join(dir, f))
	column=0
	row=1
	while(i<len(response)):
		if i%4==0:
			column=column+1
			row=1
		response_picture=controller_login.download_picture("pictures/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
		print("response pictures")
		image=Image.open(response_picture)
		image.save("temp_directory/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
		isExist = os.path.exists("temp_directory")
		if not isExist:
			# Create a new directory because it does not exist
			os.makedirs("temp_directory")
		image = Image.open("temp_directory/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
		image = image.resize((125,100))
		#Convert the image to PhotoImage
		image = image.save("temp_directory/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
		img= ImageTk.PhotoImage(master=forth_view,file="temp_directory/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
		images.append(img)
		buttons.append(Button(forth_view, image=images[i],command=partial(play, response[i], i)))
		buttons[i].grid(column=column, row=row)
		labels_title.append(Label(forth_view, text=response[i]["Title"]))
		labels_title[i].grid(column=column, row=row+1)
		row=row+2
		i=i+1
	Button_return=Button(forth_view, text="Retour aux vidéos de références", command=return_menu)
	Button_return.grid(column=1, row=10)
	forth_view.mainloop()

