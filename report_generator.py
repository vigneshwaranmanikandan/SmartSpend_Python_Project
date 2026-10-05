import os
from datetime import datetime


class ReportGenerator:
    REPORT_DIR = "reports"

    @staticmethod
    def ensure_reports_folder():
        os.makedirs(ReportGenerator.REPORT_DIR, exist_ok=True)

    @staticmethod
    def generate_monthly_report(month, expenses, analyzer):
        ReportGenerator.ensure_reports_folder()

        month_expenses = analyzer.month_expenses(month)
        total = analyzer.total_for_month(month)
        summary = analyzer.category_summary(month)
        unusual = analyzer.detect_unusual_expenses(month)

        filename = os.path.join(
            ReportGenerator.REPORT_DIR,
            f"monthly_report_{month}.txt"
        )

        with open(filename, "w", encoding="utf-8") as file:
            file.write("=" * 60 + "\n")
            file.write("             SMARTSPEND MONTHLY REPORT\n")
            file.write("=" * 60 + "\n")
            file.write(f"Month: {month}\n")
            file.write(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            )

            file.write(f"Total Spending: ₹{total:.2f}\n")
            file.write(f"Number of Transactions: {len(month_expenses)}\n\n")

            file.write("CATEGORY BREAKDOWN\n")
            file.write("-" * 40 + "\n")

            for category, amount in summary.items():
                percentage = (amount / total * 100) if total else 0
                file.write(
                    f"{category:<20} ₹{amount:>10.2f} "
                    f"({percentage:.1f}%)\n"
                )

            file.write("\nUNUSUAL EXPENSES\n")
            file.write("-" * 40 + "\n")

            if unusual:
                for item in unusual:
                    file.write(
                        f"#{item['id']} | {item['category']} | "
                        f"₹{item['amount']:.2f} | {item['reason']}\n"
                    )
            else:
                file.write("No unusual expenses detected.\n")

            file.write("\nSMART INSIGHTS\n")
            file.write("-" * 40 + "\n")

            insights = analyzer.recommendations(month)
            for insight in insights:
                file.write(f"- {insight}\n")

        return filename
