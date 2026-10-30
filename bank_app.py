import json
import secrets
import string
import tempfile
from pathlib import Path
from typing import Any


DATA_FILE = Path(__file__).with_name("datafile.json")
MAX_DEPOSIT = 10_000


class BankStorage:
    def __init__(self, path: Path = DATA_FILE) -> None:
        self.path = path

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        with self.path.open(encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError("The bank data file must contain a JSON list.")

        required_fields = {"name", "age", "email", "pin", "accountno", "balance"}
        for index, record in enumerate(records, start=1):
            if not isinstance(record, dict) or not required_fields.issubset(record):
                raise ValueError(f"Account record {index} is missing required fields.")
            if not isinstance(record["balance"], (int, float)) or record["balance"] < 0:
                raise ValueError(f"Account record {index} has an invalid balance.")
            record["accountno"] = str(record["accountno"])

        return records

    def save(self, records: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                delete=False,
            ) as file:
                temporary_path = Path(file.name)
                json.dump(records, file, indent=2)
                file.write("\n")
            temporary_path.replace(self.path)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()


class BankApp:
    def __init__(self, storage: BankStorage) -> None:
        self.storage = storage
        self.accounts = storage.load()

    @staticmethod
    def _read_integer(prompt: str, minimum: int | None = None) -> int:
        while True:
            try:
                value = int(input(prompt).strip())
            except ValueError:
                print("Please enter a whole number.")
                continue
            if minimum is not None and value < minimum:
                print(f"Please enter a number of at least {minimum}.")
                continue
            return value

    @staticmethod
    def _read_pin(prompt: str = "Enter a four-digit PIN: ") -> str:
        while True:
            pin = input(prompt).strip()
            if len(pin) == 4 and pin.isdigit():
                return pin
            print("PIN must contain exactly four digits.")

    @staticmethod
    def _new_account_number(existing: set[str]) -> str:
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        while True:
            account_number = "".join(secrets.choice(alphabet) for _ in range(7))
            if account_number not in existing:
                return account_number

    def _authenticate(self) -> dict[str, Any] | None:
        account_number = input("Account number: ").strip()
        pin = input("PIN: ").strip()
        account = next(
            (
                item
                for item in self.accounts
                if item["accountno"] == account_number
                and str(item["pin"]) == pin
            ),
            None,
        )
        if account is None:
            print("No account found with those credentials.")
        return account

    def _save_accounts(self, updated_accounts: list[dict[str, Any]]) -> None:
        self.storage.save(updated_accounts)
        self.accounts = updated_accounts

    def create_account(self) -> None:
        name = input("Name: ").strip()
        while not name:
            print("Name cannot be blank.")
            name = input("Name: ").strip()

        age = self._read_integer("Age: ", minimum=0)
        if age < 18:
            print("You must be at least 18 to open an account.")
            return

        email = input("Email: ").strip()
        while not email or "@" not in email:
            print("Please enter a valid email address.")
            email = input("Email: ").strip()
        pin = self._read_pin()

        account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountno": self._new_account_number(
                {item["accountno"] for item in self.accounts}
            ),
            "balance": 0,
        }
        self._save_accounts([*self.accounts, account])
        print(f"Account opened successfully. Account number: {account['accountno']}")
        print("Keep your account number safe.")

    def deposit(self) -> None:
        account = self._authenticate()
        if account is None:
            return

        amount = self._read_integer(
            f"Deposit amount (1-{MAX_DEPOSIT}): ", minimum=1
        )
        if amount > MAX_DEPOSIT:
            print(f"Deposits must not exceed {MAX_DEPOSIT:,}.")
            return

        updated_account = {**account, "balance": account["balance"] + amount}
        updated_accounts = [
            updated_account if item is account else item for item in self.accounts
        ]
        self._save_accounts(updated_accounts)
        print(f"Deposited {amount:,}. New balance: {updated_account['balance']:,}.")

    def withdraw(self) -> None:
        account = self._authenticate()
        if account is None:
            return

        amount = self._read_integer("Withdrawal amount: ", minimum=1)
        if amount > account["balance"]:
            print("Insufficient balance.")
            return

        updated_account = {**account, "balance": account["balance"] - amount}
        updated_accounts = [
            updated_account if item is account else item for item in self.accounts
        ]
        self._save_accounts(updated_accounts)
        print(f"Withdrew {amount:,}. New balance: {updated_account['balance']:,}.")

    def show_details(self) -> None:
        account = self._authenticate()
        if account is None:
            return

        print("Account details:")
        for key, value in account.items():
            if key != "pin":
                print(f"{key}: {value}")

    def update_details(self) -> None:
        account = self._authenticate()
        if account is None:
            return

        print("Leave a field blank to keep its current value.")
        name = input(f"Name [{account['name']}]: ").strip() or account["name"]
        email = input(f"Email [{account['email']}]: ").strip() or account["email"]
        while email != account["email"] and "@" not in email:
            print("Please enter a valid email address.")
            email = input("Email: ").strip() or account["email"]

        pin = input("New four-digit PIN (blank to keep current): ").strip()
        while pin and (len(pin) != 4 or not pin.isdigit()):
            print("PIN must contain exactly four digits.")
            pin = input("New four-digit PIN (blank to keep current): ").strip()

        updated_account = {**account, "name": name, "email": email}
        if pin:
            updated_account["pin"] = pin
        updated_accounts = [
            updated_account if item is account else item for item in self.accounts
        ]
        self._save_accounts(updated_accounts)
        print("Account details updated.")

    def delete_account(self) -> None:
        account = self._authenticate()
        if account is None:
            return

        confirmation = input("Delete this account? Enter Y to confirm: ").strip()
        if confirmation.lower() != "y":
            print("Account deletion cancelled.")
            return

        self._save_accounts([item for item in self.accounts if item is not account])
        print("Account deleted.")

    def run(self) -> None:
        actions = {
            "1": ("Create an account", self.create_account),
            "2": ("Deposit money", self.deposit),
            "3": ("Withdraw money", self.withdraw),
            "4": ("Show account details", self.show_details),
            "5": ("Update account details", self.update_details),
            "6": ("Delete an account", self.delete_account),
        }

        while True:
            print("\nBank Management")
            for choice, (label, _) in actions.items():
                print(f"{choice}. {label}")
            print("0. Exit")

            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye.")
                return
            action = actions.get(choice)
            if action is None:
                print("Please choose a listed option.")
                continue
            action[1]()


def main() -> int:
    try:
        BankApp(BankStorage()).run()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Unable to start or save the banking application: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
