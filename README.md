## Projet-Gestion-Bancaire

# Présentation du sytème.
Système de gestion de comptes bancaires pour un conseiller. Création de compte, dépôt/retrait  d’argent et virement bancaires entre comptes
Modification.
Le projet consiste en un application GUI développée via PySide. Elle est destinée à servir à un conseiller bancaire dans ses tâches.
Parmi les fonctionnalités implémentées on compte :
    - La possibilité de transférer des fonds d'un compte à un autre, dans le respect des contraintes liées aux différents types de comptes   considérés (PEL, Livret A, Compte courant).
    - L'ouverture et la fermeture de comptes bancaires pour ses clients.
    - La création de compte personnels pour chacun des client, associés à leurs informations personnelles et à leur comptes bancaires (cela dit, la gestion des comptes d'un point de vue client n''est pas garantie).

# Outils de développement 
En plus de l'utilisation de Pylance pour l'UI, on utilisera ici :
    - numpy et autres librairie classique pour la gestion des flux et des stocks numériques.
    - git et github pour la gestion des versions et du développement collaboratif.
    - DB SQLite pour la manipulation et le stockage des données utilisateurs.
    - Le reste à compléter...

# Installation
Avec environnement virtuel (recommandé).
Pour installer le projet sur votre ordinateur utilisez les commandes suivantes:

```bash
# Clone the repository
git clone https://github.com/hack-gazaliou/Projet-Gestion-Bancaire
cd Projet-Gestion-Bancaire

# Create and activate the virtual environnement
python -m venv .venv

# On linux:
source ".venv/bin/activate" 
# On Windows: 
source ".venv\Scripts\activate"

# Install dependencies
pip install requirements.txt
pip install -e .
```
## Utilisation

Pour l'utiliser, dans un terminal, entrez la commande :
```bash
gestion_bancaire
```
Lors de la première utilisation vous aurez besoin de créer la base de données. Pour cela utilisez la commande :
```bash
gestion_bancaire_init
```
Pour une base de données avec clients fictifs ou :
 ```bash
gestion_bancaire_init --clear
```
Pour une base de données vide.

# Note
Une documentation plus complète est également disponible à l'adresse : https://hack-gazaliou.github.io/Projet-Gestion-Bancaire/

