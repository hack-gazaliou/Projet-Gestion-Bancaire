from unittest.mock import patch, MagicMock
from Modele.Compte import Compte, TypeCompte

class TestCompte:

    @patch("Modele.Compte.SQLCompte.creer")
    def test_init_nouveau_compte(self, mock_creer):
        """Teste la création d'un compte qui n'existe pas encore (id=None)"""
        mock_creer.return_value = MagicMock(id=42)
        
        compte = Compte(id=None, 
                        type_compte=TypeCompte.COURANT, 
                        id_client=1, 
                        initial_amount=100
                        )
        
        # Vérifications
        assert compte._id == 42 # type:ignore
        mock_creer.assert_called_once_with(TypeCompte.COURANT, 1, 100)

    def test_init_compte_existant(self):
        """Teste l'init d'un compte déjà existant (ne doit pas appeler SQLCompte.creer)""" #noqa : E501
        with patch("Modele.Compte.SQLCompte.creer") as mock_creer:
            compte = Compte(id=10, type_compte=TypeCompte.PEL, id_client=1)
            
            assert compte._id == 10 # type:ignore
            mock_creer.assert_not_called()


    @patch("Modele.Compte.SQLCompte.get_credits_and_debits")
    def test_propriete_solde(self, mock_get_amounts):
        """Teste le calcul du solde (total_credits - total_debits)"""
        # On simule 500€ de crédits et 200€ de débits
        mock_get_amounts.return_value = (500, 200)
        
        compte = Compte(id=1, type_compte=TypeCompte.COURANT, id_client=1)
        
        assert compte.solde == 300
        mock_get_amounts.assert_called_with(1)

    @patch("Modele.Compte.SQLCompte.get")
    def test_load_success(self, mock_get_sql):
        """Teste le chargement réussi d'un compte"""
        # On simule un objet retourné par SQLAlchemy
        mock_db_obj = MagicMock()
        mock_db_obj.id = 99
        mock_db_obj.type_compte = TypeCompte.LIVRET_A
        mock_db_obj.id_client = 7
        mock_get_sql.return_value = mock_db_obj
        
        compte = Compte.load(99)
        assert compte._id == 99# type:ignore
        assert compte._type_compte == TypeCompte.LIVRET_A # type:ignore
        mock_get_sql.assert_called_once_with(99)

    @patch("Modele.Compte.SQLCompte.get")
    @patch("Modele.Compte.logger")
    def test_load_not_found(self, mock_logger, mock_get_sql):
        """Teste le comportement quand le compte n'existe pas"""
        mock_get_sql.return_value = None
        
        compte = Compte.load(404)
        
        assert compte is None
        mock_logger.error.assert_called_with("Account not found")


    @patch("Modele.Compte.SQLCompte.get_credits_and_debits")
    def test_repr(self, mock_get_amounts):
        """Teste l'affichage de l'objet"""
        mock_get_amounts.return_value = (100, 20)
        compte = Compte(id=1, type_compte=TypeCompte.COURANT, id_client=1)
        
        attendu = "<Compte(id=1, type=COURANT, solde=80€)>"
        assert repr(compte) == attendu    