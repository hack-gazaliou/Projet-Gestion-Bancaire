# Référence technique de l'API

This page contains technical documentation generated automatically from the project's docstrings.
---

## Model
The logical core and entities of the application.

### Main entities
::: gestion_bancaire.Modele.compte
::: gestion_bancaire.Modele.customer
::: gestion_bancaire.Modele.operation

### Data Access (SQL)
These modules manage persistence with the database.

::: gestion_bancaire.Modele.SQL.sql_manager
::: gestion_bancaire.Modele.SQL.db_setup
::: gestion_bancaire.Modele.SQL.sql_comptes
::: gestion_bancaire.Modele.SQL.sql_customer
::: gestion_bancaire.Modele.SQL.sql_operations

---

## Controller
The link between the Model and the View.

::: gestion_bancaire.Controleur.controleur

---

## View
The graphical user interface.

::: gestion_bancaire.Vue.vue_principale
::: gestion_bancaire.Vue.account_operations
::: gestion_bancaire.Vue.operations.account_view
::: gestion_bancaire.Vue.operations.base
::: gestion_bancaire.Vue.operations.deposit
::: gestion_bancaire.Vue.operations.transfer
::: gestion_bancaire.Vue.operations.withdraw