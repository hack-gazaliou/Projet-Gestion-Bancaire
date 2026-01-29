from functools import partial
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                               QPushButton, QComboBox, QFormLayout)
from PySide6.QtCore import Qt

def update_right_panel(main_window, new_widget):
    """Fonction utilitaire pour remplacer le widget de droite."""
    # Le widget de droite dans la fenêtre principale est nommé `right_panel_widget`
    main_window.content_layout.replaceWidget(main_window.right_panel_widget, new_widget)
    main_window.right_panel_widget.deleteLater()
    main_window.right_panel_widget = new_widget

def _show_selection_error(main_window):
    """Affiche une erreur si aucun client n'est sélectionné."""
    error_widget = QWidget()
    error_widget.setStyleSheet("background-color: #ffe6e6;") 
    layout = QVBoxLayout(error_widget)
    
    error_label = QLabel("<b>Veuillez sélectionner un client dans la liste.</b>")
    error_label.setAlignment(Qt.AlignCenter)
    
    layout.addStretch()
    layout.addWidget(error_label)
    layout.addStretch()
    
    update_right_panel(main_window, error_widget)

def _get_account_list(client_item=None):
    return [
            {"id": 101, "nom": "Compte Courant"},
            {"id": 102, "nom": "Livret A"},
            {"id": 103, "nom": "PEL"},
            {"id": 104, "nom": "PEL 2"}
        ]

def on_transfer_type_changed(index, internal_widgets, external_widgets):
    """Gère l'affichage/masquage des champs selon le type de virement."""
    is_internal = (index == 0)

    for widget in internal_widgets:
        widget.setVisible(is_internal)

    for widget in external_widgets:
        widget.setVisible(not is_internal)

def on_external_client_changed(ext_client_combo, ext_account_combo):
    """Met à jour la liste des comptes quand on change de client bénéficiaire."""
    ext_account_combo.clear()
    client_id = ext_client_combo.currentData()
    accounts = _get_account_list(client_id)
    for acc in accounts:
        ext_account_combo.addItem(acc["nom"], acc["id"])  




def show_transfer(main_window):
    """Construit et affiche l'interface de virement."""
    current_user = main_window.selected_user
    
    if not current_user:
        _show_selection_error(main_window)
        return

    container_widget = QWidget()
    container_widget.setStyleSheet("background-color: white;")
    main_layout = QVBoxLayout(container_widget)

    main_layout.addWidget(QLabel(f"<h2>Effectuer un Virement</h2><p>Émetteur : {current_user.text()}</p>"))

    form_layout = QFormLayout()

    transfer_type_combo = QComboBox()
    transfer_type_combo.addItems(["Virement Interne", "Virement Externe"])
    
    source_account_combo = QComboBox()
    for acc in _get_account_list(current_user):
        source_account_combo.addItem(acc["nom"], acc["id"])

    internal_dest_label = QLabel("Compte crédité :")
    internal_dest_combo = QComboBox()
    for acc in _get_account_list(current_user):
        internal_dest_combo.addItem(acc["nom"], acc["id"])

    external_client_label = QLabel("Bénéficiaire :")
    external_client_combo = QComboBox()
    
    external_account_label = QLabel("Compte bénéficiaire :")
    external_account_combo = QComboBox()

    amount_input = QLineEdit()
    amount_input.setPlaceholderText("0.00 €")
    
    submit_button = QPushButton("Exécuter le virement")

    current_user_id = current_user.data(Qt.UserRole)
    available_clients = [c for c in main_window.db_clients if c["id"] != current_user_id]
    
    for client in available_clients:
        external_client_combo.addItem(client["nom"], client["id"])

    form_layout.addRow("<b>Type de virement :</b>", transfer_type_combo)
    form_layout.addRow("Compte débité :", source_account_combo)
    
    form_layout.addRow(internal_dest_label, internal_dest_combo)
    form_layout.addRow(external_client_label, external_client_combo)
    form_layout.addRow(external_account_label, external_account_combo)
    form_layout.addRow("Montant :", amount_input)

    main_layout.addLayout(form_layout)
    main_layout.addWidget(submit_button)
    main_layout.addStretch()
    
    # On groupe les widgets pour les passer facilement à la fonction
    internal_widgets = [internal_dest_label, internal_dest_combo]
    external_widgets = [external_client_label, external_client_combo, 
                        external_account_label, external_account_combo]

    # 'idx'  argument envoyé par le signal (l'index sélectionné)
    transfer_type_combo.currentIndexChanged.connect(
        lambda idx: on_transfer_type_changed(idx, internal_widgets, external_widgets)
    )

    external_client_combo.currentIndexChanged.connect(
        lambda: on_external_client_changed(external_client_combo, external_account_combo)
    )

    submit_button.clicked.connect(
        lambda: make_transfer(transfer_type_combo, internal_dest_combo, 
                                   external_client_combo, external_account_combo, amount_input)
    )

    
    on_transfer_type_changed(0, internal_widgets, external_widgets)# initizlisartion en virement interne
    
    if available_clients: # On initialise la liste des comptes externes 
        on_external_client_changed(external_client_combo, external_account_combo)

    update_right_panel(main_window, container_widget)


