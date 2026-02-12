from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from .base import OperationWidget


class TransferWidget(OperationWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        if not self.show_if_user_selected():
            return
        self.init_ui()
        self.update_right_panel()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(
            QLabel(
                f"<h2>Effectuer un Virement</h2><p>Émetteur : {self.current_user.text()}</p>"
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
        self.amount_input.setPlaceholderText("0.00")
        self.amount_input.setValidator(
            QDoubleValidator(0.0, 999999.0, 2, self.amount_input)
        )

        # Remplissage comptes source
        accounts = self.get_account_list(self.current_user)
        for acc in accounts:
            self.source_combo.addItem(acc["nom"], acc["id"])
            self.dest_combo.addItem(acc["nom"], acc["id"])  # Pour l'interne

        # Remplissage clients externes (via Controller)
        current_user_id = self.current_user.data(Qt.UserRole)
        all_clients = self.main_window.controller.get_tous_les_clients()

        for client in all_clients:
            if client["id"] != current_user_id:
                self.ext_client_combo.addItem(client["nom"], client["id"])

        self.internal_dest_label = QLabel("Compte crédité :")
        self.external_client_label = QLabel("Bénéficiaire :")
        self.external_account_label = QLabel("Compte bénéficiaire :")

        form_layout.addRow("<b>Type :</b>", self.type_combo)
        form_layout.addRow("Débiter :", self.source_combo)
        form_layout.addRow(self.internal_dest_label, self.dest_combo)
        form_layout.addRow(self.external_client_label, self.ext_client_combo)
        form_layout.addRow(self.external_account_label, self.ext_account_combo)
        form_layout.addRow("Montant (€) :", self.amount_input)

        main_layout.addLayout(form_layout)

        submit_button = QPushButton("Exécuter")
        submit_button.clicked.connect(self.prepare_transfer)
        main_layout.addWidget(submit_button)
        main_layout.addStretch()

        self.type_combo.currentIndexChanged.connect(self.on_transfer_type_changed)
        self.ext_client_combo.currentIndexChanged.connect(
            self.on_external_client_changed
        )

        self.on_transfer_type_changed(0)
        if self.ext_client_combo.count() > 0:
            self.on_external_client_changed()

    def on_transfer_type_changed(self, index):
        is_internal = index == 0
        self.internal_dest_label.setVisible(is_internal)
        self.dest_combo.setVisible(is_internal)
        self.external_client_label.setVisible(not is_internal)
        self.ext_client_combo.setVisible(not is_internal)
        self.external_account_label.setVisible(not is_internal)
        self.ext_account_combo.setVisible(not is_internal)

    def on_external_client_changed(self):
        self.ext_account_combo.clear()
        client_id = self.ext_client_combo.currentData()
        if client_id:
            accounts = self.get_account_list(client_id)
            for acc in accounts:
                self.ext_account_combo.addItem(acc["nom"], acc["id"])

    def prepare_transfer(self):
        if not self.validate_amount(self.amount_input.text()):
            return

        montant = float(self.amount_input.text())
        source_id = self.source_combo.currentData()

        if self.type_combo.currentIndex() == 0:  # Interne
            dest_id = self.dest_combo.currentData()
        else:  # Externe
            dest_id = self.ext_account_combo.currentData()

        if source_id == dest_id:
            QMessageBox.warning(
                self, "Erreur", "Les comptes source et destination sont identiques."
            )
            return

        succes, msg = self.main_window.controller.effectuer_virement(
            source_id, dest_id, montant
        )

        if succes:
            QMessageBox.information(self, "Succès", msg)
            self.main_window.show_account(self.current_user)  # Retour à la vue compte
        else:
            QMessageBox.critical(self, "Erreur", msg)
