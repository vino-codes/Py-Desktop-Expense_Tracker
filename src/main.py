# src/main.py
import tkinter as tk
from gui import ExpenseTrackerView
from controller import ExpenseTrackerController


def main():
    """Create the application window and start its event loop."""
    root = tk.Tk()
    controller = ExpenseTrackerController()
    app = ExpenseTrackerView(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()