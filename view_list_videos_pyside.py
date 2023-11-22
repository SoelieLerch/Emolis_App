from PySide6.QtWidgets import QApplication, QMainWindow,QLabel, QPushButton
from PySide6.QtGui import QPixmap
global cpt
import os
import controller_login
cpt=0
from PIL import Image
class View_list_videos(QMainWindow):
    def __init__(self, user):
        super().__init__()

        # Set window properties
        self.setWindowTitle("New Window")
        self.setGeometry(0, 0, 1500, 1000)  # (x, y, width, height)
        user_indentity=user
        self.title_view = QLabel("Choisissez une vidéo pour voir les émotions en temps réel", self)
        self.title_view.setGeometry(10, 0, 500, 30)
        response=controller_login.find_all_videos(20,cpt)
        response=response.json()
        i=0
        self.buttons=[]
        self.labels_title=[]
        images=[]
        dir = 'temp_directory'
        if os.path.exists(dir)==False:
        	os.makedirs(dir)
        for f in os.listdir(dir):
        	os.remove(os.path.join(dir, f))
        column=0
        row=0
        while(i<len(response)):
            if i%4==0 and i>3:
                column=column+1
                row=0
            response_picture=controller_login.download_picture("pictures/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg")
            print("response pictures")
            image_path = "temp_directory/"+response[i]["Path"].split("/")[-1].split(".")[0]+".jpg"  # Replace with the actual path to your image file
            image=Image.open(response_picture)
            image.save(image_path)
            isExist = os.path.exists("temp_directory")
            if not isExist:
                # Create a new directory because it does not exist
                os.makedirs("temp_directory")
            # Create a button with an image
            self.buttons.append(QPushButton(self))
            self.buttons[i].setGeometry(200*row+40, column*150+30, 125, 100)  # (x, y, width, height)
            # Load an image using QPixmap
            image = Image.open(image_path)
            image = image.resize((125,100))
            #Convert the image to PhotoImage
            image = image.save(image_path)
            pixmap = QPixmap(image_path)
            # Set the image as the icon for the button
            self.buttons[i].setIcon(pixmap)
            self.buttons[i].setIconSize(pixmap.size())
            # Connect a slot to the button click event
            self.buttons[i].clicked.connect(self.play)
            self.labels_title.append(QLabel(response[i]["Title"], self))
            self.labels_title[i].setGeometry(200*row+40, column*150+130, 400, 30)
            row=row+2
            i=i+1


    def play(self):
    	print("play")
