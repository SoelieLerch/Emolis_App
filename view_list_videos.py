import controller_login
from tkinter import *
from functools import partial
from PIL import Image,ImageTk
import view_play_video

second_view=0
def play(video):
	global second_view
	second_view.destroy()
	view_play_video.play_video(video)

def display_all_videos(user):
	global second_view
	second_view = Tk()
	title_view = Label ( second_view, text="Choisissez une vidéo pour voir les émotions en temps réel" )
	title_view.pack()
	response=controller_login.find_all_videos(50,0)
	response=response.json()
	i=0
	buttons=[]
	labels_title=[]
	images=[]
	while(i<len(response)):
		image = Image.open("pictures/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
		image = image.resize((125,100))
		#Convert the image to PhotoImage
		image = image.save("pictures/"+response[i]["Path"].split("/")[-1].split(".")[0]+".png")
		img= ImageTk.PhotoImage(master=second_view,file="pictures/"+response[i]["Path"].split("/")[-1].split(".")[0]+".png")
		images.append(img)
		buttons.append(Button(second_view, image=images[i],command=partial(play, response[i])))
		buttons[i].pack()
		labels_title.append(Label(second_view, text=response[i]["Title"]))
		labels_title[i].pack()
		i=i+1
	second_view.mainloop()
