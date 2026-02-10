"""Classe de base pour tous les widgets d'opérations"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox
from PySide6.QtCore import Qt


class OperationWidget(QWidget):
    """Classe de base pour tous les widgets d'opérations"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_user = main_window.selected_user
        self.setStyleSheet("background-color: white;")
        
    def update_right_panel(self):
        """Remplace le widget de droite"""
        self.main_window.content_layout.replaceWidget(
            self.main_window.right_panel_widget, self
        )
        self.main_window.right_panel_widget.deleteLater()
        self.main_window.right_panel_widget = self

    def show_if_user_selected(self):
        """Affiche l'interface si un utilisateur est sélectionné sinon affiche erreur"""
        if not self.current_user:
            self.show_selection_error()
            return False
        return True

    def show_selection_error(self):
        """Affiche une erreur si aucun client n'est selectionne"""
        error_widget = QWidget()
        error_widget.setStyleSheet("background-color: #ffe6e6;")
        layout = QVBoxLayout(error_widget)

        error_label = QLabel("<b>Veuillez sélectionner un client dans la liste.</b>")
        error_label.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(error_label)
        layout.addStretch()

        self.main_window.content_layout.replaceWidget(
            self.main_window.right_panel_widget, error_widget
        )
        self.main_window.right_panel_widget.deleteLater()
        self.main_window.right_panel_widget = error_widget


    @staticmethod
    def get_account_list(client_item=None):
        """Retourne une liste de comptes simulée pour un client donné"""
        return [
            {"id": 101, "nom": "Compte Courant"},
            {"id": 102, "nom": "Livret A"},
            {"id": 103, "nom": "PEL"},
            {"id": 104, "nom": "PEL 2"},
        ]

    def validate_amount(self, amount_text):
        """verifie que le montant est valide"""
        if amount_text == "" or int(amount_text) == 0:
            QMessageBox.warning(
                self.main_window,
                "Montant invalide",
                "Veuillez entrer un montant strictement positif.",
            )
            return False
        return True
