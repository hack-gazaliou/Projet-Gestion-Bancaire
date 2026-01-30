import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QListWidget,
    QLabel,
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Barre latérale fixe - PySide6")
        self.resize(800, 500)

        self.sideBar = self.createSideBar()
        self.menuBar = self.createMenuBar()
        self.zone_droite_widget = QWidget()  # Widget conteneur pour la zone droite
        self.zone_droite_layout = QVBoxLayout(self.zone_droite_widget)
        self.zone_droite_layout.addWidget(QListWidget())

        central_widget = QWidget()  # necessaire pour QMainWindow
        self.setCentralWidget(central_widget)
        self.page_Layout = QHBoxLayout(central_widget)

        self.page_Layout.addLayout(self.sideBar, 1)
        self.page_Layout.addWidget(self.zone_droite_widget, 4)
        # pas besoin d'ajouter menuBar, QMainWindow le gere automatiquement

        self.edit.textChanged.connect(self.filtrer_clients)

    def filtrer_clients(
        self,
    ):  # plus tard peut etre autoriser recherche par nom ou prenom
        texte_recherche = self.edit.text().lower()
        for i in range(self.client_list.count()):
            item = self.client_list.item(i)
            correspondance = item.text().lower().startswith(texte_recherche)
            item.setHidden(not correspondance)

    def createZoneDroite(self):
        return QVBoxLayout()

    def createMenuBar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        edit_menu = menu_bar.addMenu("&Edit")
        help_menu = menu_bar.addMenu("&Help")
        return menu_bar

    def createSideBar(self):
        sidebar_layout = QVBoxLayout()

        barre_recherche = QHBoxLayout()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Nom client")

        barre_recherche.addWidget(self.edit)

        sidebar_layout.addLayout(barre_recherche)

        self.client_list = QListWidget()
        self.client_list.setAlternatingRowColors(True)

        liste_clients = ["Client 1", "Client 2", "Client 3", "Augustin", "test"]
        self.client_list.addItems(liste_clients)
        self.client_list.itemClicked.connect(self.afficher_details_client)

        sidebar_layout.addWidget(self.client_list)

        return sidebar_layout

    def afficher_details_client(self, item):
        new_widget = QWidget()
        new_widget.setStyleSheet("background-color: white;")
        new_layout = QVBoxLayout(new_widget)

        nom_client = QLabel(f"<b>Détails - {item.text()}</b>")
        comptes = QLabel(f"Informations du client :\n\nComptes: Courant, PEL, Livret A")

        new_layout.addWidget(nom_client)
        new_layout.addWidget(comptes)
        new_layout.addStretch()  # comble l'espace vide en bas

        self.page_Layout.replaceWidget(self.zone_droite_widget, new_widget)
        self.zone_droite_widget.deleteLater()
        self.zone_droite_widget = new_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
