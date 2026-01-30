from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                               QDialogButtonBox, QLabel, QMessageBox)
from PySide6.QtCore import Qt
import VuePrincipale


def show_create_client_popup(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("Créer un nouveau client")
    layout = QVBoxLayout(dialog)

    form = QFormLayout()
    prenom_input = QLineEdit()
    nom_input = QLineEdit()
    tel_input = QLineEdit()
    email_input = QLineEdit()
    date_input = QLineEdit()
    adresse_input = QLineEdit()

    form.addRow("Prénom:", prenom_input)
    form.addRow("Nom:", nom_input)
    form.addRow("Téléphone:", tel_input)
    form.addRow("Email:", email_input)
    form.addRow("Date d'expiration:", date_input)
    form.addRow("Adresse:", adresse_input)

    layout.addLayout(form)

    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    layout.addWidget(buttons)

    buttons.accepted.connect(lambda: create_client(main_window, prenom_input, nom_input, tel_input,
                                                    email_input, date_input, adresse_input, dialog))
    buttons.rejected.connect(dialog.reject)

    dialog.exec()


def show_modify_client_popup(main_window):
    selected_item = main_window.selected_user 

    if not selected_item:
        QMessageBox.warning(main_window, "Aucun client sélectionné", "Veuillez sélectionner un client à modifier.")
        return

    client_id = selected_item.data(Qt.UserRole)
    infos = getInfos(client_id)

    dialog = QDialog(main_window)
    dialog.setWindowTitle("Modifier le client")
    layout = QVBoxLayout(dialog)

    form = QFormLayout()
    prenom_input = QLineEdit(infos.get("prenom", ""))
    nom_input = QLineEdit(infos.get("nom", ""))
    tel_input = QLineEdit(infos.get("telephone", ""))
    email_input = QLineEdit(infos.get("email", ""))
    date_input = QLineEdit(infos.get("date_exp", ""))
    adresse_input = QLineEdit(infos.get("adresse", ""))

    form.addRow("Prénom:", prenom_input)
    form.addRow("Nom:", nom_input)
    form.addRow("Téléphone:", tel_input)
    form.addRow("Email:", email_input)
    form.addRow("Date d'expiration:", date_input)
    form.addRow("Adresse:", adresse_input)

    layout.addLayout(form)

    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    layout.addWidget(buttons)

    buttons.accepted.connect(lambda: modify_client(main_window, prenom_input, nom_input, tel_input,
                                                    email_input, date_input, adresse_input, dialog))
    buttons.rejected.connect(dialog.reject)

    dialog.exec()




def create_client(main_window, prenom_input, nom_input, tel_input,
                   email_input, date_input, adresse_input, dialog):
    prenom = prenom_input.text().strip()
    nom = nom_input.text().strip()
    if not prenom or not nom:
        QMessageBox.warning(dialog, "Champs manquants", "Le prénom et le nom sont obligatoires.")
        return
    dialog.reject()
    #TODO enregistrer le nouveau client dans la base de données et refresh la liste
    main_window.reload_client_list()

def modify_client(main_window, prenom_input, nom_input, tel_input, email_input, date_input, adresse_input, dialog):
    dialog.reject()
    print("TODO")


def getInfos(client_id):
    # Valeurs par défaut génériques TODO
    return {
        "nom": "Sacha",
        "prenom": "Bliard",
        "telephone": "0123456789",
        "email": "sacha.bliard@example.com",
        "date_exp": "2026-12-31",
        "adresse": "1 rue Exemple, 75100 Strasbourg"
    }