from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMessageBox, QVBoxLayout, QWidget


class OperationWidget(QWidget):
    """Classe de base pour tous les widgets d'opérations"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_user = main_window.selected_user
        self.setStyleSheet("background-color: white;")

    def update_right_panel(self):
        """Remplace le widget de droite"""
        if self.main_window.right_panel_widget:
            self.main_window.right_panel_widget.deleteLater()

        self.main_window.content_layout.addWidget(self, 4)
        self.main_window.right_panel_widget = self

    def show_if_user_selected(self):
        if not self.current_user:
            self.show_selection_error()
            return False
        return True

    def show_selection_error(self):
        error_widget = QWidget()
        error_widget.setStyleSheet("background-color: #ffe6e6;")
        layout = QVBoxLayout(error_widget)
        error_label = QLabel("<b>Veuillez sélectionner un client dans la liste.</b>")
        error_label.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(error_label)
        layout.addStretch()

        if self.main_window.right_panel_widget:
            self.main_window.right_panel_widget.deleteLater()
        self.main_window.content_layout.addWidget(error_widget, 4)
        self.main_window.right_panel_widget = error_widget

    def get_account_list(self, client_item=None):
        """Retourne la vraie liste des comptes via le contrôleur"""
        target_item = client_item if client_item else self.current_user
        if not target_item:
            return []

        client_id = (
            target_item
            if isinstance(target_item, int)
            else target_item.data(Qt.UserRole)
        )

        comptes = self.main_window.controller.get_comptes_client(client_id)

        formatted_accounts = []
        for c in comptes:
            formatted_accounts.append(
                {"id": c["id"], "nom": f"{c['type']} (Solde: {c['solde']})"}
            )
        return formatted_accounts

    def validate_amount(self, amount_text):
        if not amount_text or amount_text.strip() == "":
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un montant.")
            return False
        try:
            val = float(amount_text)
            if val <= 0:
                raise ValueError
            return True
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Montant invalide (doit être > 0).")
            return False
