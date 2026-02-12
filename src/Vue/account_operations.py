from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)


def show_create_client_popup(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("Créer un nouveau client")
    layout = QVBoxLayout(dialog)

    form = QFormLayout()
    prenom_input = QLineEdit()
    nom_input = QLineEdit()
    tel_input = QLineEdit()
    email_input = QLineEdit()
    adresse_input = QLineEdit()

    form.addRow("Prénom:", prenom_input)
    form.addRow("Nom:", nom_input)
    form.addRow("Téléphone:", tel_input)
    form.addRow("Email:", email_input)
    form.addRow("Adresse:", adresse_input)

    layout.addLayout(form)

    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    layout.addWidget(buttons)

    buttons.accepted.connect(
        lambda: create_client(
            main_window,
            prenom_input,
            nom_input,
            tel_input,
            email_input,
            adresse_input,
            dialog,
        )
    )
    buttons.rejected.connect(dialog.reject)

    dialog.exec()


def show_modify_client_popup(main_window):
    selected_item = main_window.selected_user

    if not selected_item:
        QMessageBox.warning(
            main_window,
            "Aucun client sélectionné",
            "Veuillez sélectionner un client à modifier.",
        )
        return

    client_id = selected_item.data(Qt.UserRole)

    infos = main_window.controller.get_client_details(client_id)

    if not infos:
        QMessageBox.critical(
            main_window, "Erreur", "Impossible de récupérer les infos du client."
        )
        return

    dialog = QDialog(main_window)
    dialog.setWindowTitle(f"Modifier {infos['nom']}")
    layout = QVBoxLayout(dialog)

    form = QFormLayout()

    prenom_input = QLineEdit(infos.get("prenom", ""))
    nom_input = QLineEdit(infos.get("nom_famille", ""))

    if not nom_input.text() and "nom" in infos:
        parts = infos["nom"].split(" ")
        if len(parts) > 1:
            nom_input.setText(parts[0])
            prenom_input.setText(" ".join(parts[1:]))
        else:
            nom_input.setText(infos["nom"])

    tel_input = QLineEdit(infos.get("telephone", ""))
    email_input = QLineEdit(infos.get("email", ""))
    adresse_input = QLineEdit(infos.get("adresse", ""))

    form.addRow("Prénom:", prenom_input)
    form.addRow("Nom:", nom_input)
    form.addRow("Téléphone:", tel_input)
    form.addRow("Email:", email_input)
    form.addRow("Adresse:", adresse_input)

    layout.addLayout(form)

    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    layout.addWidget(buttons)

    buttons.accepted.connect(
        lambda: modify_client(
            main_window,
            client_id,
            prenom_input,
            nom_input,
            tel_input,
            email_input,
            adresse_input,
            dialog,
        )
    )
    buttons.rejected.connect(dialog.reject)

    dialog.exec()


def create_client(
    main_window, prenom_inp, nom_inp, tel_inp, email_inp, adr_inp, dialog
):
    prenom = prenom_inp.text().strip()
    nom = nom_inp.text().strip()

    if not prenom or not nom:
        QMessageBox.warning(dialog, "Erreur", "Nom et Prénom obligatoires.")
        return

    succes, msg = main_window.controller.creer_nouveau_client(
        nom=nom,
        prenom=prenom,
        email=email_inp.text().strip(),
        telephone=tel_inp.text().strip(),
        adresse=adr_inp.text().strip(),
    )

    if succes:
        QMessageBox.information(dialog, "Succès", f"Client créé : {msg}")
        dialog.accept()
        main_window.reload_client_list()
    else:
        QMessageBox.critical(dialog, "Erreur", f"Erreur lors de la création : {msg}")


def modify_client(
    main_window, client_id, prenom_inp, nom_inp, tel_inp, email_inp, adr_inp, dialog
):
    succes, msg = main_window.controller.mettre_a_jour_client(
        client_id=client_id,
        nom=nom_inp.text().strip(),
        prenom=prenom_inp.text().strip(),
        email=email_inp.text().strip(),
        telephone=tel_inp.text().strip(),
        adresse=adr_inp.text().strip(),
    )

    if succes:
        QMessageBox.information(dialog, "Succès", "Informations mises à jour.")
        dialog.accept()
        main_window.reload_client_list()
        if (
            main_window.selected_user
            and main_window.selected_user.data(Qt.UserRole) == client_id
        ):
            main_window.show_account(main_window.selected_user)
    else:
        QMessageBox.critical(dialog, "Erreur", f"Échec mise à jour : {msg}")
