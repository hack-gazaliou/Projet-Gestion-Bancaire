import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from Controleur.controleur import Controller
from Vue import account_operations, operations


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = Controller()

        self.setWindowTitle("Gestion Bancaire - Finale")
        self.resize(900, 600)

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

        self.reload_client_list()

    def createToolBar(self):
        """Création de la barre de menu en haut"""
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
        """Création de la colonne de gauche (Recherche + Liste vide)"""
        sidebar_layout = QVBoxLayout()

        search_row = QHBoxLayout()
        self.barre_recherche_client = QLineEdit()
        self.barre_recherche_client.setPlaceholderText("Nom client")
        self.barre_recherche_client.textChanged.connect(self.filtrer_clients)

        self.bouton_refresh_clients = QPushButton("Refresh")
        self.bouton_refresh_clients.clicked.connect(self.reload_client_list)

        search_row.addWidget(self.barre_recherche_client)
        search_row.addWidget(self.bouton_refresh_clients)
        sidebar_layout.addLayout(search_row)

        # Liste vide
        self.client_list = QListWidget()
        self.client_list.setAlternatingRowColors(True)
        self.client_list.itemClicked.connect(self.show_account)
        sidebar_layout.addWidget(self.client_list)

        # Bouton création
        self.bouton_create_new_client = QPushButton("Créer un client")
        self.bouton_create_new_client.clicked.connect(
            lambda: account_operations.show_create_client_popup(self)
        )
        sidebar_layout.addWidget(self.bouton_create_new_client)

        return sidebar_layout

    def reload_client_list(self):
        """Récupère les clients depuis la BDD et remplit la liste"""
        self.barre_recherche_client.clear()
        self.selected_user = None
        self.client_list.clear()

        clients = self.controller.get_tous_les_clients()

        for client in clients:
            item = QListWidgetItem(client["nom"])
            # On cache l'ID SQL dans l'item
            item.setData(Qt.UserRole, client["id"])
            self.client_list.addItem(item)

    def filtrer_clients(self):
        """Filtre visuel de la liste"""
        texte_recherche = self.barre_recherche_client.text().lower()
        for i in range(self.client_list.count()):
            item = self.client_list.item(i)
            if item:
                correspondance = item.text().lower().startswith(texte_recherche)
                item.setHidden(not correspondance)

    def show_account(self, item):
        """Affiche les détails du client à droite"""
        if item is None:
            return
        new_widget = QWidget()
        new_widget.setStyleSheet("background-color: white;")
        new_layout = QVBoxLayout(new_widget)

        if hasattr(self, "right_panel_widget") and self.right_panel_widget:
            self.content_layout.replaceWidget(self.right_panel_widget, new_widget)
            self.right_panel_widget.deleteLater()  # On détruit proprement l'ancien

        self.right_panel_widget = new_widget
        self.right_panel_layout = new_layout

        if isinstance(item, QListWidgetItem):
            client_id = item.data(Qt.UserRole)
            self.selected_user = item
        else:
            client_id = item.data(Qt.UserRole)
            self.selected_user = item

        infos = self.controller.get_client_details(client_id)
        comptes = self.controller.get_comptes_client(client_id)

        if infos:
            self.right_panel_layout.addWidget(
                QLabel(f"<h2>Client : {infos['nom']}</h2>")
            )
            self.right_panel_layout.addWidget(
                QLabel(f"<b>Email :</b> {infos.get('email', 'N/A')}")
            )
            self.right_panel_layout.addWidget(
                QLabel(f"<b>Tél :</b> {infos.get('telephone', 'N/A')}")
            )
            self.right_panel_layout.addWidget(
                QLabel(f"<b>Adresse :</b> {infos.get('adresse', 'N/A')}")
            )

        self.right_panel_layout.addWidget(QLabel("<h3>Comptes Bancaires :</h3>"))

        if not comptes:
            self.right_panel_layout.addWidget(QLabel("<i>Aucun compte ouvert.</i>"))
        else:
            for cpt in comptes:
                btn_texte = (
                    f"{cpt['type']} (N°{cpt['id']})   ----->   Solde : {cpt['solde']}"
                )
                btn = QPushButton(btn_texte)
                btn.setStyleSheet(
                    "text-align: left; padding: 10px; font-size: 14px; background-color: #f0f0f0; border: 1px solid #ccc;"
                )
                self.right_panel_layout.addWidget(btn)

        self.right_panel_layout.addStretch()

        while self.right_panel_layout.count():
            child = self.right_panel_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        client_id = item.data(Qt.UserRole)
        self.selected_user = item

        infos = self.controller.get_client_details(client_id)
        comptes = self.controller.get_comptes_client(client_id)

        if infos:
            self.right_panel_layout.addWidget(
                QLabel(f"<h2>Client : {infos['nom']}</h2>")
            )
            self.right_panel_layout.addWidget(
                QLabel(f"<b>Email :</b> {infos.get('email', 'N/A')}")
            )
            self.right_panel_layout.addWidget(
                QLabel(f"<b>Tél :</b> {infos.get('telephone', 'N/A')}")
            )
            self.right_panel_layout.addWidget(
                QLabel(f"<b>Adresse :</b> {infos.get('adresse', 'N/A')}")
            )

        self.right_panel_layout.addWidget(QLabel("<h3>Comptes Bancaires :</h3>"))

        if not comptes:
            self.right_panel_layout.addWidget(QLabel("<i>Aucun compte ouvert.</i>"))
        else:
            for cpt in comptes:
                btn_texte = (
                    f"{cpt['type']} (N°{cpt['id']})   ----->   Solde : {cpt['solde']}"
                )
                btn = QPushButton(btn_texte)
                btn.setStyleSheet("text-align: left; padding: 10px; font-size: 14px;")
                self.right_panel_layout.addWidget(btn)

        self.right_panel_layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
