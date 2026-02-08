import os
import random
import sys
from enum import Enum

from Modele.Customer import (
    Customer,
    CustomerCardInfo,
    CustomerContactInfo,
    CustomerPersonalInfo,
)
from Modele.SQL.Customer_SQL import Customer as CustomerSQL
from Modele.Compte import Compte, Decouvert
from Modele.Operation import Operation, TypeOperation
from Modele.SQLManager import SessionLocal


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

DECOUVERT_MAX = Decouvert.DECOUVERT_MAX


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
                liste_affichage.append({
                    "id": c.customer_id,
                    "nom": f"{c.last_name.upper()} {c.first_name.capitalize()}",
                })
            return liste_affichage

    def creer_nouveau_client(self, nom, prenom, email, telephone, adresse):
        if not nom or not prenom:
            return False, "Le nom et le prénom sont obligatoires."
        
        faux_numero_carte = f"FR76{''.join([str(random.randint(0, 9)) for _ in range(12)])}"

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
                return True, f"Client créé avec succès (ID: {nouveau_client.customer_id})"
            except Exception as e:
                return False, f"Erreur : {e}"

    def ajouter_compte_client(self, client_id, type_compte, solde_initial):
        with SessionLocal() as session:
            client = Customer.obtain(session, client_id)
            if not client:
                return False, "Client introuvable."
            try:
                Compte.creer(client_id, type_compte, solde_initial)
                return True, "Compte créé avec succès."
            except Exception as e:
                return False, f"Erreur lors de la création : {e}"

    def get_comptes_client(self, client_id) -> list:
        with SessionLocal() as session:
            try:
                comptes_du_client = session.query(Compte).filter_by(id_client=client_id).all()
            except Exception as e:
                print(f"Erreur SQL : {e}")
                return []

            data_comptes = []
            for compte in comptes_du_client:
                valeur_solde = compte.solde
                
                nom_type = compte.type_compte.name if hasattr(compte.type_compte, "name") else str(compte.type_compte)
                
                data_comptes.append({
                    "id": compte.id, 
                    "type": nom_type, 
                    "solde": f"{(valeur_solde / 100):.2f} €"
                })
            return data_comptes


    def gerer_operation_espece(self, compte_id, montant, type_operation: TypeOperation):
        compte = Compte.obtenir(compte_id)
        if not compte: return False, "Compte introuvable"
        
        solde_init = compte.solde
        
        match type_operation.value:
            case 0: # DEPOT
                Operation.transferer(0, compte_id, montant)
                solde_act = Compte.obtenir(compte_id).solde
                return True, f"Dépôt de {montant/100}€ effectué. Nouveau solde : {solde_act/100:.2f} €"
            
            case 1: # RETRAIT
                if (solde_init - montant) >= -DECOUVERT_MAX:
                    Operation.transferer(compte_id, 0, montant)
                    solde_act = Compte.obtenir(compte_id).solde
                    return True, f"Retrait de {montant/100}€ effectué. Nouveau solde : {solde_act/100:.2f} €"
                else:
                    return False, f"Solde insuffisant (Découvert max: {DECOUVERT_MAX/100}€)"

    def effectuer_virement(self, id_source, id_cible, montant):
        source = Compte.obtenir(id_source)
        if not source: return False, "Compte source introuvable"
        solde_init = source.solde

        if (solde_init - montant) >= -DECOUVERT_MAX:
            Operation.transferer(id_source, id_cible, montant)
            solde_act = Compte.obtenir(id_source).solde
            return True, f"Virement de {montant/100}€ effectué. Nouveau solde : {solde_act/100:.2f} €"
        else:
            return False, f"Solde insuffisant (Découvert max : {DECOUVERT_MAX/100} €)"