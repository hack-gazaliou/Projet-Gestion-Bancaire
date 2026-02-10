# Système de Gestion Bancaire

!!! info "Project status"
    The project is currently at version **0.1.0**. It is still under development.

## Description

Welcome to the  documentation for the **Banking Management** project. This application allows you to manage accounts and customers and perform internal and external financial transactions.
---

## Main features

* **Account Management**: Create, close and monitor balances.
* **Transactions**: Deposits, withdrawals, and transfers between accounts.
* **SQL Database**: Robust data persistence via SQLite.
* **MVC Architecture**: Clear separation between logic (Model), interface (View), and management (Controller).

---

## Quick installation

To install the project in development mode, use the following commands in your terminal:

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
pip install -e .
```
## Use it

To use the application after successful installation, simply use the command :
```bash
gestion_bancaire
```