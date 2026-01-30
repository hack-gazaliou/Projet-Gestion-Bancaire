
import sys
import os
import Modele
from Modele import Compte
from Modele import Operation
from enum import Enum
from Modele.Compte import Compte, TypeCompte, Decouvert
from Modele.Operation import Operation, TypeOperation
from Modele.SQLManager import SessionLocal
#from Modele.Class_SQL.Customer_SQL import Customer as CustomerSQL
#from Modele.Customer import Customer 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

DECOUVERT_MAX = Decouvert.DECOUVERT_MAX

def get_client_details(self, client_id): # Renvoit les infos perso (hors compte)
    with SessionLocal() as session:
        client_obj = Customer.obtain(session, client_id)
        if not client_obj:
            return None
        details = {
            #"id": client_obj.customer_id,
            "nom": client_obj.personal_info.last_name,
            "prenom": client_obj.personal_info.first_name,
            "telephone": client_obj.contact_info.phone,
            "email": client_obj.contact_info.email,
            "adresse": client_obj.address,
        }
        return details

def get_tous_les_clients(self):#Récupère la liste (ID, Nom, Prénom) pour la sidebar.
    with SessionLocal() as session:
        clients_sql = session.query(CustomerSQL).all()
        liste_affichage = []
        for c in clients_sql:
            liste_affichage.append({
                "id": c.customer_id,
                "nom": f"{c.first_name.capitalize.capitalize()} {c.last_name.capitalize()}" 
            })   
        return liste_affichage

def ajouter_compte_client(self, client_id, type_compte, solde_initial):
    with SessionLocal() as session:
        # Vérification optionnelle : est-ce que ce client existe ?
        client = Customer.obtain(session, client_id)
        if not client:
            return False, "Client introuvable."
        try:
            Compte.creer(client_id, type_compte, solde_initial)
            return True, "Compte créé avec succès."
        except Exception as e:
            return False, f"Erreur lors de la création : {e}"

def get_comptes_client(self, client_id)->dict: #Récupère la liste des comptes d'un client et calcule leurs soldes à la volée.
        with SessionLocal() as session:
            try:
                comptes_du_client = session.query(Compte).filter_by(id_client=client_id).all() #ne devrait pas arriver pcq on a deja créé la colonne id_clilent, bon pour le debug
            except Exception as e:
                print(f"Erreur SQL : {e}")
                return []

            data_comptes = []
            for compte in comptes_du_client:
                # On accède à .solde sans parenthèses.
                valeur_solde = compte.solde 
                solde_formate = f"{(valeur_solde/100):.2f} €"
                # Récupération propre du nom de l'Enum (ex: LIVRET_A)
                nom_type = compte.type_compte.name if hasattr(compte.type_compte, 'name') else str(compte.type_compte)
                data_comptes.append({
                    "id": compte.id,
                    "type": nom_type,
                    "solde": solde_formate
                })
            return data_comptes
    
def gerer_operation_espece(compte_id, montant, type_operation: TypeOperation) : #enum de la classe opération: DEPOT = 0 /RETRAIT=1
    solde_init  = (Compte.obtenir(compte_id)).solde()
    match type_operation.value :
        case 0 :
            Operation.transferer(0, compte_id, montant) #source = compte, cible =banque
            solde_act = (Compte.obtenir(compte_id)).solde()
            return True,  f"Le depot de {montant/100} € a bien été effectué. Solde actuel : {solde_act/100} €."
        case 1 :
            if (solde_init - montant < 0 and abs(solde_init - montant) > DECOUVERT_MAX):
                Operation.transferer(compte_id, 0, montant) #inverse
                solde_act = (Compte.obtenir(compte_id)).solde()
                return True, f"Le retrait de {montant/100}€ a bien été effectué. Solde actuel : {solde_act/100}."
            else :
                return False, f"Solde insuffisant pour effectuer l'opération.\nSolde = {solde_init/100}, montant du retrait = {montant/100}. \n Découvert max autorisé : {DECOUVERT_MAX/100}."

def effectuer_virement(id_source, id_cible, montant) :
    solde_init = Compte.solde(Compte.obtenir(id_source))
    if (solde_init - montant < 0 and abs(solde_init - montant) > DECOUVERT_MAX):
        Operation.transferer(id_source, id_cible, montant)
        solde_act = Compte.solde(Compte.obtenir(id_source))
        return True, f"Virement de {montant/100} € effectué, solde actuel : {solde_act/100} €."
    else :
        return False , f"Solde insuffisant pour effectuer l'opération.\nSolde = {solde_init/100} €, montant du transfert = {montant/100} €\n Découvert max autorisé : {DECOUVERT_MAX/100} €"

"""
Table Clients : Il faut une classe Client avec (id, nom, prenom, adresse, annee).

Lien Compte-Client : La table Comptes doit avoir une colonne client_id (ForeignKey).

Appartenance : Le Modèle doit te permettre de savoir facilement à qui appartient un compte (pour vérifier la règle "Virement Interne")
"""