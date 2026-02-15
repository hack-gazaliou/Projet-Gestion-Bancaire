import os
import sys
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

# Configuration du path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "..")
sys.path.append(src_dir)

from Controleur.controleur import Controller  # noqa: E402


@pytest.fixture
def controller():
    return Controller()


@pytest.fixture
def mock_session():
    with patch("Controleur.controleur.SessionLocal") as mock_session_cls:
        yield mock_session_cls.return_value.__enter__.return_value


# TESTS CLIENTS


def test_get_tous_les_clients(controller, mock_session):
    c1 = MagicMock(customer_id=1, last_name="Dupont", first_name="Jean")
    c2 = MagicMock(customer_id=2, last_name="Martin", first_name="Sophie")
    mock_session.query.return_value.all.return_value = [c1, c2]

    resultat = controller.get_tous_les_clients()

    assert len(resultat) == 2
    assert resultat[0]["nom"] == "DUPONT Jean"


def test_get_client_details_succes(controller):
    fake_client = MagicMock()
    fake_client.personal_info.last_name = "Dupont"
    fake_client.personal_info.first_name = "Jean"
    fake_client.contact_info.email = "jean@test.com"

    with patch("Controleur.controleur.Customer.obtain", return_value=fake_client):
        details = controller.get_client_details(1)
        assert details["nom"] == "Dupont"


def test_creer_nouveau_client_succes(controller):
    with patch("Controleur.controleur.Customer") as MockCustomer:
        instance = MockCustomer.return_value
        instance.customer_id = 123

        succes, msg = controller.creer_nouveau_client(
            "Nom", "Prenom", "mail", "tel", "adr"
        )

        assert succes is True
        assert "123" in msg
        instance.save.assert_called_once()


# TESTS COMPTES


def test_ajouter_compte_client_succes(controller):
    with patch("Controleur.controleur.TypeCompte") as MockEnum:
        MockEnum.__getitem__.return_value = "MOCK_ENUM"
        with patch("Controleur.controleur.Compte") as MockCompteClass:
            succes, msg = controller.ajouter_compte_client(1, "COURANT", 100)
            assert succes is True
            MockCompteClass.assert_called_once()


def test_get_comptes_client(controller, mock_session):
    sql_compte = MagicMock(id=10)
    mock_session.query.return_value.filter_by.return_value.all.return_value = [
        sql_compte
    ]

    fake_metier = MagicMock()
    fake_metier.get_id.return_value = 10
    fake_metier.get_type_compte.return_value.name = "PEL"
    type(fake_metier).solde = PropertyMock(return_value=15000.0)

    with patch("Controleur.controleur.Compte.load", return_value=fake_metier):
        resultat = controller.get_comptes_client(1)
        assert len(resultat) == 1
        assert resultat[0]["solde"] == "150.00 €"


# TESTS OPERATIONS


def test_depot_espece(controller):
    fake_compte = MagicMock()
    type(fake_compte).solde = PropertyMock(side_effect=[0, 10000])

    with patch("Controleur.controleur.Compte.load", return_value=fake_compte):
        with patch("Controleur.controleur.Operation") as MockOperationClass:
            mock_op_instance = MockOperationClass.return_value

            succes, _ = controller.effectuer_depot(1, 100.0)

            assert succes is True

            MockOperationClass.assert_called_with(0, 1, 10000)
            mock_op_instance.execute.assert_called_once()


def test_retrait_espece_succes(controller):
    fake_compte = MagicMock()
    type(fake_compte).solde = PropertyMock(return_value=50000.0)

    with patch("Controleur.controleur.Compte.load", return_value=fake_compte):
        with patch("Controleur.controleur.Operation") as MockOperationClass:
            mock_op_instance = MockOperationClass.return_value

            succes, msg = controller.effectuer_retrait(1, 100.0)

            assert succes is True
            MockOperationClass.assert_called_with(1, 0, 10000)
            mock_op_instance.execute.assert_called_once()


def test_retrait_espece_insuffisant(controller):
    fake_compte = MagicMock()
    type(fake_compte).solde = PropertyMock(return_value=0.0)

    with patch("Controleur.controleur.Compte.load", return_value=fake_compte):
        with patch("Controleur.controleur.Operation") as MockOperationClass:
            _ = MockOperationClass.return_value

            succes, msg = controller.effectuer_retrait(1, 100000)

            assert succes is False
            assert "insuffisant" in msg
            MockOperationClass.assert_not_called()


def test_virement_succes(controller):
    source = MagicMock()
    type(source).solde = PropertyMock(return_value=10000.0)
    cible = MagicMock()

    with patch("Controleur.controleur.Compte.load", side_effect=[source, cible]):
        with patch("Controleur.controleur.Operation") as MockOperationClass:
            mock_op_instance = MockOperationClass.return_value

            succes, _ = controller.effectuer_virement(1, 2, 50.0)

            assert succes is True
            MockOperationClass.assert_called_with(1, 2, 5000)
            mock_op_instance.execute.assert_called_once()


def test_virement_compte_inconnu(controller):
    with patch("Controleur.controleur.Compte.load", return_value=None):
        succes, msg = controller.effectuer_virement(1, 2, 5000)
        assert succes is False
        assert "introuvable" in msg
