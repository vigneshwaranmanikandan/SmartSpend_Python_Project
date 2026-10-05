from datetime import datetime
from file_manager import FileManager


class ExpenseManager:
    def __init__(self):
        self.expenses = FileManager.load_expenses()
        self.undo_stack = []
        self._next_id = self._calculate_next_id()

    def _calculate_next_id(self):
        if not self.expenses:
            return 1
        return max(e["id"] for e in self.expenses) + 1

    def _validate_date(self, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

    def add_expense(self, date, category, description, amount):
        self._validate_date(date)

        if not category:
            raise ValueError("Category cannot be empty.")
        if not description:
            raise ValueError("Description cannot be empty.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        expense = {
            "id": self._next_id,
            "date": date,
            "category": category.title(),
            "description": description,
            "amount": round(amount, 2)
        }

        self.expenses.append(expense)
        self.undo_stack.append(("delete", expense.copy()))
        self._next_id += 1
        self._save()

    def update_expense(self, expense_id, date=None, category=None,
                       description=None, amount=None):
        expense = self._find(expense_id)
        old = expense.copy()

        if date:
            self._validate_date(date)
            expense["date"] = date
        if category:
            expense["category"] = category.title()
        if description:
            expense["description"] = description
        if amount is not None:
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            expense["amount"] = round(amount, 2)

        self.undo_stack.append(("restore", old))
        self._save()

    def delete_expense(self, expense_id):
        expense = self._find(expense_id)
        self.expenses.remove(expense)
        self.undo_stack.append(("add", expense.copy()))
        self._save()

    def search_expenses(self, keyword):
        keyword = keyword.lower()
        return [
            e for e in self.expenses
            if keyword in e["category"].lower()
            or keyword in e["description"].lower()
        ]

    def get_expenses(self):
        return sorted(
            self.expenses,
            key=lambda x: (x["date"], x["id"])
        )

    def _find(self, expense_id):
        for expense in self.expenses:
            if expense["id"] == expense_id:
                return expense
        raise KeyError(f"Expense ID {expense_id} not found.")

    def undo_last_action(self):
        if not self.undo_stack:
            return False

        action, expense = self.undo_stack.pop()

        if action == "delete":
            self.expenses = [
                e for e in self.expenses if e["id"] != expense["id"]
            ]
        elif action == "add":
            self.expenses.append(expense)
        elif action == "restore":
            current = self._find(expense["id"])
            current.update(expense)

        self._save()
        return True

    def _save(self):
        FileManager.save_expenses(self.expenses)
