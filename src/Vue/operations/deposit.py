from PySide6.QtWidgets import (
    QComboBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QFormLayout,
)
from PySide6.QtGui import QIntValidator
from .base import OperationWidget


class DepositWidget(OperationWidget):
    """Widget pour effectuer un dépôt"""
    
    def __init__(self, main_window):
        super().__init__(main_window)
        
        if not self.show_if_user_selected():
            return
            
        self.init_ui()
        self.update_right_panel()

    def init_ui(self):
        """Initialise l'interface utilisateur du dépôt"""
        main_layout = QVBoxLayout(self)

        main_layout.addWidget(
            QLabel(
                f"<h2>Effectuer un Dépôt</h2>"
                f"<p>Client : {self.current_user.text()}</p>"
            )
        )

        form_layout = QFormLayout()
        
        self.account_combo = QComboBox()
        for acc in self.get_account_list(self.current_user):
            self.account_combo.addItem(acc["nom"], acc["id"])

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00 €")
        self.amount_input.setValidator(
            QIntValidator(0, 9999, self.amount_input)
        )

        form_layout.addRow("Vers le compte :", self.account_combo)
        form_layout.addRow("Montant à déposer :", self.amount_input)

        main_layout.addLayout(form_layout)

        submit_button = QPushButton("Valider le dépôt")
        submit_button.clicked.connect(self.prepare_deposit)
        main_layout.addWidget(submit_button)
        main_layout.addStretch()

    def prepare_deposit(self):
        """Prépare et valide les données avant d'exécuter un dépôt"""
        amount_text = self.amount_input.text()
        if not self.validate_amount(amount_text):
            return
        
        account_id = self.account_combo.itemData(
            self.account_combo.currentIndex()
        )
        print(f"Compte {account_id} montant {int(amount_text)}")
