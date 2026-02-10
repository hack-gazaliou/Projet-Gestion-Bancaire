import os
import sys
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "..")
sys.path.append(src_dir)


from Controleur.controleur import Controller  # noqa: E402


@pytest.fixture
def controller():
    """Crée un contrôleur neuf avant chaque test"""
    return Controller()


@pytest.fixture
def mock_session():
    """
    Empêche le contrôleur de parler à la vraie BDD.
    Remplace SessionLocal par un faux objet magique.
    """
    with patch("Controleur.controleur.SessionLocal") as mock_session_cls:
        session_instance = mock_session_cls.return_value.__enter__.return_value
        yield session_instance


def test_creer_nouveau_client_succes(controller, mock_session):
    # GIVEN (Ce qu'on prépare)
    # On mocke la classe Customer pour ne pas toucher au SQL
    with patch("Controleur.controleur.Customer") as MockCustomer:
        # On configure le faux client pour qu'il ait un ID après sauvegarde
        fake_client_instance = MockCustomer.return_value
        fake_client_instance.customer_id = 999

        # WHEN (L'action)
        succes, message = controller.creer_nouveau_client(
            nom="Dupont",
            prenom="Jean",
            email="test@test.com",
            telephone="0600000000",
            adresse="Paris",
        )

        # THEN (La vérification)
        assert succes is True
        assert "999" in message
        # Vérifie que la méthode .save() a bien été appelée une fois
        fake_client_instance.save.assert_called_once()


# --- 5. EXEMPLE DE TEST (Virement Refusé) ---


def test_virement_refuse_solde_insuffisant(controller, mock_session):
    # GIVEN
    # On simule un compte avec 10€
    compte_source = MagicMock()
    # On utilise PropertyMock car .solde est une @property
    type(compte_source).solde = PropertyMock(return_value=10.0)

    compte_cible = MagicMock()

    # On injecte ces faux comptes quand le contrôleur fera Compte.obtenir()
    with patch(
        "Controleur.controleur.Compte.obtenir",
        side_effect=[compte_source, compte_cible],
    ):
        # WHEN (Tentative de virement de 1000€ alors qu'on a 10€)
        succes, msg = controller.effectuer_virement(1, 2, 1000.0)

        # THEN
        assert succes is False
        assert "Solde insuffisant" in msg
