import os
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DATA_FILE = "expenses.csv"
CATEGORIES = [
    "Food", "Transport", "Utilities", "Entertainment",
    "Shopping", "Health", "Education", "Other"
]


class ExpenseTracker:
    """Manage expense records stored in a CSV file."""

    def __init__(self, file_name=DATA_FILE):
        self.file_name = file_name
        self.data = pd.DataFrame(
            columns=["Date", "Amount", "Category", "Description"]
        )
        self.load_data()

    def load_data(self):
        """Load saved expenses and clean basic invalid rows."""
        if os.path.exists(self.file_name):
            try:
                self.data = pd.read_csv(self.file_name)
                required = ["Date", "Amount", "Category", "Description"]

                for column in required:
                    if column not in self.data.columns:
                        self.data[column] = ""

                self.data = self.data[required]
                self.data["Date"] = pd.to_datetime(
                    self.data["Date"], errors="coerce"
                )
                self.data["Amount"] = pd.to_numeric(
                    self.data["Amount"], errors="coerce"
                )
                self.data = self.data.dropna(
                    subset=["Date", "Amount", "Category"]
                )
                self.data = self.data[self.data["Amount"] > 0]
                self.data["Date"] = self.data["Date"].dt.strftime("%Y-%m-%d")
                self.data["Category"] = self.data["Category"].astype(str)
                self.data["Description"] = (
                    self.data["Description"].fillna("").astype(str)
                )
            except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError) as error:
                print("Could not load the dataset:", error)
                self.data = pd.DataFrame(
                    columns=["Date", "Amount", "Category", "Description"]
                )
        else:
            self.save_data()

    def save_data(self):
        """Save all current records to the CSV dataset."""
        self.data.to_csv(self.file_name, index=False)

    def add_expense(self, date, amount, category, description):
        """Validate and add one expense."""
        try:
            valid_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format.")
            return False

        try:
            amount = float(amount)
        except (ValueError, TypeError):
            print("Amount must be a number.")
            return False

        if amount <= 0:
            print("Amount must be greater than zero.")
            return False

        category = category.strip().title()
        if category not in CATEGORIES:
            print("Invalid category. Choose one from:", ", ".join(CATEGORIES))
            return False

        description = description.strip()
        new_row = pd.DataFrame([{
            "Date": valid_date.strftime("%Y-%m-%d"),
            "Amount": amount,
            "Category": category,
            "Description": description
        }])

        self.data = pd.concat([self.data, new_row], ignore_index=True)
        self.save_data()
        print("Expense added successfully.")
        return True

    def get_summary(self):
        """Show total, average, and category-wise expenses using NumPy/Pandas."""
        if self.data.empty:
            print("No expense records available.")
            return None

        amounts = self.data["Amount"].to_numpy(dtype=float)
        total = np.sum(amounts)
        average = np.mean(amounts)
        category_totals = self.data.groupby("Category")["Amount"].sum().sort_values(
            ascending=False
        )

        print("\n--- Expense Summary ---")
        print(f"Number of expenses : {len(amounts)}")
        print(f"Total expenses     : Rs. {total:.2f}")
        print(f"Average expense    : Rs. {average:.2f}")
        print("\nCategory-wise totals:")
        print(category_totals.to_string())

        percentages = (category_totals / total) * 100 if total else category_totals
        print("\nSpending percentage by category:")
        for category, percentage in percentages.items():
            print(f"{category:<18} {percentage:.2f}%")

        date_values = pd.to_datetime(self.data["Date"], errors="coerce")
        monthly = self.data.assign(Month=date_values.dt.to_period("M")).groupby(
            "Month"
        )["Amount"].mean()
        if not monthly.empty:
            print("\nMonthly average spending:")
            print(monthly.to_string())

        print("\nHighest spending category:", category_totals.idxmax())
        print("Highest expense amount : Rs. {:.2f}".format(self.data["Amount"].max()))

        return {
            "total": float(total),
            "average": float(average),
            "category_totals": category_totals
        }

    def filter_expenses(self, condition=None):
        """Filter by category, date range, or amount range."""
        if self.data.empty:
            print("No expense records available.")
            return self.data.copy()

        print("\nFilter Expenses")
        print("1. By category")
        print("2. By date range")
        print("3. By amount range")
        print("4. Show all expenses")
        choice = input("Choose filter: ").strip()

        filtered = self.data.copy()

        if choice == "1":
            category = input("Enter category: ").strip().title()
            filtered = filtered[filtered["Category"].str.lower() == category.lower()]
        elif choice == "2":
            start_date = input("Start date (YYYY-MM-DD): ").strip()
            end_date = input("End date (YYYY-MM-DD): ").strip()
            try:
                start = pd.to_datetime(start_date, format="%Y-%m-%d")
                end = pd.to_datetime(end_date, format="%Y-%m-%d")
                if start > end:
                    print("Start date cannot be after end date.")
                    return self.data.iloc[0:0]
                dates = pd.to_datetime(filtered["Date"], errors="coerce")
                filtered = filtered[(dates >= start) & (dates <= end)]
            except ValueError:
                print("Invalid date format.")
                return self.data.iloc[0:0]
        elif choice == "3":
            try:
                minimum = float(input("Minimum amount: "))
                maximum = float(input("Maximum amount: "))
                if minimum < 0 or maximum < minimum:
                    print("Enter a valid amount range.")
                    return self.data.iloc[0:0]
                filtered = filtered[
                    (filtered["Amount"] >= minimum)
                    & (filtered["Amount"] <= maximum)
                ]
            except ValueError:
                print("Please enter numeric amounts.")
                return self.data.iloc[0:0]
        elif choice != "4":
            print("Invalid filter choice.")
            return self.data.iloc[0:0]

        if filtered.empty:
            print("No matching expenses found.")
        else:
            print("\nFiltered Expenses:")
            print(filtered.to_string(index=False))
            print("Filtered total: Rs. {:.2f}".format(filtered["Amount"].sum()))

        return filtered

    def generate_report(self):
        """Print key metrics and a short report."""
        summary = self.get_summary()
        if summary is None:
            return

        print("\n--- Expense Report ---")
        print("Dataset file       :", self.file_name)
        print("Records available  :", len(self.data))
        print("Total spending     : Rs. {:.2f}".format(summary["total"]))
        print("Average spending   : Rs. {:.2f}".format(summary["average"]))
        print("Categories used    :", self.data["Category"].nunique())
        print("First expense date :", self.data["Date"].min())
        print("Last expense date  :", self.data["Date"].max())

    def show_expenses(self):
        """Display all saved expense records."""
        if self.data.empty:
            print("No expense records available.")
        else:
            print("\n--- All Expenses ---")
            print(self.data.to_string(index=False))

    def visualize_data(self):
        """Create bar, line, pie, and histogram visualizations."""
        if self.data.empty:
            print("No data to visualize. Add expenses first.")
            return

        sns.set_theme(style="whitegrid")
        data = self.data.copy()
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
        category_totals = data.groupby("Category")["Amount"].sum().sort_values(
            ascending=False
        )
        monthly_totals = data.groupby(data["Date"].dt.to_period("M"))["Amount"].sum()

        # Bar chart: total expenses by category
        plt.figure(figsize=(9, 5))
        sns.barplot(x=category_totals.index, y=category_totals.values)
        plt.title("Total Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount (Rs.)")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.show()

        # Line graph: spending trends over time
        plt.figure(figsize=(9, 5))
        if not monthly_totals.empty:
            x_values = monthly_totals.index.astype(str)
            plt.plot(x_values, monthly_totals.values, marker="o")
        plt.title("Monthly Spending Trend")
        plt.xlabel("Month")
        plt.ylabel("Total Amount (Rs.)")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.show()

        # Pie chart: proportional spending distribution
        plt.figure(figsize=(7, 7))
        plt.pie(
            category_totals.values,
            labels=category_totals.index,
            autopct="%1.1f%%",
            startangle=90
        )
        plt.title("Spending Distribution by Category")
        plt.tight_layout()
        plt.show()

        # Histogram: frequency of expense amounts
        plt.figure(figsize=(9, 5))
        sns.histplot(data=data, x="Amount", bins=8, kde=True)
        plt.title("Frequency of Expense Amounts")
        plt.xlabel("Expense Amount (Rs.)")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n========== SMART EXPENSE TRACKER ==========")
        print("1. Add Expense")
        print("2. Show All Expenses")
        print("3. Expense Summary and Analysis")
        print("4. Filter Expenses")
        print("5. Generate Report")
        print("6. Show Charts")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            date = input("Date (YYYY-MM-DD): ").strip()
            amount = input("Amount: ").strip()
            print("Categories:", ", ".join(CATEGORIES))
            category = input("Category: ").strip()
            description = input("Description: ").strip()
            tracker.add_expense(date, amount, category, description)
        elif choice == "2":
            tracker.show_expenses()
        elif choice == "3":
            tracker.get_summary()
        elif choice == "4":
            tracker.filter_expenses()
        elif choice == "5":
            tracker.generate_report()
        elif choice == "6":
            tracker.visualize_data()
        elif choice == "7":
            print("Thank you for using Smart Expense Tracker.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
