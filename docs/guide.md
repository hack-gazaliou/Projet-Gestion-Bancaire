# User Guide: Banking Consultant Dashboard

Welcome to the **Bank Management** tool. This guide is designed to help you navigate the interface and perform daily operations like managing accounts, processing transfers, and updating client information.

---

## Interface Overview

The application is divided into three main areas:

1.  **Top Navigation Bar**: Access global actions (Accounts, Transfers, Deposits, Withdrawals, Edit Info).
2.  **Left Sidebar**: Search for existing clients or create new ones.
3.  **Main Panel**: View detailed information and account balances for the selected client.

---

## 1. Managing Clients and Accounts

### Selecting a Client
To perform any action, you must first select a client:
* Use the **Search Bar** in the left sidebar to type a client's name.
* Click on a name in the list. The central panel will update with their personal details and bank accounts.
* Click the **Refresh** button if you need to update the client list from the database.

### Viewing Account Details
Once a client is selected, the main panel displays:
* **Personal Info**: Name, Email, and Phone number.
* **Bank Accounts**: A list showing the account type (e.g., COURANT, LIVRET_A), Account ID, and the current balance.

### Opening a New Account
1.  Select a client in the sidebar.
2.  Click the green **+ Ouvrir un compte** (+ Open an account) button in the main panel.
3.  Select the account type from the dropdown menu (Courant, Livret A, or PEL).
4.  Confirm. The account is created with a default balance of **0.00 €**.

### Closing an Account
1.  Locate the specific account in the client's list.
2.  Click the red **Clôturer** (Close) button.
3.  Confirm the action. 
    * **Note**: An account can only be closed if the balance is exactly **0.00 €**. If the balance is not zero, the system will prevent the closure.

---

## 2. Bank Transfers (Virements)

The **Virements** menu allows you to move money between accounts electronically.

1.  Click **Virements** in the top navigation bar.
2.  **Internal Transfer**: Choose a "Source" and "Target" account belonging to the same client.
3.  **External Transfer**: Select a "Source" account from the current client and specify a "Target" account ID belonging to a different client.
4.  Enter the amount and confirm. 
    * The system validates if the source account has sufficient funds (respecting the authorized overdraft limit).

---

## 3. Deposits (Dépôts)

Use this menu when a client brings cash to the desk to credit an account.

1.  Select the client in the sidebar.
2.  Click **Depot** in the top navigation bar.
3.  Select the target account from the list.
4.  Enter the amount to deposit.
5.  Click confirm. The balance will update instantly in the main panel.

---

## 4. Withdrawals (Retraits)

Use this menu for cash withdrawals performed at the desk.

1.  Select the client in the sidebar.
2.  Click **Retrait** in the top navigation bar.
3.  Select the source account.
4.  Enter the amount to withdraw.
5.  **Validation**:
    * If the balance is sufficient, the transaction is processed and a success message appears.
    * If the withdrawal exceeds the authorized limit, an "Insuffisant" error message will appear.

---

## 5. Modifying Client Information

To keep the database up to date (change of phone number, address, etc.):

1.  Select the client in the sidebar.
2.  Click **Modifier infos** in the top navigation bar.
3.  A popup window will appear with the current data.
4.  Edit the necessary fields (First name, Last name, Email, Phone, or Address).
5.  Click **Save** to apply changes.

> **Tip**: To onboard an entirely new client, use the **Créer un client** button located at the bottom of the left sidebar.

---

## Summary of Business Rules

| Action | Constraint |
| :--- | :--- |
| **Withdrawal** | Limited by the maximum authorized overdraft. |
| **Account Closure** | Balance must be exactly 0.00 €. |
| **New Account** | Opens with a 0.00 € balance by default. |
| **Transfer** | Requires a valid Source and Target ID. |

---