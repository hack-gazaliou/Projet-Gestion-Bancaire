import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QInputDialog,
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
        #self.right_panel_widget.setStyleSheet("background-color: white;")
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
        """Affiche les détails du client et ses comptes avec actions"""
        if item is None:
            return

        new_widget = QWidget()
        # new_widget.setStyleSheet("background-color: white;")
        new_layout = QVBoxLayout(new_widget)

        if hasattr(self, "right_panel_widget") and self.right_panel_widget:
            self.content_layout.replaceWidget(self.right_panel_widget, new_widget)
            self.right_panel_widget.deleteLater()

        self.right_panel_widget = new_widget
        self.right_panel_layout = new_layout

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

        self.right_panel_layout.addWidget(QLabel("<hr>"))

        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<h3>Comptes Bancaires :</h3>"))

        btn_add = QPushButton("+ Ouvrir un compte")
        btn_add.setStyleSheet(
            "background-color: #27ae60; color: white; font-weight: bold; padding: 5px;"
        )
        btn_add.clicked.connect(lambda: self.ouvrir_compte_dialog(client_id))
        header_layout.addWidget(btn_add)

        self.right_panel_layout.addLayout(header_layout)

        if not comptes:
            self.right_panel_layout.addWidget(QLabel("<i>Aucun compte ouvert.</i>"))
        else:
            for cpt in comptes:
                frame = QFrame()
                frame.setStyleSheet(
                    "border: 1px solid #ccc; border-radius: 5px; margin-bottom: 5px;"
                )
                row_layout = QHBoxLayout(frame)

                lbl_info = QLabel(f"<b>{cpt['type']}</b> (N°{cpt['id']})")
                lbl_solde = QLabel(f"{cpt['solde']}")
                lbl_solde.setStyleSheet(
                    "font-weight: bold; color: #2c3e50; font-size: 14px;"
                )

                row_layout.addWidget(lbl_info)
                row_layout.addStretch()  # Pousse le reste à droite
                row_layout.addWidget(lbl_solde)

                btn_close = QPushButton("Clôturer")
                btn_close.setStyleSheet(
                    "background-color: #e74c3c; color: white; border: none; padding: 5px;"
                )

                btn_close.clicked.connect(
                    lambda checked, cid=cpt["id"]: self.cloturer_compte_dialog(cid)
                )

                row_layout.addWidget(btn_close)

                self.right_panel_layout.addWidget(frame)

        self.right_panel_layout.addStretch()

    def ouvrir_compte_dialog(self, client_id):
        """Ouvre une popup pour choisir le type de compte à créer"""
        types = ["COURANT", "LIVRET_A", "PEL"]
        type_choisi, ok = QInputDialog.getItem(
            self, "Nouveau Compte", "Type de compte :", types, 0, False
        )

        if ok and type_choisi:
            # On crée avec 0€ par défaut
            succes, msg = self.controller.ajouter_compte_client(
                client_id, type_choisi, 0.0
            )

            if succes:
                QMessageBox.information(self, "Succès", "Compte ouvert avec succès.")
                self.show_account(self.selected_user)  # Rafraîchir l'affichage
            else:
                QMessageBox.critical(self, "Erreur", msg)

    def cloturer_compte_dialog(self, compte_id):
        """Demande confirmation et clôture le compte"""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Êtes-vous sûr de vouloir clôturer ce compte ?\nCette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            succes, msg = self.controller.cloturer_compte(compte_id)

            if succes:
                QMessageBox.information(self, "Succès", msg)
                self.show_account(self.selected_user)  # Rafraîchir
            else:
                QMessageBox.warning(self, "Impossible", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
