from file_manager import FileManager


class BudgetManager:
    def __init__(self):
        self.budgets = FileManager.load_budgets()

    def set_budget(self, month, amount):
        if len(month) != 7 or month[4] != "-":
            raise ValueError("Month must be in YYYY-MM format.")

        if amount <= 0:
            raise ValueError("Budget must be greater than zero.")

        self.budgets[month] = round(amount, 2)
        FileManager.save_budgets(self.budgets)

    def get_budget(self, month):
        return self.budgets.get(month)