def show_deposit(main_window):
    current_user = main_window.selected_user
    if not current_user:
        _show_selection_error(main_window)
        return

    container_widget = QWidget()
    container_widget.setStyleSheet("background-color: white;")
    main_layout = QVBoxLayout(container_widget)

    main_layout.addWidget(QLabel(f"<h2>Effectuer un Dépôt</h2><p>Client : {current_user.text()}</p>"))

    form_layout = QFormLayout()
    target_account_combo = QComboBox()
    for acc in _get_account_list(current_user):
        target_account_combo.addItem(acc["nom"], acc["id"])
    
    amount_input = QLineEdit()
    amount_input.setPlaceholderText("0.00 €")

    form_layout.addRow("Vers le compte :", target_account_combo)
    form_layout.addRow("Montant à déposer :", amount_input)
    
    main_layout.addLayout(form_layout)

    submit_button = QPushButton("Valider le dépôt")
    submit_button.clicked.connect(lambda: make_deposit(current_user, target_account_combo, amount_input))
    
    main_layout.addWidget(submit_button)
    main_layout.addStretch()

    update_right_panel(main_window, container_widget)


def show_retrait(main_window):
    current_user = main_window.selected_user
    if not current_user:
        _show_selection_error(main_window)
        return

    container_widget = QWidget()
    container_widget.setStyleSheet("background-color: white;")
    main_layout = QVBoxLayout(container_widget)

    main_layout.addWidget(QLabel(f"<h2>Effectuer un Retrait</h2><p>Client : {current_user.text()}</p>"))

    form_layout = QFormLayout()
    source_account_combo = QComboBox()
    for acc in _get_account_list(current_user):
        source_account_combo.addItem(acc["nom"], acc["id"])
    
    amount_input = QLineEdit()
    amount_input.setPlaceholderText("0.00 €")

    form_layout.addRow("Depuis le compte :", source_account_combo)
    form_layout.addRow("Montant à retirer :", amount_input)
    
    main_layout.addLayout(form_layout)

    submit_button = QPushButton("Valider le retrait")
    submit_button.clicked.connect(lambda: make_withdraw(current_user, source_account_combo, amount_input))
    
    main_layout.addWidget(submit_button)
    main_layout.addStretch()

    update_right_panel(main_window, container_widget)




def make_transfer(type_combo, int_dest_combo, ext_client_combo, ext_acc_combo, amount_input):
    #TODO, virer l'argent amount_input.text() depuis le compte int_dest_combo ou ext_acc_combo selon interne ou externe vers le compte sélectionné
    pass

def make_deposit(current_user, target_account_combo, amount_input):
    #TODO dans le controleur
    pass

def make_withdraw(current_user, source_account_combo, amount_input):
    #TODO dans le controleur
    pass