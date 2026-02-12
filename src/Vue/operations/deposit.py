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


class DepositWidget(OperationWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        if not self.show_if_user_selected():
            return
        self.init_ui()
        self.update_right_panel()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(
            QLabel(f"<h2>Dépôt</h2><p>Client : {self.current_user.text()}</p>")
        )

        form_layout = QFormLayout()
        self.account_combo = QComboBox()
        for acc in self.get_account_list(self.current_user):
            self.account_combo.addItem(acc["nom"], acc["id"])

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        self.amount_input.setValidator(
            QDoubleValidator(0.0, 1000000.0, 2, self.amount_input)
        )

        form_layout.addRow("Vers le compte :", self.account_combo)
        form_layout.addRow("Montant :", self.amount_input)
        main_layout.addLayout(form_layout)

        btn = QPushButton("Valider le dépôt")
        btn.clicked.connect(self.prepare_deposit)
        main_layout.addWidget(btn)
        main_layout.addStretch()

    def prepare_deposit(self):
        if not self.validate_amount(self.amount_input.text()):
            return

        account_id = self.account_combo.currentData()
        montant = float(self.amount_input.text())

        # APPEL CONTROLEUR
        succes, msg = self.main_window.controller.effectuer_depot(account_id, montant)

        if succes:
            QMessageBox.information(self, "Succès", msg)
            self.main_window.show_account(self.current_user)
        else:
            QMessageBox.critical(self, "Erreur", msg)
