from PySide6.QtWidgets import QApplication, QMainWindow,QLabel
class View_list_videos(QMainWindow):
    def __init__(self, user):
        super().__init__()

        # Set window properties
        self.setWindowTitle("New Window")
        self.setGeometry(300, 300, 400, 200)  # (x, y, width, height)
        user_indentity=user
        self.title_view = QLabel("Choisissez une vidéo pour voir les émotions en temps réel", self)
        self.title_view.setGeometry(10, 0, 500, 30)

