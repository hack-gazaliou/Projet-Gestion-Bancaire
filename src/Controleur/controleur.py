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
from Modele.Operation import Operation
from Modele.SQL.sql_comptes import SQLCompte
from Modele.SQL.sql_manager import SessionLocal
from Modele.SQL.SQLCustomer import Customer as CustomerSQL
from Modele.type_compte import TypeCompte

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# 500.00 € = 50 000 centimes
DECOUVERT_MAX = 50_000


class Controller:
    # --- UTILITAIRES DE CONVERSION ---
    def _euros_vers_centimes(self, montant_euros: float) -> int:
        """Convertit 10.50€ en 1050 cts"""
        return int(round(float(montant_euros) * 100))

    # --- LECTURE ---
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

    def get_comptes_client(self, client_id) -> list:
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

                        if client_id == 0:
                            solde_str = "∞"
                        else:
                            solde_str = f"{(valeur_solde / 100):.2f} €"
                        # --------------------------------------------

                        data_comptes.append(
                            {
                                "id": compte_metier.get_id(),
                                "type": nom_type,
                                "solde": solde_str,
                            }
                        )
                return data_comptes

    # --- ECRITURE ---

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

    def mettre_a_jour_client(self, client_id, nom, prenom, email, telephone, adresse):
        try:
            with SessionLocal() as session:
                client = (
                    session.query(CustomerSQL).filter_by(customer_id=client_id).first()
                )
                if not client:
                    return False, "Client introuvable."

                client.first_name = prenom
                client.last_name = nom
                client.email = email
                client.phone = telephone
                client.address = adresse

                session.commit()
                return True, "Mise à jour réussie."
        except Exception as e:
            return False, f"Erreur SQL : {e}"

    def ajouter_compte_client(self, client_id, type_compte_str, solde_initial_euros):
        try:
            type_enum = TypeCompte[type_compte_str]
        except KeyError:
            return False, f"Type de compte invalide : {type_compte_str}"

        try:
            # CONVERSION : Euros (Input) -> Centimes (BDD)
            solde_initial_centimes = self._euros_vers_centimes(solde_initial_euros)

            Compte(
                account_id=None,
                type_compte=type_enum,
                id_client=client_id,
                initial_amount=solde_initial_centimes,  # On passe des centimes
            )
            return True, "Compte créé avec succès."

        except Exception as e:
            return False, f"Erreur lors de la création : {e}"

    def effectuer_depot(self, compte_id, montant_euros):
        try:
            # CONVERSION
            montant_centimes = self._euros_vers_centimes(montant_euros)
            if montant_centimes <= 0:
                return False, "Le montant doit être positif."

            compte = Compte.load(compte_id)
            if not compte:
                return False, "Compte introuvable"

            # 0 = Banque/Cash vers Compte
            op = Operation(0, compte_id, montant_centimes)
            op.execute()

            solde_act = Compte.load(compte_id).solde
            return True, f"Dépôt effectué. Nouveau solde : {solde_act / 100:.2f} €"
        except Exception as e:
            return False, str(e)

    def effectuer_retrait(self, compte_id, montant_euros):
        try:
            # CONVERSION
            montant_centimes = self._euros_vers_centimes(montant_euros)
            if montant_centimes <= 0:
                return False, "Le montant doit être positif."

            compte = Compte.load(compte_id)
            if not compte:
                return False, "Compte introuvable"

            solde_init = compte.solde  # Déjà en centimes

            if (solde_init - montant_centimes) >= -DECOUVERT_MAX:
                # Compte vers 0 (Banque/Cash)
                op = Operation(compte_id, 0, montant_centimes)
                op.execute()

                solde_act = Compte.load(compte_id).solde
                return (
                    True,
                    f"Retrait effectué. Nouveau solde : {solde_act / 100:.2f} €",
                )
            else:
                return False, "Solde insuffisant"
        except Exception as e:
            return False, str(e)

    def effectuer_virement(self, id_source, id_cible, montant_euros):
        try:
            # CONVERSION
            montant_centimes = self._euros_vers_centimes(montant_euros)
            if montant_centimes <= 0:
                return False, "Le montant doit être positif."

            source = Compte.load(id_source)
            if not source:
                return False, "Compte source introuvable"

            solde_init = source.solde  # En centimes

            # Cas spécial Banque (ID 0)
            if id_source == 0:
                Operation(id_source, id_cible, montant_centimes).execute()
                return True, "Virement Banque effectué."

            if (solde_init - montant_centimes) >= -DECOUVERT_MAX:
                op = Operation(id_source, id_cible, montant_centimes)
                op.execute()
                return True, "Virement effectué."
            else:
                return False, "Solde insuffisant"
        except Exception as e:
            return False, f"Erreur virement: {e}"

    def cloturer_compte(self, id_compte):
        try:
            compte_metier = Compte.load(id_compte)
            if not compte_metier:
                return False, "Compte introuvable."

            if compte_metier.solde != 0:
                solde_euros = compte_metier.solde / 100
                return (
                    False,
                    f"Solde non nul ({solde_euros:.2f} €). Impossible de clôturer.",
                )

            sql_compte = SQLCompte.get(id_compte)
            if sql_compte:
                sql_compte.supprimer()
                return True, "Compte clôturé avec succès."
            return False, "Erreur technique lors de la suppression."

        except Exception as e:
            return False, f"Erreur lors de la clôture : {e}"
