from Modele.SQLManager import engine, Base, SessionLocal
from Modele.Compte import Compte, TypeCompte

def initialiser_bdd():
    Base.metadata.drop_all(bind=engine)
    print("Base de données vidée")
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée")
def initialiser_coffre_fort():
    with SessionLocal() as session:
        # On vérifie si le compte 0 existe déjà
        coffre = session.query(Compte).filter_by(id=0).first()
        
        if not coffre:
            # Pour forcer l'ID à 0 avec SQLAlchemy/SQLite
            coffre = Compte(id=0, type_compte=TypeCompte.COURANT)
            session.add(coffre)
            try:
                session.commit()
                print("Le Coffre-fort de la banque (ID 0) a été initialisé.")
            except Exception:
                session.rollback()
                # Certains systèmes n'aiment pas l'ID 0, on peut utiliser 999
                print("Note : L'ID 0 peut être réservé, vérifiez votre configuration.")