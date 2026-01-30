
import sys
import os
import Modele
from Modele import Compte
from Modele import Operation
from enum import Enum
from Modele.Compte import Compte, TypeCompte, Decouvert
from Modele.Operation import Operation
#from Modele.Customer import Customer 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

DECOUVERT_MAX = Decouvert.DECOUVERT_MAX

def get_client_details(self, client_id):
    pass

def get_tous_les_clients() :
    pass

def ajouter_compte_client(client_id, type_compte :TypeCompte, solde_initial):
    Compte.creer(client_id, type_compte, solde_initial) #il faut qu'on ajoute l'id client mais pour l'instant il n'est pas en param de creer
    

def gerer_operation_espece(compte_id, montant, type_operation: Enum) : #il faut ajouter à la classe opération une enum : DEPOT = 0 /RETRAIT=1, je remplacerais "Enum" par son vrai nom
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