
import sys
import os
import Modele
from Modele import Compte
from Modele import Operation
from enum import Enum
from Modele.Compte import Compte, TypeCompte
from Modele.Operation import Operation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

def get_client_details(self, client_id):
    pass

def get_tous_les_clients() :
    pass

def ajouter_compte_client(client_id, type_compte : Compte.TypeCompte, solde_initial):
    Compte.creer(client_id, type_compte, solde_initial) #il faut qu'on ajoute l'id client mais pour l'instant il n'est pas en param de creer
    

def gerer_operation_espece(compte_id, montant, type_operation: Enum) : #il faut ajouter à la classe opération une enum : DEPOT = 0 /RETRAIT=1, je remplacerais "Enum" par son vrai nom
    match type_operation.value :
        case 0 :
            Operation.transferer(0, compte_id, montant) #source = compte, cible =banque
            return True 
        case 1 :
            solde = (Compte.obtenir(compte_id)).solde()
            if (solde>Compte.DECOUVERT_MAX):
                Operation.transferer(compte_id, 0, montant) #Inverse, eventuellement checker le découvert?
                return True
            else :
                return False, f"Solde insuffisant pour effectuer l'opération.\nSolde = {solde}, montant du retrait = {montant})"

def effectuer_virement(id_source, id_cible, montant) :
    solde = Compte.solde(Compte.obtenir(id_source))
    if (solde>Compte.DECOUVERT_MAX):
        Operation.transferer(id_source, id_cible, montant)
        return True 
    else :
        return False , f"Solde insuffisant pour effectuer l'opération.\nSolde = {solde}, montant du transfert = {montant}"

"""
Table Clients : Il faut une classe Client avec (id, nom, prenom, adresse, annee).

Lien Compte-Client : La table Comptes doit avoir une colonne client_id (ForeignKey).

Appartenance : Le Modèle doit te permettre de savoir facilement à qui appartient un compte (pour vérifier la règle "Virement Interne")
"""