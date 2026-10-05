import json
import os


DATA_DIR = "data"
EXPENSE_FILE = os.path.join(DATA_DIR, "expenses.json")
BUDGET_FILE = os.path.join(DATA_DIR, "budgets.json")


class FileManager:
    @staticmethod
    def _ensure_data_directory():
        os.makedirs(DATA_DIR, exist_ok=True)

    @staticmethod
    def load_expenses():
        FileManager._ensure_data_directory()

        if not os.path.exists(EXPENSE_FILE):
            return []

        try:
            with open(EXPENSE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def save_expenses(expenses):
        FileManager._ensure_data_directory()

        with open(EXPENSE_FILE, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)

    @staticmethod
    def load_budgets():
        FileManager._ensure_data_directory()

        if not os.path.exists(BUDGET_FILE):
            return {}

        try:
            with open(BUDGET_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    @staticmethod
    def save_budgets(budgets):
        FileManager._ensure_data_directory()

        with open(BUDGET_FILE, "w", encoding="utf-8") as file:
            json.dump(budgets, file, indent=4)
