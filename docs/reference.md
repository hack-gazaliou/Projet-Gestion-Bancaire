# Référence technique de l'API

This page contains technical documentation generated automatically from the project's docstrings.
---

## Model
The logical core and entities of the application.

### Main entities
::: Modele.Compte
::: Modele.Customer
::: Modele.Operation

### Data Access (SQL)
These modules manage persistence with the database.

::: Modele.SQL.sql_manager
::: Modele.SQL.db_setup
::: Modele.SQL.sql_comptes
::: Modele.SQL.SQLCustomer
::: Modele.SQL.sql_operations

---

## Controller
The link between the Model and the View.

::: Controleur

---

## View
The graphical user interface.

::: Vue.vue_principale
::: Vue.account_operations
::: Vue.operations.account_view
::: Vue.operations.base
::: Vue.operations.deposit
::: Vue.operations.transfer
::: Vue.operations.withdraw