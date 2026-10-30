# Bank Management System

A simple command-line banking application for creating and managing customer bank accounts.

## Features

- Create a new account
- Deposit money
- Withdraw money
- View account details
- Update account information
- Delete an account
- Data is stored in JSON format for easy persistence

## Project files

- `bank_app.py` — main application logic and menu-driven interface
- `datafile.json` — JSON database storing account records
- `main.py` — older prototype script for the same banking concept

## How to run

From the project folder, run:

```bash
python bank_app.py
```

If you want to use the older script instead:

```bash
python main.py
```

## Account data

Each account record stores the following information:

- name
- age
- email
- pin
- accountno
- balance

## Notes

- A valid account is identified by its account number and PIN.
- The application enforces a minimum age of 18.
- PINs must be exactly four digits.
- Deposits are limited to a maximum of 10,000 per transaction.

## Example workflow

1. Run the app.
2. Choose option `1` to create an account.
3. Use the generated account number and PIN for future actions.
4. Deposit, withdraw, update, or delete the account as needed.
