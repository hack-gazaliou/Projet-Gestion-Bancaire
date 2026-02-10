"""Package pour la gestion des opérations bancaires"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from .transfer import TransferWidget
from .deposit import DepositWidget
from .withdraw import WithdrawWidget
from .account_view import AccountViewWidget


def show_transfer(main_window):
    """Affiche interface de virement"""
    TransferWidget(main_window)


def show_deposit(main_window):
    """Affiche interface de dépôt"""
    DepositWidget(main_window)


def show_retrait(main_window):
    """Affiche interface de retrait"""
    WithdrawWidget(main_window)


def show_account(main_window, item):
    """Affiche les comptes d'un client"""
    main_window.selected_user = item
    if not main_window.selected_user:
        show_selection_error(main_window)
        return
    
    client_id = item.data(Qt.UserRole)
    client_name = item.text()
    AccountViewWidget(main_window, client_id, client_name)


def show_selection_error(main_window):
    """Affiche une erreur si aucun client n'est selectionne"""
    error_widget = QWidget()
    error_widget.setStyleSheet("background-color: #ffe6e6;")
    error_layout = QVBoxLayout(error_widget)

    error_label = QLabel("<b>Veuillez sélectionner un client dans la liste.</b>")
    error_label.setAlignment(Qt.AlignCenter)

    error_layout.addStretch()
    error_layout.addWidget(error_label)
    error_layout.addStretch()

    main_window.content_layout.replaceWidget(
        main_window.right_panel_widget, error_widget
    )
    main_window.right_panel_widget.deleteLater()
    main_window.right_panel_widget = error_widget
