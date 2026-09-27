import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'expenses.db')

class ExpenseModel:
    def __init__(self):
        """Connect to the database and ensure its tables exist."""
        try:
            self.conn = sqlite3.connect(DB_FILE)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")
            raise
        self.create_tables_if_not_exist()

    def create_tables_if_not_exist(self):
        """Create the expense and category tables when needed."""
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                    id INTEGER PRIMARY KEY,
                                    amount REAL,
                                    category TEXT,
                                    date TEXT,
                                    description TEXT)''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT UNIQUE)''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            raise

    def add_expense(self, amount, category, date, description):
        """Insert an expense into the database."""
        try:
            self.cursor.execute(
                'INSERT INTO expenses (amount, category, date, description) '
                'VALUES (?, ?, ?, ?)',
                (amount, category, date, description),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding expense: {e}")
            raise

    def get_expenses(self):
        """Return expense details without their database IDs."""
        try:
            self.cursor.execute('SELECT amount, category, date, description FROM expenses')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching expenses: {e}")
            raise
        
    def get_expenses_charts(self):
        """Return full expense rows for chart generation."""
        try:
            self.cursor.execute('SELECT * FROM expenses')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching expenses: {e}")
            raise

    def add_category(self, category):
        """Insert a category unless it already exists."""
        try:
            self.cursor.execute('INSERT INTO categories (name) VALUES (?)', (category,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Category '{category}' already exists.")
        except sqlite3.Error as e:
            print(f"Error adding category: {e}")
            raise

    def remove_category(self, category):
        """Delete a category by name."""
        try:
            self.cursor.execute('DELETE FROM categories WHERE name=?', (category,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error removing category: {e}")
            raise

    def get_categories(self):
        """Return the names of all saved categories."""
        try:
            self.cursor.execute('SELECT name FROM categories')
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error fetching categories: {e}")
            raise

    def export_to_csv(self, file_path):
        """Export all expenses to a CSV file."""
        try:
            self.cursor.execute('SELECT * FROM expenses')
            rows = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error exporting to CSV: {e}")
            raise

        df = pd.DataFrame(rows, columns=['id', 'amount', 'category', 'date', 'description'])
        df.to_csv(file_path, index=False)
        print(f"Data exported to {file_path} successfully.")

    def export_to_pdf(self, file_path):
        """Export all expenses to a PDF table."""
        try:
            self.cursor.execute('SELECT * FROM expenses')
            rows = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error exporting to PDF: {e}")
            raise

        df = pd.DataFrame(rows, columns=['id', 'amount', 'category', 'date', 'description'])
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)
        ax.axis('off')
        ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

        with matplotlib.backends.backend_pdf.PdfPages(file_path) as pdf:
            pdf.savefig(fig)
        print(f"Data exported to {file_path} successfully.")

    def export_to_sqlite(self, file_path):
        """Copy expense rows into a separate SQLite database."""
        conn_export = None
        try:
            conn_export = sqlite3.connect(file_path)
            cursor_export = conn_export.cursor()
            
            self.cursor.execute('SELECT amount, category, date, description FROM expenses')
            rows = self.cursor.fetchall()

            cursor_export.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                    id INTEGER PRIMARY KEY,
                                    amount REAL,
                                    category TEXT,
                                    date TEXT,
                                    description TEXT)''')

            cursor_export.executemany(
                'INSERT INTO expenses (amount, category, date, description) '
                'VALUES (?, ?, ?, ?)',
                rows,
            )
            conn_export.commit()
        except sqlite3.Error as e:
            print(f"Error exporting to SQLite: {e}")
            raise
        finally:
            if conn_export is not None:
                conn_export.close()
        print(f"Data exported to {file_path} successfully.")

    def close_connection(self):
        """Close the database connection."""
        try:
            self.conn.close()
            print("Database connection closed.")
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")
            raise
