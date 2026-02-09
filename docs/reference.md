# Référence technique de l'API

Cette page regroupe la documentation technique générée automatiquement à partir des docstrings du projet.

---

## Modèle (Modele)
Le cœur logique et les entités de l'application.

### Entités principales
::: Modele.Compte
::: Modele.Customer
::: Modele.Operation

### Accès aux données (SQL)
Ces modules gèrent la persistance avec la base de données.

::: Modele.SQL.sql_manager
::: Modele.SQL.db_setup
::: Modele.SQL.sql_comptes
::: Modele.SQL.sql_customer
::: Modele.SQL.sql_operations

---

## Contrôleur (Controleur)
Le lien entre le Modèle et la Vue.

::: Controleur

---

## Vue (Vue)
L'interface utilisateur graphique.

::: Vue.VuePrincipale
::: Vue.operations
::: Vue.account_operations