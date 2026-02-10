from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .base import OperationWidget


class AccountViewWidget(OperationWidget):
    """Widget pour visualiser les comptes d'un client"""

    def __init__(self, main_window, client_id, client_name):
        QWidget.__init__(self)
        self.main_window = main_window
        self.client_id = client_id
        self.client_name = client_name
        self.setStyleSheet("background-color: white;")

        self.create_interface()
        self.update_right_panel()

    def create_interface(self):
        """Initialise l'interface utilisateur"""
        main_layout = QVBoxLayout(self)

        header = QLabel(f"<h2>Comptes de {self.client_name}</h2>")
        main_layout.addWidget(header)

        accounts = self.get_account_list(
            self.client_id
        )  # TODO: remplacer par une vraie requete SQL

        if not accounts:
            no_accounts_label = QLabel("Aucun compte trouvé pour ce client.")
            no_accounts_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(no_accounts_label)
            main_layout.addStretch()
            return

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        for account in accounts:
            account_widget = self._create_account_card(account)
            scroll_layout.addWidget(account_widget)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        buttons_layout = QHBoxLayout()

        create_account_button = QPushButton("Créer un compte")
        create_account_button.clicked.connect(self._on_create_account)
        buttons_layout.addWidget(create_account_button)

        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)

    def _create_account_card(self, account):
        """Crée une carte pour afficher un compte"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                background-color: #f9f9f9;
            }
        """)

        layout = QVBoxLayout(card)

        account_title = QLabel(f"<b>{account['nom']}</b>")
        account_title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(account_title)

        account_id_label = QLabel(f"numéro du compte: {account['id']}")
        layout.addWidget(account_id_label)

        account_money_label = QLabel("Solde: TODO")
        layout.addWidget(account_money_label)

        button_layout = QHBoxLayout()

        detail_button = QPushButton("Voir détails")
        detail_button.clicked.connect(lambda: self._show_account_detail(account))
        button_layout.addWidget(detail_button)

        close_button = QPushButton("Clôturer")
        close_button.clicked.connect(lambda: self._on_close_account(account))
        button_layout.addWidget(close_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        return card

    def _show_account_detail(self, account):
        """Affiche le détail d'un compte selectionné"""
        # TODO affiche l historique du compte
        print(f"Détail du compte {account['id']} ({account['nom']})")

    def _on_create_account(self) -> None:
        """Crée un nouveau compte pour le client"""
        # À implémenter
        print(f"Créer un compte pour le client {self.client_id}")

    def _on_close_account(self, account) -> None:
        """Clôture le compte spécifié"""
        # À implémenter
        print(
            f"Clôturer le compte {account['id']} ({account['nom']}) pour le client {self.client_id}"
        )
