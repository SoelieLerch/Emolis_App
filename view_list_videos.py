import controller_login
from tkinter import *
from functools import partial
from PIL import Image,ImageTk
import tkinter.ttk as ttk
import view_play_video3
import os
second_view=0
button_last=0
button_next=0
def next(cpt2):
	global button_last, button_next, buttons, labels_title
	if button_last!=0:
		button_last.destroy()
		button_last=0
	if button_next!=0 :
		button_next.destroy()
		button_next=0
	i=0
	while(i<len(buttons)):
		buttons[i].destroy()
		labels_title[i].destroy()
		i=i+1
	cpt=cpt2
	title_view = Label ( second_view, text="Choisissez une vidéo pour voir les émotions en temps réel" )
	title_view.grid(column=1, row=0)
	response=controller_login.find_all_videos(20,cpt)
	response=response.json()
	if cpt !=0:
		del response[0]
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
		img= ImageTk.PhotoImage(master=second_view,file="temp_directory/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
		images.append(img)
		buttons.append(Button(second_view, image=images[i],command=partial(play, response[i])))
		buttons[i].grid(column=column, row=row)
		labels_title.append(Label(second_view, text=response[i]["Title"]))
		labels_title[i].grid(column=column, row=row+1)
		row=row+2
		i=i+1
	style = ttk.Style()
	style.layout('Left.TButton',[('Button.focus', {'children': [('Button.leftarrow', None),('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})]})])
	style.configure('Left.TButton',font=('','50','bold'), width=1, arrowcolor='blue')
	style.layout('Right.TButton',[('Button.focus', {'children': [('Button.rightarrow', None),('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})]})])
	style.configure('Right.TButton',font=('','50','bold'), width=1, arrowcolor='blue')
	print(response)
	if response[0]["id_video"]!=1:
		button_last=ttk.Button(second_view, style='Left.TButton', command=partial(next, cpt-1))
		button_last.grid(column=4, row=9)
	response2=controller_login.find_all_videos(20,cpt+1)
	response2=response2.json()
	print(response2)
	if response2!=[]:
		button_next=ttk.Button(second_view, style='Right.TButton', command=partial(next, cpt+1))
		button_next.grid(column=5, row=9)
	second_view.mainloop()

def play(video):
	global second_view
	second_view.destroy()
	view_play_video3.play_video(video, user_identity)

def display_all_videos(user):
	global second_view, user_identity, buttons, cpt, button_last, button_next, labels_title
	user_identity=user
	second_view = Tk()
	title_view = Label ( second_view, text="Choisissez une vidéo pour voir les émotions en temps réel" )
	title_view.grid(column=1, row=0)
	response=controller_login.find_all_videos(20,cpt)
	response=response.json()
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
		img= ImageTk.PhotoImage(master=second_view,file="temp_directory/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
		images.append(img)
		buttons.append(Button(second_view, image=images[i],command=partial(play, response[i])))
		buttons[i].grid(column=column, row=row)
		labels_title.append(Label(second_view, text=response[i]["Title"]))
		labels_title[i].grid(column=column, row=row+1)
		row=row+2
		i=i+1
	style = ttk.Style()
	style.layout('Left.TButton',[('Button.focus', {'children': [('Button.leftarrow', None),('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})]})])
	style.configure('Left.TButton',font=('','50','bold'), width=1, arrowcolor='blue')
	style.layout('Right.TButton',[('Button.focus', {'children': [('Button.rightarrow', None),('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})]})])
	style.configure('Right.TButton',font=('','50','bold'), width=1, arrowcolor='blue')
	button_next=ttk.Button(second_view, style='Right.TButton', command=partial(next, cpt+1))
	button_next.grid(column=5, row=9)
	second_view.mainloop()
cpt=0