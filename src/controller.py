import sqlite3
from datetime import datetime

from data import ExpenseModel

class ExpenseTrackerController:
    def __init__(self):
        """Create the controller and its expense model."""
        self.model = ExpenseModel()
        
    def validate_date(self, date_str):
        """Validate a date and return it in ISO format."""
        if not date_str:
            return datetime.today().date().strftime("%Y-%m-%d")

        for date_format in ("%Y-%m-%d", "%m/%d/%Y"):
            try:
                parsed_date = datetime.strptime(date_str, date_format)
                return parsed_date.date().strftime("%Y-%m-%d")
            except ValueError:
                continue

        raise ValueError("Date format must be YYYY-MM-DD or MM/DD/YYYY.")

    def add_expense(self, amount, category, date_str, description):
        """Validate expense details and save the expense."""
        if not (amount and category and date_str):
            raise ValueError("Amount, category, and date are required.")

        amount = float(amount)
        expense_date = self.validate_date(date_str)
        self.model.add_expense(amount, category, expense_date, description)

    def get_expenses(self):
        """Return saved expenses, or an empty list after a database error."""
        try:
            return self.model.get_expenses()
        except sqlite3.Error:
            return []

    def get_expenses_charts(self):
        """Return expense rows used to build reports."""
        try:
            return self.model.get_expenses_charts()
        except sqlite3.Error:
            return []

    def get_categories(self):
        """Return saved categories, or an empty list after a database error."""
        try:
            return self.model.get_categories()
        except sqlite3.Error:
            return []

    def add_category(self, category):
        """Add a category, reporting expected database failures."""
        try:
            self.model.add_category(category)
        except sqlite3.Error:
            return

    def remove_category(self, category):
        """Remove a category, reporting expected database failures."""
        try:
            self.model.remove_category(category)
        except sqlite3.Error:
            return

    def load_expenses(self):
        """Return expenses for the view, or an empty list on database failure."""
        try:
            return self.model.get_expenses()
        except sqlite3.Error:
            return []

    def filter_expenses(
        self, category, start_date, end_date, min_amount, max_amount
    ):
        """Filter expenses by category, date range, and amount range."""
        try:
            expenses = self.model.get_expenses()

            if category and category != 'All':
                expenses = [expense for expense in expenses if expense[1] == category]

            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                expenses = [
                    expense for expense in expenses
                    if datetime.strptime(expense[2], '%Y-%m-%d') >= start_date
                ]

            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                expenses = [
                    expense for expense in expenses
                    if datetime.strptime(expense[2], '%Y-%m-%d') <= end_date
                ]

            if min_amount:
                expenses = [expense for expense in expenses
                            if expense[0] >= float(min_amount)]

            if max_amount:
                expenses = [expense for expense in expenses
                            if expense[0] <= float(max_amount)]

            return expenses
        except sqlite3.Error:
            return []

    def plot_expense_distribution(self):
        """Generate the expense distribution report."""
        try:
            return self.model.plot_expense_distribution()
        except sqlite3.Error:
            return None

    def plot_monthly_expenses(self):
        """Generate the monthly expenses report."""
        try:
            return self.model.plot_monthly_expenses()
        except sqlite3.Error:
            return None

    def export_to_csv(self, file_path):
        """Export expenses to a CSV file."""
        try:
            return self.model.export_to_csv(file_path)
        except sqlite3.Error:
            return None

    def export_to_pdf(self, file_path):
        """Export expenses to a PDF file."""
        try:
            return self.model.export_to_pdf(file_path)
        except sqlite3.Error:
            return None

    def export_to_sqlite(self, file_path):
        """Export expenses to another SQLite database."""
        try:
            return self.model.export_to_sqlite(file_path)
        except sqlite3.Error:
            return None
