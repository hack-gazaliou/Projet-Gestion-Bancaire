import Modele
from Modele import Compte
from Modele import Operation
from enum import Enum

def get_client_details(self, client_id):
        # Pour l'instant recherche dans une fausse liste de clients car on a pas encore d'objets clients
        client = next((c for c in self.mock_clients if c["id"] == client_id), None)
        if not client:
            return None

        # Récupérer les vrais comptes via SQLAlchemy
        comptes_details = []
        for compte_id in client["comptes_ids"]:
            compte_obj = Modele.Compte.obtenir(compte_id)
            if compte_obj:
                comptes_details.append({
                    "id": compte_obj.id,
                    "type": compte_obj.type_compte.name, 
                    "solde": f"{compte_obj.solde:.2f} €" 
                })
            else:
                # Si le compte est dans le mock mais pas en BDD
                comptes_details.append({
                    "id": compte_id, 
                    "type": "INCONNU", 
                    "solde": "N/A"
                })

        # Retourne un dictionnaire propre pour la Vue
        return {
            "nom_complet": f"{client['nom']} {client['prenom']}",
            "comptes": comptes_details
        }

def get_tous_les_clients() :
    pass

def ajouter_compte_client(client_id, type_compte : Compte.TypeCompte, solde_initial):
    Compte.creer(client_id, type_compte, solde_initial) #il faut qu'on ajoute l'id client mais pour l'instant il n'est pas en param de creer
    

def gerer_operation_espece(compte_id, montant, type_operation: Enum) : #il faut ajouter à la classe opération une enum : DEPOT = 0 /RETRAIT=1, je remplacerais "Enum" par son vrai nom
    match type_operation.value() :
        case 0 :
            Operation.transferer(compte_id, 0, montant) #source = compte, cible =banque
            return True 
        case 1 :
            solde = Compte.solde(Compte.obtenir(compte_id))
            if (solde>Compte.DECOUVERT_MAX):
                Operation.transferer(0, compte_id, montant) #Inverse, eventuellement checker le découvert?
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