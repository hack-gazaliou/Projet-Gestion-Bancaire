"""Module gérant les opérations bancaires (virements, dépôts, retraits)"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QFormLayout,
    QMessageBox,
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt


def update_right_panel(main_window, new_widget):
    """Fonction pour remplacer le widget de droite."""
    main_window.content_layout.replaceWidget(main_window.right_panel_widget, new_widget)
    main_window.right_panel_widget.deleteLater()
    main_window.right_panel_widget = new_widget


def show_selection_error(main_window):
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


def get_account_list(client_item=None):  # pylint: disable=unused-argument
    """Retourne une liste de comptes simulée pour un client donné."""
    return [
        {"id": 101, "nom": "Compte Courant"},
        {"id": 102, "nom": "Livret A"},
        {"id": 103, "nom": "PEL"},
        {"id": 104, "nom": "PEL 2"},
    ]


def on_transfer_type_changed(index, internal_widgets, external_widgets):
    """Gère l'affichage/masquage des champs selon le type de virement."""
    is_internal = index == 0

    for widget in internal_widgets:
        widget.setVisible(is_internal)

    for widget in external_widgets:
        widget.setVisible(not is_internal)


def on_external_client_changed(ext_client_combo, ext_account_combo):
    """Met à jour la liste des comptes quand on change de client beneficiaire."""
    ext_account_combo.clear()
    client_id = ext_client_combo.currentData()
    accounts = get_account_list(client_id)
    for acc in accounts:
        ext_account_combo.addItem(acc["nom"], acc["id"])


def show_transfer(main_window):
    """Construit et affiche l'interface de virement."""
    current_user = main_window.selected_user

    if not current_user:
        show_selection_error(main_window)
        return

    container_widget = QWidget()
    container_widget.setStyleSheet("background-color: white;")
    main_layout = QVBoxLayout(container_widget)

    main_layout.addWidget(
        QLabel(f"<h2>Effectuer un Virement</h2><p>Émetteur : {current_user.text()}</p>")
    )

    form_layout = QFormLayout()

    # regroupement dans dictionnaire pour pylint et éviter les variables locales multiples
    ui_widgets = {
        "type_combo": QComboBox(),
        "source_combo": QComboBox(),
        "dest_combo": QComboBox(),
        "ext_client_combo": QComboBox(),
        "ext_account_combo": QComboBox(),
        "amount_input": QLineEdit(),
    }

    ui_widgets["type_combo"].addItems(["Virement Interne", "Virement Externe"])
    ui_widgets["amount_input"].setPlaceholderText("0.00 €")
    ui_widgets["amount_input"].setValidator(QIntValidator(0, 9999, ui_widgets["amount_input"]))

    for acc in get_account_list(current_user):
        ui_widgets["source_combo"].addItem(acc["nom"], acc["id"])
        ui_widgets["dest_combo"].addItem(acc["nom"], acc["id"])

    current_user_id = current_user.data(Qt.UserRole)
    available_clients = [c for c in main_window.db_clients if c["id"] != current_user_id]
    for client in available_clients:
        ui_widgets["ext_client_combo"].addItem(client["nom"], client["id"])

    internal_dest_label = QLabel("Compte crédité :")
    external_client_label = QLabel("Bénéficiaire :")
    external_account_label = QLabel("Compte bénéficiaire :")

    form_layout.addRow("<b>Type de virement :</b>", ui_widgets["type_combo"])
    form_layout.addRow("Compte débité :", ui_widgets["source_combo"])
    form_layout.addRow(internal_dest_label, ui_widgets["dest_combo"])
    form_layout.addRow(external_client_label, ui_widgets["ext_client_combo"])
    form_layout.addRow(external_account_label, ui_widgets["ext_account_combo"])
    form_layout.addRow("Montant :", ui_widgets["amount_input"])

    main_layout.addLayout(form_layout)

    submit_button = QPushButton("Exécuter le virement")
    main_layout.addWidget(submit_button)
    main_layout.addStretch()

    internal_widgets = [internal_dest_label, ui_widgets["dest_combo"]]
    external_widgets = [
        external_client_label,
        ui_widgets["ext_client_combo"],
        external_account_label,
        ui_widgets["ext_account_combo"],
    ]

    ui_widgets["type_combo"].currentIndexChanged.connect(
        lambda idx: on_transfer_type_changed(idx, internal_widgets, external_widgets)
    )

    ui_widgets["ext_client_combo"].currentIndexChanged.connect(
        lambda: on_external_client_changed(
            ui_widgets["ext_client_combo"], ui_widgets["ext_account_combo"]
        )
    )

    submit_button.clicked.connect(
        lambda: prepare_transfer(main_window, ui_widgets)
    )

    on_transfer_type_changed(0, internal_widgets, external_widgets)

    if available_clients:
        on_external_client_changed(
            ui_widgets["ext_client_combo"], ui_widgets["ext_account_combo"]
        )

    update_right_panel(main_window, container_widget)


