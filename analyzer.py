from statistics import mean

try:
    import winsound
except ImportError:
    winsound = None


class ExpenseAnalyzer:
    def __init__(self, expense_manager):
        self.manager = expense_manager

    def month_expenses(self, month):
        return [
            e for e in self.manager.get_expenses()
            if e["date"].startswith(month)
        ]

    def total_for_month(self, month):
        return sum(e["amount"] for e in self.month_expenses(month))

    def category_summary(self, month):
        result = {}

        for expense in self.month_expenses(month):
            category = expense["category"]
            result[category] = result.get(category, 0) + expense["amount"]

        return dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True)
        )

    def highest_category(self, month):
        summary = self.category_summary(month)

        if not summary:
            return ("None", 0)

        return next(iter(summary.items()))

    def play_warning_sound(self):
        if winsound:
            for i in range(3):
                winsound.Beep(1000, 300)
                winsound.Beep(1300, 300)

    def detect_unusual_expenses(self, month):
        expenses = self.month_expenses(month)

        if len(expenses) < 3:
            return []

        amounts = [e["amount"] for e in expenses]
        average = mean(amounts)

        threshold = average * 2.5

        results = []

        for expense in expenses:

            if expense["amount"] > threshold:

                # Play alert sound
                self.play_warning_sound()

                results.append({
                    "id": expense["id"],
                    "category": expense["category"],
                    "amount": expense["amount"],
                    "reason": (
                        f"{expense['amount'] / average:.1f}x "
                        f"the monthly average"
                    )
                })

        return results

    def projected_monthly_spending(self, month):
        expenses = self.month_expenses(month)

        if not expenses:
            return 0

        days = max(int(expenses[-1]["date"][-2:]), 1)
        total = self.total_for_month(month)

        return (total / days) * 30

    def recommendations(self, month, budget=None):
        expenses = self.month_expenses(month)

        if not expenses:
            return []

        insights = []
        total = self.total_for_month(month)
        summary = self.category_summary(month)

        highest = self.highest_category(month)

        if highest[1] > total * 0.40:
            insights.append(
                f"{highest[0]} accounts for more than 40% of your "
                f"spending (₹{highest[1]:.2f})."
            )

        projected = self.projected_monthly_spending(month)

        if budget:
            if projected > budget:
                insights.append(
                    f"At your current spending rate, projected monthly "
                    f"spending is ₹{projected:.2f}, which is "
                    f"₹{projected - budget:.2f} above your budget."
                )

            elif projected > budget * 0.80:
                insights.append(
                    f"Your projected spending is ₹{projected:.2f}. "
                    f"Consider reducing discretionary expenses."
                )

        unusual = self.detect_unusual_expenses(month)

        if unusual:
            insights.append(
                f"{len(unusual)} unusual expense(s) detected. "
                f"Review them to ensure they were intentional."
            )

        if not insights:
            insights.append(
                "Your current spending pattern looks reasonable. "
                "Continue monitoring your budget."
            )

        return insights
