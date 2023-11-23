from tkinter import *
import controller_login
from tkinter.ttk import *
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox

import view_list_videos_pyside
class Error_box(QMainWindow):
    def __init__(self, text):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Second Window")
        self.setGeometry(200, 200, 250, 100)  # (x, y, width, height)
        self.error_login = QLabel(text, self)
        self.error_login.setGeometry(30, 0, 270, 30)  # (x, y, width, height)
        self.button_error_ok = QPushButton("OK", self)
        self.button_error_ok.setGeometry(30, 30, 100, 30)  # (x, y, width, height)
        # Connect button click signal to the login slot
        self.button_error_ok.clicked.connect(self.resolve_error)
    def resolve_error(self):
    	self.close()


class View_login(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("My PySide Window")
        self.setGeometry(0, 0, 500, 300)  # (x, y, width, height)
        self.title = QLabel("Bienvenue dans Emolis App, veuillez vous connecter ou créer un compte", self)
        self.title.setGeometry(30, 0, 500, 30)  # (x, y, width, height)
        self.text_login = QLabel("Identifiant :", self)
        self.text_login.setGeometry(30, 30, 200, 30)  # (x, y, width, height)
        self.text_entry_login = QLineEdit(self)
        self.text_entry_login.setGeometry(220, 30, 100, 30)
        self.text_age = QLabel("Age : (option si déjà inscrit)", self)
        self.text_age.setGeometry(30, 60, 200, 30)  # (x, y, width, height)
        self.text_entry_age = QLineEdit(self)
        self.text_entry_age.setGeometry(220, 60, 100, 30)
        self.text_genre = QLabel("Genre : (option si déjà inscrit)", self)
        self.text_genre.setGeometry(30, 90, 200, 30)  # (x, y, width, height)
        self.selection_genre = QComboBox(self)
        self.selection_genre.setGeometry(220, 90, 100, 30)  # (x, y, width, height)
        self.selection_genre.addItems(["Homme", "Femme", "Transgenre"])       
        self.check_physio = QCheckBox("Physio", self)
        self.check_physio.setGeometry(30, 120, 100, 30)
        self.button_login = QPushButton("Se connecter", self)
        self.button_login.setGeometry(150, 150, 100, 30)  # (x, y, width, height)
        # Connect button click signal to the login slot
        self.button_login.clicked.connect(self.login)
        self.button_create_user = QPushButton("Créer un compte", self)
        self.button_create_user.setGeometry(280, 150, 150, 30)  # (x, y, width, height)
        # Connect button click signal to the login slot
        self.button_create_user.clicked.connect(self.create_user)
    def login(self):
        response=controller_login.login_user(self.text_entry_login.text())
        if response.status_code==404:
            global error_box
            error_box=Error_box("Erreur Login n'existe pas")
            error_box.show()
        elif response.status_code==200:
            global view_list_videos
            view_list_videos=view_list_videos_pyside.View_list_videos(response.json(),0)
            view_list_videos.show()
            self.close()
            print("ok")
            
    def create_user(self):
        global error_box
        try :
            a=int(self.text_entry_age.text())
            response=controller_login.create_user(self.text_entry_login.text(), self.text_entry_age.text(), self.selection_genre.currentText(), self.check_physio.isChecked())
            if response.status_code==405:
                error_box=Error_box("Erreur Login déjà existant")
                error_box.show()
            elif response.status_code==201:
                global view_list_videos
                view_list_videos=view_list_videos_pyside.View_list_videos(response.json(),0)
                view_list_videos.show()
                self.close()
        except:
            error_box=Error_box("Ecrire un age valide (nombre)")
            error_box.show()
        print("user")

if __name__ == "__main__":
    # Create the application instance
    app = QApplication([])

    # Create and show the main window
    window = View_login()
    window.show()

    # Start the application event loop
    app.exec()

