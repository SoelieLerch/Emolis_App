import controller_login
from functools import partial
import os
global cpt
import view_recommendation_video
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsWidget, QGraphicsProxyWidget, QLabel,QGraphicsEllipseItem, QGraphicsPolygonItem,QGraphicsTextItem, QPushButton
from PySide6.QtGui import QColor, QPolygonF
from PySide6.QtCore import Qt, QPointF
import view_recommendation_video
cpt=-1


class ClickableStar(QGraphicsPolygonItem):
    def __init__(self, x, y, i):
        star_polygon = QPolygonF([
            QPointF(25, 2), QPointF(10, 50),
            QPointF(48, 20), QPointF(2, 20),
            QPointF(40, 50),
        ])
        self.num=i
        super(ClickableStar, self).__init__(star_polygon)
        self.setPos(x, y)
        self.setFlag(QGraphicsPolygonItem.ItemIsSelectable, True)
        self.setBrush(QColor("white"))
        self.identity=i

    def mousePressEvent(self, event):
        if booleans[self.identity]==False:
        	booleans[self.identity]=True
        	i=0
        	while(i<=self.identity):
        		stars[i].setBrush(QColor("yellow"))
        		i=i+1
        	while(i<len(stars)):
        		stars[i].setBrush(QColor("white"))
        		i=i+1
        else :
        	booleans[self.identity]=False
        	i=0
        	while(i<self.identity):
        		stars[i].setBrush(QColor("yellow"))
        		i=i+1
        	while(i<len(stars)):
        		stars[i].setBrush(QColor("white"))
        		i=i+1



class View_notate(QMainWindow):
    def __init__(self, id_video_ref, id_video_reco, id_user, rank):
        super().__init__()

        # Set window properties
        global user,video_ref,video_reco, rank_video
        user=id_user
        video_reco=id_video_reco
        video_ref=id_video_ref
        rank_video=rank
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 600, 300)
        label = QGraphicsTextItem("Notez la similarité émotionnelle entre la vidéo de référence et la vidéo d'origine !")
        label.setPos(30,0)
        self.scene.addItem(label)
        global stars, booleans
        booleans=[]
        stars=[]
        for i in range(4):
            star = ClickableStar(i * 80+150, 50, i)
            stars.append(star)
            booleans.append(False)
            self.scene.addItem(star)
        label = QGraphicsTextItem("Pas du tout")
        label.setPos(150,130)
        self.scene.addItem(label)
        label = QGraphicsTextItem("un peu")
        label.setPos(230,130)
        self.scene.addItem(label)
        label = QGraphicsTextItem("Beaucoup")
        label.setPos(310,130)
        self.scene.addItem(label)
        label = QGraphicsTextItem("Parfaitement")
        label.setPos(390,130)
        self.scene.addItem(label)
        button_notate = QPushButton("Notez")
        proxy_button = QGraphicsProxyWidget()
        proxy_button.setWidget(button_notate)
        proxy_button.setPos(200, 160)  # Adjust the position as needed

        # Connect the button click signal
        button_notate.clicked.connect(self.notate_reco)

        # Add the button to the first scene
        self.scene.addItem(proxy_button)

        self.view.show()
    def notate_reco(self):
    	global cpt
    	note=controller_login.note(cpt, user["id_user"], video_ref,video_reco, rank_video)
    	view_reco=view_recommendation_video.View_Recommendation_video(video_ref, user)
    	view_reco.show()
    	self.close()

