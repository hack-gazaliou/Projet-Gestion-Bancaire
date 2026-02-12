import os
import random
import sys

from Modele.Compte import Compte
from Modele.Customer import (
    Customer,
    CustomerCardInfo,
    CustomerContactInfo,
    CustomerPersonalInfo,
)
from Modele.Operation import Operation, TypeOperation
from Modele.SQL.sql_comptes import SQLCompte
from Modele.SQL.sql_manager import SessionLocal
from Modele.SQL.SQLCustomer import Customer as CustomerSQL
from Modele.type_compte import TypeCompte

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

DECOUVERT_MAX = 50_000


class Controller:
    def get_client_details(self, client_id):
        with SessionLocal() as session:
            client_obj = Customer.obtain(session, client_id)
            if not client_obj:
                return None
            details = {
                "nom": client_obj.personal_info.last_name,
                "prenom": client_obj.personal_info.first_name,
                "telephone": client_obj.contact_info.phone,
                "email": client_obj.contact_info.email,
                "adresse": client_obj.address,
            }
            return details

    def get_tous_les_clients(self):
        with SessionLocal() as session:
            clients_sql = session.query(CustomerSQL).all()
            liste_affichage = []
            for c in clients_sql:
                liste_affichage.append(
                    {
                        "id": c.customer_id,
                        "nom": f"{c.last_name.upper()} {c.first_name.capitalize()}",
                    }
                )
            return liste_affichage

    def creer_nouveau_client(self, nom, prenom, email, telephone, adresse):
        if not nom or not prenom:
            return False, "Le nom et le prénom sont obligatoires."

        faux_numero_carte = (
            f"FR76{''.join([str(random.randint(0, 9)) for _ in range(12)])}"
        )

        infos_perso = CustomerPersonalInfo(first_name=prenom, last_name=nom)
        infos_contact = CustomerContactInfo(phone=telephone, email=email)
        infos_carte = CustomerCardInfo(card_number=faux_numero_carte)

        nouveau_client = Customer(
            personal_info=infos_perso,
            contact_info=infos_contact,
            card_info=infos_carte,
            address=adresse,
            customer_id=None,
        )

        with SessionLocal() as session:
            try:
                nouveau_client.save(session)
                return (
                    True,
                    f"Client créé avec succès (ID: {nouveau_client.customer_id})",
                )
            except Exception as e:
                return False, f"Erreur : {e}"

    def ajouter_compte_client(self, client_id, type_compte_str, solde_initial):
        """
        Crée un compte en utilisant le constructeur __init__ du nouveau modèle.
        """
        try:
            type_enum = TypeCompte[type_compte_str]
        except KeyError:
            return False, f"Type de compte invalide : {type_compte_str}"

        try:
            # On passe account_id=None pour dire que c'est un nouveau compte
            nouveau_compte = Compte(
                account_id=None,
                type_compte=type_enum,
                id_client=client_id,
                initial_amount=solde_initial,
            )
            # Si aucune erreur n'est levée, c'est que c'est bon
            return True, "Compte créé avec succès."

        except Exception as e:
            return False, f"Erreur lors de la création : {e}"

    def get_comptes_client(self, client_id) -> list:
        """
        Récupère les comptes via SQLCompte, puis les transforme en objets Métier Compte
        pour avoir le calcul du solde.
        """
        with SessionLocal() as session:
            try:
                comptes_sql = (
                    session.query(SQLCompte).filter_by(id_client=client_id).all()
                )
            except Exception as e:
                print(f"Erreur SQL : {e}")
                return []

            data_comptes = []
            for c_sql in comptes_sql:
                compte_metier = Compte.load(c_sql.id)

                if compte_metier:
                    valeur_solde = compte_metier.solde
                    nom_type = compte_metier.get_type_compte().name

                    data_comptes.append(
                        {
                            "id": compte_metier.get_id(),
                            "type": nom_type,
                            "solde": f"{(valeur_solde / 100):.2f} €",
                        }
                    )
            return data_comptes

    def gerer_operation_espece(self, compte_id, montant, type_operation: TypeOperation):
        # Utilisation de LOAD (nouveau modèle Compte)
        compte = Compte.load(compte_id)
        if not compte:
            return False, "Compte introuvable"

        solde_init = compte.solde

        match type_operation.value:
            case 0:  # DEPOT
                # NOUVELLE LOGIQUE : Création objet -> execute()
                # 0 représente la banque
                op = Operation(0, compte_id, montant)
                op.execute()

                # On recharge le compte pour avoir le solde à jour
                solde_act = Compte.load(compte_id).solde
                return True, f"Dépôt effectué. Nouveau solde : {solde_act / 100:.2f} €"

            case 1:  # RETRAIT
                if (solde_init - montant) >= -DECOUVERT_MAX:
                    # NOUVELLE LOGIQUE
                    op = Operation(compte_id, 0, montant)
                    op.execute()

                    solde_act = Compte.load(compte_id).solde
                    return (
                        True,
                        f"Retrait effectué. Nouveau solde : {solde_act / 100:.2f} €",
                    )
                else:
                    return False, f"Solde insuffisant"

    def effectuer_virement(self, id_source, id_cible, montant):
        source = Compte.load(id_source)
        if not source:
            return False, "Compte source introuvable"

        solde_init = source.solde

        if (solde_init - montant) >= -DECOUVERT_MAX:
            # NOUVELLE LOGIQUE
            op = Operation(id_source, id_cible, montant)
            op.execute()

            return True, "Virement effectué."
        else:
            return False, "Solde insuffisant"
