from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .base import OperationWidget


class AccountViewWidget(OperationWidget):
    def __init__(self, main_window, client_id, client_name):
        QWidget.__init__(self)
        self.main_window = main_window
        self.client_id = client_id
        self.client_name = client_name
        # self.setStyleSheet("background-color: white;")

        self.create_interface()

    def create_interface(self):
        main_layout = QVBoxLayout(self)
        header = QLabel(f"<h2>Comptes de {self.client_name}</h2>")
        main_layout.addWidget(header)

        accounts = self.main_window.controller.get_comptes_client(self.client_id)

        if not accounts:
            no_accounts_label = QLabel("Aucun compte trouvé pour ce client.")
            no_accounts_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(no_accounts_label)
        else:
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)

            for account in accounts:
                acc_data = {
                    "id": account["id"],
                    "nom": account["type"],
                    "solde": account["solde"],
                }
                scroll_layout.addWidget(self._create_account_card(acc_data))

            scroll_layout.addStretch()
            scroll_area.setWidget(scroll_widget)
            main_layout.addWidget(scroll_area)

        # Bouton Créer
        buttons_layout = QHBoxLayout()
        create_account_button = QPushButton("Ouvrir un nouveau compte")
        create_account_button.clicked.connect(self._on_create_account)
        buttons_layout.addWidget(create_account_button)
        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)

    def _create_account_card(self, account):
        card = QFrame()
        card.setStyleSheet(
            "QFrame { border: 1px solid #ddd; border-radius: 5px; padding: 10px; background-color: #f9f9f9; }"
        )
        layout = QVBoxLayout(card)

        # Titre (Type)
        title = QLabel(f"<b>{account['nom']}</b>")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)

        # Info
        layout.addWidget(QLabel(f"N° Compte : {account['id']}"))

        # Solde
        lbl_solde = QLabel(f"Solde : {account['solde']}")
        lbl_solde.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px;")
        layout.addWidget(lbl_solde)

        # Actions
        btn_layout = QHBoxLayout()
        close_button = QPushButton("Clôturer")
        close_button.setStyleSheet("color: red;")
        close_button.clicked.connect(lambda: self._on_close_account(account))
        btn_layout.addWidget(close_button)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        return card

    def _on_create_account(self):
        types = ["COURANT", "LIVRET_A", "PEL"]
        type_choisi, ok = QInputDialog.getItem(
            self, "Ouvrir un compte", "Type de compte :", types, 0, False
        )

        if ok and type_choisi:
            succes, msg = self.main_window.controller.ajouter_compte_client(
                self.client_id, type_choisi, 0.0
            )
            if succes:
                QMessageBox.information(self, "Succès", "Compte ouvert.")
                self.main_window.show_account(self.main_window.selected_user)  # Refresh
            else:
                QMessageBox.critical(self, "Erreur", msg)

    def _on_close_account(self, account):
        reply = QMessageBox.question(
            self,
            "Confirmer",
            f"Voulez-vous vraiment clôturer le compte {account['nom']} (N°{account['id']}) ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            QMessageBox.information(
                self,
                "Info",
                "Fonctionnalité de clôture à implémenter dans le contrôleur.",
            )
