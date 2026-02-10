from PySide6.QtWidgets import (
    QComboBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QFormLayout,
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt
from .base import OperationWidget


class TransferWidget(OperationWidget):
    """Widget pour effectuer un virement"""
    
    def __init__(self, main_window):
        super().__init__(main_window)
        
        if not self.show_if_user_selected():
            return
            
        self.init_ui()
        self.update_right_panel()

    def init_ui(self):
        """Initialise l'interface utilisateur du virement"""
        main_layout = QVBoxLayout(self)
        
        main_layout.addWidget(
            QLabel(
                f"<h2>Effectuer un Virement</h2>"
                f"<p>Émetteur : {self.current_user.text()}</p>"
            )
        )

        form_layout = QFormLayout()

        self.type_combo = QComboBox()
        self.source_combo = QComboBox()
        self.dest_combo = QComboBox()
        self.ext_client_combo = QComboBox()
        self.ext_account_combo = QComboBox()
        self.amount_input = QLineEdit()

        self.type_combo.addItems(["Virement Interne", "Virement Externe"])
        self.amount_input.setPlaceholderText("0.00 €")
        self.amount_input.setValidator(
            QIntValidator(0, 9999, self.amount_input)
        )


        for acc in self.get_account_list(self.current_user):
            self.source_combo.addItem(acc["nom"], acc["id"])
            self.dest_combo.addItem(acc["nom"], acc["id"])

        current_user_id = self.current_user.data(Qt.UserRole)
        available_clients = [
            c for c in self.main_window.db_clients if c["id"] != current_user_id
        ]
        for client in available_clients:
            self.ext_client_combo.addItem(client["nom"], client["id"])

        self.internal_dest_label = QLabel("Compte crédité :")
        self.external_client_label = QLabel("Bénéficiaire :")
        self.external_account_label = QLabel("Compte bénéficiaire :")

        form_layout.addRow("<b>Type de virement :</b>", self.type_combo)
        form_layout.addRow("Compte débité :", self.source_combo)
        form_layout.addRow(self.internal_dest_label, self.dest_combo)
        form_layout.addRow(self.external_client_label, self.ext_client_combo)
        form_layout.addRow(self.external_account_label, self.ext_account_combo)
        form_layout.addRow("Montant :", self.amount_input)

        main_layout.addLayout(form_layout)

        submit_button = QPushButton("Exécuter le virement")
        submit_button.clicked.connect(self.prepare_transfer)
        main_layout.addWidget(submit_button)
        main_layout.addStretch()

        self.type_combo.currentIndexChanged.connect(self.on_transfer_type_changed)
        self.ext_client_combo.currentIndexChanged.connect(
            self.on_external_client_changed
        )


        self.on_transfer_type_changed(0)
        if available_clients:
            self.on_external_client_changed()

    def on_transfer_type_changed(self, index):
        """Gère l'affichage/masquage des champs selon le type de virement"""
        is_internal = index == 0
        self.internal_dest_label.setVisible(is_internal)
        self.dest_combo.setVisible(is_internal)
        self.external_client_label.setVisible(not is_internal)
        self.ext_client_combo.setVisible(not is_internal)
        self.external_account_label.setVisible(not is_internal)
        self.ext_account_combo.setVisible(not is_internal)

    def on_external_client_changed(self):
        """Met à jour la liste des comptes quand on change de client bénéficiaire"""
        self.ext_account_combo.clear()
        client_id = self.ext_client_combo.currentData()
        accounts = self.get_account_list(client_id)
        for acc in accounts:
            self.ext_account_combo.addItem(acc["nom"], acc["id"])

    def prepare_transfer(self):
        """Prépare et valide les données avant d'exécuter un virement"""
        amount_text = self.amount_input.text()
        if not self.validate_amount(amount_text):
            return

        source_account_id = self.source_combo.itemData(
            self.source_combo.currentIndex()
        )
        transfer_type = self.type_combo.currentText()
        amount_cents = int(amount_text) * 100

        if transfer_type == "Virement Interne":
            dest_account_id = self.dest_combo.itemData(
                self.dest_combo.currentIndex()
            )
            print(
                f"Virement interne: compte source {source_account_id} "
                f"compte destinataire {dest_account_id} "
                f"d'un montant de {amount_cents}"
            )
        elif transfer_type == "Virement Externe":
            dest_account_id = self.ext_account_combo.itemData(
                self.ext_account_combo.currentIndex()
            )
            print(
                f"Virement externe: compte source {source_account_id} "
                f"compte destinataire {dest_account_id} "
                f"d'un montant de {amount_cents}"
            )
