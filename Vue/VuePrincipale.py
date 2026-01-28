import sys
from PySide6.QtWidgets import *

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, QAction
from PySide6 import QtGui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barre latérale fixe - PySide6")
        self.setWindowIcon(QIcon("icons/file.png"))
        self.resize(800, 500)
        self.createMenuBar()
        # Layout principal horizontal
        main_layout = QHBoxLayout(self)

        # selection d'un client
        sidebar_layout = QVBoxLayout()
        sidebar = QListWidget()

        

        ListeClients = [ "client1","client2","client3","client4","client5","..."]
        sidebar.addItems(ListeClients)
        barreRecherche= QHBoxLayout()

        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Nom client")
        self.boutonRecherche = QPushButton("")
        self.boutonRecherche.setIcon(QIcon("icons/loupe.png"))


        barreRecherche.addWidget(self.edit)
        barreRecherche.addWidget(self.boutonRecherche)

        sidebar_layout.addLayout(barreRecherche)
        sidebar_layout.addWidget(sidebar)
        main_layout.addLayout(sidebar_layout, 1)  # 1 = largeur relative
        
        # Zone droite
        zone_droite = QVBoxLayout()
        main_layout.addLayout(zone_droite, 4)          # 4 = largeur relative

        

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


    def createMenuBar(self):
        menuBar = self.menuBar()

        file = menuBar.addMenu("&File")
        edit = menuBar.addMenu("&Edit")
        
        helpMenu = menuBar.addMenu("&Help")







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
