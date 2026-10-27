## Project Overview
The Smart Expense Tracker is a Python application that records personal expenses, validates inputs, analyzes spending, filters records, and displays charts.

## Features
- Add expenses with date, amount, category, and description.
- Validate date format, positive amounts, and category names.
- Store data in `expenses.csv`.
- View all expenses.
- Calculate total and average expenses using NumPy.
- Analyze category totals, spending percentages, monthly average spending, and top spending category using Pandas.
- Filter records by category, date range, or amount range.
- Generate a summary report.
- Create a category bar chart, monthly line graph, pie chart, and amount histogram with Matplotlib and Seaborn.

## Requirements
- Python 3.10 or later
- NumPy
- Pandas
- Matplotlib
- Seaborn

## Installation
Open Command Prompt or PowerShell in the project folder and run:

```bash
python -m pip install numpy pandas matplotlib seaborn
```

## Run the Project
Keep `expense_tracker.py` and `expenses.csv` in the same folder, then run:

```bash
python expense_tracker.py
```

## Dataset
The `expenses.csv` file contains these columns:

- `Date` — date in `YYYY-MM-DD` format
- `Amount` — expense amount
- `Category` — expense category
- `Description` — short note about the expense

The program creates an empty CSV automatically if the dataset file is not present. It saves new expenses to the CSV file.

## Categories
Food, Transport, Utilities, Entertainment, Shopping, Health, Education, Other.

## Main Class Methods
- `add_expense(date, amount, category, description)` — validates and records an expense.
- `get_summary()` — calculates totals, average, category totals, percentages, and monthly averages.
- `filter_expenses(condition=None)` — offers category, date-range, and amount-range filtering.
- `generate_report()` — prints key report metrics.
- `visualize_data()` — displays four types of charts.

## Project Files
- `expense_tracker.py` — main Python program
- `expenses.csv` — sample expense dataset
- `README.md` — project setup and usage instructions
