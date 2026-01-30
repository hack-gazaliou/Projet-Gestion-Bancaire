# Référence technique de l'API

Cette page regroupe la documentation technique générée automatiquement à partir des docstrings du projet.

---

## Modèle (Modele)
Le cœur logique et les entités de l'application.

### Entités principales
::: src.Modele.Compte
::: src.Modele.Customer
::: src.Modele.Operation

### Accès aux données (SQL)
Ces modules gèrent la persistance avec la base de données.

::: src.Modele.SQL.SQLManager
::: src.Modele.SQL.DBSetup
::: src.Modele.SQL.SQLComptes
::: src.Modele.SQL.SQLCustomer
::: src.Modele.SQL.SQLOperations

---

## Contrôleur (Controleur)
Le lien entre le Modèle et la Vue.

::: src.Controleur

---

## Vue (Vue)
L'interface utilisateur graphique.

::: src.Vue.VuePrincipale
::: src.Vue.operations
::: src.Vue.account_operations
