import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel, QToolBar,QListWidgetItem) # Ajout de QToolBar
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Barre latérale fixe - PySide6")
        self.resize(800, 500)

        self.createToolBar()

        content_area = QWidget() 
        self.setCentralWidget(content_area)
        self.content_layout = QHBoxLayout(content_area)

        self.side_client_bar = self.createSideClientBar()

        self.zone_droite_widget = QWidget()
        self.zone_droite_widget.setStyleSheet("background-color: white;")
        self.zone_droite_layout = QVBoxLayout(self.zone_droite_widget)
        self.zone_droite_layout.addWidget(QListWidget())

        self.content_layout.addLayout(self.side_client_bar, 1)
        self.content_layout.addWidget(self.zone_droite_widget, 4)

        self.selected_user=None

    def filtrer_clients(self):
        texte_recherche = self.barre_recherche_client.text().lower()
        for i in range(self.client_list.count()):
            item = self.client_list.item(i)
            if item: 
                correspondance = item.text().lower().startswith(texte_recherche)
                item.setHidden(not correspondance)

    def createToolBar(self):
        toolbar = self.addToolBar("Menu Principal")
        toolbar.setMovable(False) 

        action_comptes = QAction("Comptes", self)
        action_comptes.triggered.connect(lambda: self.show_account(self.selected_user))
        toolbar.addAction(action_comptes)

        action_virements = QAction("Virements", self)
        action_virements.triggered.connect(self.reinitialize_text_zone)
        toolbar.addAction(action_virements)

        action_depot = QAction("Depot", self)
        action_depot.triggered.connect(lambda: print("TODO"))
        toolbar.addAction(action_depot)

        action_retrait = QAction("Retrait", self)
        action_retrait.triggered.connect(lambda: print("TODO"))
        toolbar.addAction(action_retrait)

        action_modif = QAction("Modifier infos", self)
        action_modif.triggered.connect(lambda: print("TODO"))
        toolbar.addAction(action_modif)

    def createSideClientBar(self):
        sidebar_layout = QVBoxLayout()

        self.barre_recherche_client = QLineEdit()
        self.barre_recherche_client.setPlaceholderText("Nom client")
        self.barre_recherche_client.textChanged.connect(self.filtrer_clients)
        
        sidebar_layout.addWidget(self.barre_recherche_client)

        self.client_list = QListWidget()
        self.client_list.setAlternatingRowColors(True)

        self.db_clients = self.get_customer_list()

        for client in self.db_clients:
            item = QListWidgetItem(client["nom"])
            item.setData(Qt.UserRole, client["id"])#on stocke l'identifiant au cas ou il y ait des doublons
            self.client_list.addItem(item)

        self.client_list.itemClicked.connect(self.show_account)
        sidebar_layout.addWidget(self.client_list)

        self.bouton_create_new_client = QPushButton("Créer un client")
        #self.bouton_create_new_client.clicked.connect(TODO)

        sidebar_layout.addWidget(self.bouton_create_new_client)

        return sidebar_layout

    def show_account(self, item):
        if item:
            self.selected_user=item
            nom_client = QLabel(f"<b>Détails - {item.text()},id = {item.data(Qt.UserRole)}</b>")
            comptes = QLabel(f"Informations du client :\n\nComptes: Courant, PEL, Livret A")
        
            new_zone_droite_widget = QWidget()
            new_zone_droite_widget.setStyleSheet("background-color: white;")

            new_zone_droite_layout = QVBoxLayout(new_zone_droite_widget)
            new_zone_droite_layout.addWidget(nom_client)
            new_zone_droite_layout.addWidget(comptes)
            new_zone_droite_layout.addStretch()
            
            self.content_layout.replaceWidget(self.zone_droite_widget, new_zone_droite_widget)
            self.zone_droite_widget.deleteLater()
            self.zone_droite_widget = new_zone_droite_widget

    def reinitialize_text_zone(self):
        new_zone_droite_widget = QWidget()
        new_zone_droite_widget.setStyleSheet("background-color: white;")

        new_zone_droite_layout = QVBoxLayout(new_zone_droite_widget)
        new_zone_droite_layout.addStretch()
        
        self.content_layout.replaceWidget(self.zone_droite_widget, new_zone_droite_widget)
        self.zone_droite_widget.deleteLater()
        self.zone_droite_widget = new_zone_droite_widget

    def get_customer_list(self)-> dict:
        return [
            {"id": 101, "nom": "Client 1"},
            {"id": 102, "nom": "Sacha Bliard"},
            {"id": 103, "nom": "Antoine Augustin"},
            {"id": 104, "nom": "Sacha Bliard"}, # Homonyme
            {"id": 105, "nom": "Hack Gazaliou"}
        ]




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())