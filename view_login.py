from tkinter import *
import controller_login
from tkinter.ttk import *
import view_list_videos
main_view = Tk()
error_box_login=0

def login():
    response=controller_login.login_user(text_entry_login.get())
    if response.status_code==404:
    	global error_box_login
    	error_box_login=Toplevel(main_view)
    	error_login=Label ( error_box_login,text="'Erreur Login n'existe pas")
    	error_login.pack()
    	button_error_ok= Button(error_box_login, text="Ok", command = resolve_error) 
    	button_error_ok.pack()
    if response.status_code==200:
    	view_list_videos.display_all_videos(response.json())  
    	main_view.destroy()

def resolve_error():
	global error_box_login
	error_box_login.destroy()

def create_user():
	global error_box_login
	try :
		a=int(text_entry_age.get())
		Options=['Homme','Femme','Transgenre']
		if selection_genre.get() not in Options :
			error_box_login=Toplevel(main_view)
			error_login=Label ( error_box_login,text="'Erreur Sélectionnez un genre valide 'homme', 'femme' ou 'transgenre'")
			error_login.pack()
			button_error_ok= Button(error_box_login, text="Ok", command = resolve_error) 
			button_error_ok.pack()
		else :
			response=controller_login.create_user(text_entry_login.get(), text_entry_age.get(), selection_genre.get(), bool(value_button_login.get()))
			if response.status_code==405:
				error_box_login=Toplevel(main_view)
				error_login=Label ( error_box_login,text="'Erreur Login déjà existant")
				error_login.pack()
				button_error_ok= Button(error_box_login, text="Ok", command = resolve_error) 
				button_error_ok.pack()			
	except :
		error_box_login=Toplevel(main_view)
		error_login=Label ( error_box_login,text="Ecrire un age valide entier")
		error_login.pack()
		button_error_ok= Button(error_box_login, text="Ok", command = resolve_error) 
		button_error_ok.pack()
	if response.status_code==201:
		view_list_videos.display_all_videos(response.json())  
		main_view.destroy()

title = Label ( main_view, text="Bienvenue dans Emolis App, veuillez vous connecter ou créer un compte" )
title.pack()

text_login = Label ( main_view,text="Login")
text_login.pack()

text_entry_login = Entry( main_view, width=50)
text_entry_login.pack()

text_age = Label (main_view,text="Age (option si déjà inscrit")
text_age.pack()

text_entry_age = Entry( main_view, width=50)
text_entry_age.pack()

text_genre = Label ( main_view,text="Genre (option si déjà inscrit)")
text_genre.pack()

Options=['Homme','Femme','Transgenre']
selection_genre=Combobox(main_view,values=Options)
selection_genre.pack()

value_button_login=IntVar()

check_physio = Checkbutton(main_view, text = "Physio", width = 10, variable=value_button_login)
check_physio.pack()


button_login = Button(main_view, text="Se connecter", command = login) 
button_login.pack()

button_create_user = Button(main_view, text="Créer un compte", command = create_user) 
button_create_user.pack()



main_view.mainloop()



main_view.mainloop()