def show_deposit(main_window):
    """Construit et affiche l'interface de dépôt."""
    current_user = main_window.selected_user
    if not current_user:
        show_selection_error(main_window)
        return

    container_widget = QWidget()
    container_widget.setStyleSheet("background-color: white;")
    main_layout = QVBoxLayout(container_widget)

    main_layout.addWidget(
        QLabel(f"<h2>Effectuer un Dépôt</h2><p>Client : {current_user.text()}</p>")
    )

    form_layout = QFormLayout()
    account_combo = QComboBox()
    for acc in get_account_list(current_user):
        account_combo.addItem(acc["nom"], acc["id"])

    amount_input = QLineEdit()
    amount_input.setPlaceholderText("0.00 €")
    amount_input.setValidator(QIntValidator(0, 9999, amount_input))

    form_layout.addRow("Vers le compte :", account_combo)
    form_layout.addRow("Montant à déposer :", amount_input)

    main_layout.addLayout(form_layout)

    submit_button = QPushButton("Valider le dépôt")
    submit_button.clicked.connect(
        lambda: prepare_deposit(main_window, account_combo, amount_input)
    )

    main_layout.addWidget(submit_button)
    main_layout.addStretch()

    update_right_panel(main_window, container_widget)


def show_retrait(main_window):
    """Construit et affiche l'interface de retrait."""
    current_user = main_window.selected_user
    if not current_user:
        show_selection_error(main_window)
        return

    container_widget = QWidget()
    container_widget.setStyleSheet("background-color: white;")
    main_layout = QVBoxLayout(container_widget)

    main_layout.addWidget(
        QLabel(f"<h2>Effectuer un Retrait</h2><p>Client : {current_user.text()}</p>")
    )

    form_layout = QFormLayout()
    account_combo = QComboBox()
    for acc in get_account_list(current_user):
        account_combo.addItem(acc["nom"], acc["id"])

    amount_input = QLineEdit()
    amount_input.setPlaceholderText("0.00 €")
    amount_input.setValidator(QIntValidator(0, 9999, amount_input))

    form_layout.addRow("Depuis le compte :", account_combo)
    form_layout.addRow("Montant à retirer :", amount_input)

    main_layout.addLayout(form_layout)

    submit_button = QPushButton("Valider le retrait")
    submit_button.clicked.connect(
        lambda: prepare_withdraw(main_window, account_combo, amount_input)
    )

    main_layout.addWidget(submit_button)
    main_layout.addStretch()

    update_right_panel(main_window, container_widget)


def prepare_transfer(main_window, ui_widgets):
    """Prépare et valide les données avant d'exécuter un virement."""
    amount_text = ui_widgets["amount_input"].text()
    if amount_text == "" or int(amount_text) == 0:
        QMessageBox.warning(
            main_window,
            "Montant invalide",
            "Veuillez entrer un montant strictement positif.",
        )
        return

    index_source = ui_widgets["source_combo"].currentIndex()
    source_account_id = ui_widgets["source_combo"].itemData(index_source)
    transfer_type = ui_widgets["type_combo"].currentText()
    amount_cents = int(amount_text) * 100

    if transfer_type == "Virement Interne":
        index_dest = ui_widgets["dest_combo"].currentIndex()
        dest_account_id = ui_widgets["dest_combo"].itemData(index_dest)
        print(
            f"Virement interne: compte source {source_account_id} "
            f"compte destinataire {dest_account_id} "
            f"d'un montant de {amount_cents}"
        )
    elif transfer_type == "Virement Externe":
        index_dest = ui_widgets["ext_account_combo"].currentIndex()
        dest_account_id = ui_widgets["ext_account_combo"].itemData(index_dest)
        print(
            f"Virement externe: compte source {source_account_id} "
            f"compte destinataire {dest_account_id} "
            f"d'un montant de {amount_cents}"
        )


def prepare_deposit(main_window, account_combo, amount_input):
    """Prépare et valide les données avant d'exécuter un dépôt."""
    amount_text = amount_input.text()
    if amount_text == "" or int(amount_text) == 0:
        QMessageBox.warning(
            main_window,
            "Montant invalide",
            "Veuillez entrer un montant strictement positif.",
        )
        return
    index_source = account_combo.currentIndex()
    account_id = account_combo.itemData(index_source)
    print(f"Compte {account_id} montant {int(amount_text)}")


def prepare_withdraw(main_window, account_combo, amount_input):
    """Prépare et valide les données avant d'exécuter un retrait."""
    amount_text = amount_input.text()
    if amount_text == "" or int(amount_text) == 0:
        QMessageBox.warning(
            main_window,
            "Montant invalide",
            "Veuillez entrer un montant strictement positif.",
        )
        return
    index_source = account_combo.currentIndex()
    account_id = account_combo.itemData(index_source)
    print(f"Compte {account_id} montant {int(amount_text) * 100}")