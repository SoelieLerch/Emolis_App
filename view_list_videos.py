import controller_login
from tkinter import *
def display_all_videos(user):
	main_view = Tk()
	title_view = Label ( main_view, text="Choisissez une vidéos pour voir les émotions en temps réel" )
	title_view.pack()
	response=controller_login.find_all_videos(0,50)
	print(response.json())
	pass