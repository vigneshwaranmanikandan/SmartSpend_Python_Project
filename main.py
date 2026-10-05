from expense_manager import ExpenseManager
from budget_manager import BudgetManager
from analyzer import ExpenseAnalyzer
from report_generator import ReportGenerator


def print_menu():
    print("\n" + "=" * 55)
    print("             SMARTSPEND")
    print(" Personal Expense, Budget & Spending Analyzer")
    print("=" * 55)
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Update Expense")
    print("4. Delete Expense")
    print("5. Search Expenses")
    print("6. Set Monthly Budget")
    print("7. View Budget Status")
    print("8. Spending Analysis")
    print("9. Detect Unusual Expenses")
    print("10. Smart Recommendations")
    print("11. Undo Last Transaction")
    print("12. Generate Monthly Report")
    print("0. Exit")
    print("=" * 55)


def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError("Amount must be greater than zero.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")


def add_expense(manager):
    print("\n--- Add Expense ---")
    date = input("Date (YYYY-MM-DD): ").strip()
    category = input("Category: ").strip()
    description = input("Description: ").strip()
    amount = get_float("Amount: ₹")

    manager.add_expense(date, category, description, amount)
    print("✓ Expense added successfully.")


def update_expense(manager):
    print("\n--- Update Expense ---")
    try:
        expense_id = int(input("Expense ID: "))
        print("Leave a field blank to keep the existing value.")
        date = input("New date: ").strip()
        category = input("New category: ").strip()
        description = input("New description: ").strip()
        amount_text = input("New amount: ₹").strip()
        amount = float(amount_text) if amount_text else None

        manager.update_expense(
            expense_id, date or None, category or None,
            description or None, amount
        )
        print("✓ Expense updated.")
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")


def delete_expense(manager):
    print("\n--- Delete Expense ---")
    try:
        expense_id = int(input("Expense ID: "))
        manager.delete_expense(expense_id)
        print("✓ Expense deleted.")
    except (ValueError, KeyError) as e:
        print(f"Error: {e}")


def view_expenses(manager):
    expenses = manager.get_expenses()
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses found.")
        return

    print(f"{'ID':<5}{'Date':<13}{'Category':<15}{'Amount':>12}  Description")
    print("-" * 70)

    for e in expenses:
        print(
            f"{e['id']:<5}{e['date']:<13}"
            f"{e['category']:<15}₹{e['amount']:>10.2f}  "
            f"{e['description']}"
        )


def search_expenses(manager):
    keyword = input("\nSearch category/description: ").strip()
    results = manager.search_expenses(keyword)

    if not results:
        print("No matching expenses found.")
        return

    print(f"\nFound {len(results)} expense(s):")
    for e in results:
        print(
            f"#{e['id']} | {e['date']} | {e['category']} | "
            f"₹{e['amount']:.2f} | {e['description']}"
        )


def set_budget(budget_manager):
    try:
        month = input("Month (YYYY-MM): ").strip()
        amount = get_float("Monthly budget: ₹")
        budget_manager.set_budget(month, amount)
        print("✓ Budget saved.")
    except ValueError as e:
        print(f"Error: {e}")


def budget_status(manager, budget_manager, analyzer):
    month = input("Month (YYYY-MM): ").strip()
    budget = budget_manager.get_budget(month)

    if budget is None:
        print("No budget set for this month.")
        return

    spent = analyzer.total_for_month(month)
    remaining = budget - spent
    percentage = (spent / budget) * 100

    print(f"\n--- Budget Status: {month} ---")
    print(f"Budget       : ₹{budget:.2f}")
    print(f"Spent        : ₹{spent:.2f}")
    print(f"Remaining    : ₹{remaining:.2f}")
    print(f"Used         : {percentage:.1f}%")

    if remaining < 0:
        print("⚠ Budget exceeded!")
    elif percentage >= 80:
        print("⚠ Warning: You have used more than 80% of your budget.")
    else:
        print("✓ You are within your budget.")


def spending_analysis(analyzer):
    month = input("Month (YYYY-MM): ").strip()
    summary = analyzer.category_summary(month)
    total = analyzer.total_for_month(month)

    print(f"\n--- Spending Analysis: {month} ---")
    print(f"Total Spending: ₹{total:.2f}")

    if not summary:
        print("No expenses found.")
        return

    print("\nCategory Breakdown:")
    for category, amount in summary.items():
        percentage = (amount / total) * 100 if total else 0
        print(f"{category:<20} ₹{amount:>10.2f}  ({percentage:.1f}%)")

    highest = analyzer.highest_category(month)
    print(f"\nHighest Spending Category: {highest[0]} (₹{highest[1]:.2f})")


def unusual_expenses(analyzer):
    month = input("Month (YYYY-MM): ").strip()
    results = analyzer.detect_unusual_expenses(month)

    print("\n--- Unusual Expense Detection ---")
    if not results:
        print("No unusual expenses detected.")
        return

    for item in results:
        print(
            f"⚠ Expense #{item['id']} | {item['category']} | "
            f"₹{item['amount']:.2f} | {item['reason']}"
        )


def recommendations(analyzer, budget_manager):
    month = input("Month (YYYY-MM): ").strip()
    budget = budget_manager.get_budget(month)
    insights = analyzer.recommendations(month, budget)

    print(f"\n--- Smart Insights: {month} ---")
    if not insights:
        print("Not enough data for recommendations.")
        return

    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")


def generate_report(manager, analyzer):
    month = input("Month (YYYY-MM): ").strip()
    path = ReportGenerator.generate_monthly_report(
        month,
        manager.get_expenses(),
        analyzer
    )
    print(f"✓ Report generated: {path}")


def main():
    manager = ExpenseManager()
    budget_manager = BudgetManager()
    analyzer = ExpenseAnalyzer(manager)
    ReportGenerator.ensure_reports_folder()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_expense(manager)
            elif choice == "2":
                view_expenses(manager)
            elif choice == "3":
                update_expense(manager)
            elif choice == "4":
                delete_expense(manager)
            elif choice == "5":
                search_expenses(manager)
            elif choice == "6":
                set_budget(budget_manager)
            elif choice == "7":
                budget_status(manager, budget_manager, analyzer)
            elif choice == "8":
                spending_analysis(analyzer)
            elif choice == "9":
                unusual_expenses(analyzer)
            elif choice == "10":
                recommendations(analyzer, budget_manager)
            elif choice == "11":
                if manager.undo_last_action():
                    print("✓ Last transaction undone.")
                else:
                    print("Nothing to undo.")
            elif choice == "12":
                generate_report(manager, analyzer)
            elif choice == "0":
                print("Thank you for using SmartSpend!")
                break
            else:
                print("Invalid choice. Please select from the menu.")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
