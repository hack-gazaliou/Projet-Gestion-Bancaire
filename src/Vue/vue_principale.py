import os
import sys

import account_operations
import operations
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.Controleur.controleur import Controller


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.setWindowTitle("Barre latérale fixe - PySide6")
        self.resize(800, 500)

        self.selected_user = None

        self.right_panel_widget = QWidget()
        self.right_panel_widget.setStyleSheet("background-color: white;")
        self.right_panel_layout = QVBoxLayout(self.right_panel_widget)
        self.right_panel_layout.addWidget(
            QLabel("Sélectionnez un client ou une action.")
        )

        self.createToolBar()

        content_area = QWidget()
        self.setCentralWidget(content_area)
        self.content_layout = QHBoxLayout(content_area)

        self.side_client_bar = self.createSideClientBar()

        self.content_layout.addLayout(self.side_client_bar, 1)
        self.content_layout.addWidget(self.right_panel_widget, 4)

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
        action_virements.triggered.connect(lambda: operations.show_transfer(self))
        toolbar.addAction(action_virements)

        action_depot = QAction("Depot", self)
        action_depot.triggered.connect(lambda: operations.show_deposit(self))
        toolbar.addAction(action_depot)

        action_retrait = QAction("Retrait", self)
        action_retrait.triggered.connect(lambda: operations.show_retrait(self))
        toolbar.addAction(action_retrait)

        action_modif = QAction("Modifier infos", self)
        action_modif.triggered.connect(
            lambda: account_operations.show_modify_client_popup(self)
        )
        toolbar.addAction(action_modif)

    def createSideClientBar(self):
        sidebar_layout = QVBoxLayout()

        # Barre de recherche et bouton Refresh côte à côte
        search_row = QHBoxLayout()
        self.barre_recherche_client = QLineEdit()
        self.barre_recherche_client.setPlaceholderText("Nom client")
        self.barre_recherche_client.textChanged.connect(self.filtrer_clients)

        self.bouton_refresh_clients = QPushButton("Refresh")
        self.bouton_refresh_clients.clicked.connect(self.reload_client_list)

        search_row.addWidget(self.barre_recherche_client)
        search_row.addWidget(self.bouton_refresh_clients)
        sidebar_layout.addLayout(search_row)

        self.client_list = QListWidget()
        self.client_list.setAlternatingRowColors(True)

        # self.db_clients = self.get_customer_list()

        for client in self.db_clients:
            item = QListWidgetItem(client["nom"])
            item.setData(Qt.UserRole, client["id"])
            self.client_list.addItem(item)

        self.client_list.itemClicked.connect(self.show_account)
        sidebar_layout.addWidget(self.client_list)

        self.bouton_create_new_client = QPushButton("Créer un client")
        self.bouton_create_new_client.clicked.connect(
            lambda: account_operations.show_create_client_popup(self)
        )
        sidebar_layout.addWidget(self.bouton_create_new_client)

        return sidebar_layout

    def reload_client_list(self):
        self.barre_recherche_client.clear()
        self.selected_user = None
        self.client_list.clear()

        # On récupère la vraie liste via LE Contrôleur
        clients = self.controller.get_tous_les_clients()

        for client in clients:
            item = QListWidgetItem(client["nom"])
            # On cache l'ID SQL dans l'item visuel
            item.setData(Qt.UserRole, client["id"])
            self.client_list.addItem(item)

    def show_account(self, item):
        # Nettoyage de la zone de droite
        while self.right_panel_layout.count():
            child = self.right_panel_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # récupération des données via l'ID caché
        client_id = item.data(Qt.UserRole)
        self.selected_user = item

        infos = self.controller.get_client_details(client_id)
        comptes = self.controller.get_comptes_client(client_id)

        # Affichage
        if infos:
            self.right_panel_layout.addWidget(
                QLabel(f"<h2>Client : {infos['nom']}</h2>")
            )
            self.right_panel_layout.addWidget(
                QLabel(f"Email : {infos.get('email', 'N/A')}")
            )

        self.right_panel_layout.addWidget(QLabel("<h3>Comptes :</h3>"))

        if not comptes:
            self.right_panel_layout.addWidget(QLabel("Aucun compte."))
        else:
            for cpt in comptes:
                texte = f"{cpt['type']} (N°{cpt['id']}) : {cpt['solde']}"
                self.right_panel_layout.addWidget(
                    QPushButton(texte)
                )  # Bouton pour cliquer dessus plus tard

        self.right_panel_layout.addStretch()

    """def get_customer_list(self) -> list:
        return [
            {"id": 101, "nom": "Client 1"},
            {"id": 102, "nom": "Sacha Bliard"},
            {"id": 103, "nom": "Antoine Augustin"},
            {"id": 104, "nom": "Sacha Bliard"},
            {"id": 105, "nom": "Hack Gazaliou"},
        ]"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
