"""
Unitary test for the Compte class and associated method
"""
from unittest.mock import patch, MagicMock
from Modele.compte import Compte
from Modele.type_compte import TypeCompte

class TestCompte:
    """
    Compte test class
    """
    @patch("Modele.compte.SQLCompte.creer")
    def test_init_nouveau_compte(self, mock_creer):
        """Test account creation (id=None)"""
        mock_creer.return_value = MagicMock(id=42)
        compte = Compte(account_id=None,
                        type_compte=TypeCompte.COURANT,
                        id_client=1,
                        initial_amount=100
                        )
        # Vérifications
        assert compte.get_id() == 42 
        mock_creer.assert_called_once_with(TypeCompte.COURANT, 1, 100)

    def test_init_compte_existant(self):
        """Test init of an existing account""" #noqa : E501
        with patch("Modele.compte.SQLCompte.creer") as mock_creer:
            compte = Compte(account_id=10, type_compte=TypeCompte.PEL, id_client=1)
            assert compte.get_id() == 10 # type:ignore
            mock_creer.assert_not_called()

            assert compte.get_id() == 10  # type:ignore
            mock_creer.assert_not_called()

    @patch("Modele.compte.SQLCompte.get_credits_and_debits")
    def test_propriete_solde(self, mock_get_amounts):
        """Test balance computation"""
        # On simule 500€ de crédits et 200€ de débits
        mock_get_amounts.return_value = (500, 200)
        compte = Compte(account_id=1, type_compte=TypeCompte.COURANT, id_client=1)
        assert compte.solde == 300
        mock_get_amounts.assert_called_with(1)

    @patch("Modele.compte.SQLCompte.get")
    def test_load_success(self, mock_get_sql):
        """Test account loading"""
        mock_db_obj = MagicMock()
        mock_db_obj.id = 99
        mock_db_obj.type_compte = TypeCompte.LIVRET_A
        mock_db_obj.id_client = 7
        mock_get_sql.return_value = mock_db_obj
        compte = Compte.load(99)
        assert compte.get_id()== 99# type:ignore
        assert compte.get_type_compte() == TypeCompte.LIVRET_A # type:ignore
        mock_get_sql.assert_called_once_with(99)

    @patch("Modele.compte.SQLCompte.get")
    @patch("Modele.compte.logger")
    def test_load_not_found(self, mock_logger, mock_get_sql):
        """Test account loading fail"""
        mock_get_sql.return_value = None
        compte = Compte.load(404)
        assert compte is None
        mock_logger.error.assert_called_with("Account not found")

    @patch("Modele.compte.SQLCompte.get_credits_and_debits")
    def test_repr(self, mock_get_amounts):
        """Test object display"""
        mock_get_amounts.return_value = (100, 20)
        compte = Compte(account_id=1, type_compte=TypeCompte.COURANT, id_client=1)
        attendu = "<Compte(id=1, type=COURANT)>"
        assert repr(compte) == attendu
