# PROGRAM SPECIFICATIONS:
# Good layout (GUI)
# Data persistence: File Handling (Binary file) w/ CRUD functionality
# Exception handling
# Collections
# KEY CONCEPT / PROGRAM BASIS: Expenses Tracker


from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import pickle
import tkinter as tk
from tkinter import ttk, messagebox


# ---------------------------
# 1) DATA MODEL (OOP)
# ---------------------------
@dataclass
class Expense:
    expense_id: int
    date_iso: str
    category: str
    description: str
    amount: float


# ---------------------------
# 2) REPOSITORY (FILE HANDLING)
# Binary persistence using pickle
# ---------------------------
class ExpenseRepository:
    def __init__(self, file_path="expenses.dat"):
        self.file_path = Path(file_path)

    def load_all(self):
        if not self.file_path.exists():
            return []
        try:
            with self.file_path.open("rb") as f:
                data = pickle.load(f)
                return data if isinstance(data, list) else []
        except EOFError:
            return []
        except (pickle.UnpicklingError, OSError) as err:
            raise RuntimeError(f"Could not read file: {err}")

    def save_all(self, expenses):
        try:
            with self.file_path.open("wb") as f:
                pickle.dump(expenses, f)
        except OSError as err:
            raise RuntimeError(f"Could not save file: {err}")


# ---------------------------
# 3) SERVICE (CRUD + VALIDATION)
# Business rules independent from GUI
# ---------------------------
class ExpenseService:
    def __init__(self, repository):
        self.repo = repository

    def create_expense(self, date_iso, category, description, amount_text):
        self._validate_date(date_iso)
        amount = self._validate_amount(amount_text)
        category = category.strip()
        description = description.strip()

        if not category or not description:
            raise ValueError("Category and description are required.")

        expenses = self.repo.load_all()
        new_id = 1 if not expenses else max(e.expense_id for e in expenses) + 1

        new_expense = Expense(
            expense_id=new_id,
            date_iso=date_iso,
            category=category,
            description=description,
            amount=amount,
        )
        expenses.append(new_expense)
        self.repo.save_all(expenses)
        return new_expense

    def read_expenses(self):
        return self.repo.load_all()

    def update_expense(self, expense_id_text, date_iso="", category="", description="", amount_text=""):
        expense_id = self._validate_id(expense_id_text)
        expenses = self.repo.load_all()

        for exp in expenses:
            if exp.expense_id == expense_id:
                if date_iso.strip():
                    self._validate_date(date_iso)
                    exp.date_iso = date_iso
                if category.strip():
                    exp.category = category.strip()
                if description.strip():
                    exp.description = description.strip()
                if amount_text.strip():
                    exp.amount = self._validate_amount(amount_text)

                self.repo.save_all(expenses)
                return exp

        raise ValueError("Expense ID not found.")

    def delete_expense(self, expense_id_text):
        expense_id = self._validate_id(expense_id_text)
        expenses = self.repo.load_all()

        for i, exp in enumerate(expenses):
            if exp.expense_id == expense_id:
                removed = expenses.pop(i)
                self.repo.save_all(expenses)
                return removed

        raise ValueError("Expense ID not found.")

    @staticmethod
    def _validate_amount(amount_text):
        try:
            amount = float(amount_text)
        except ValueError:
            raise ValueError("Amount must be numeric.")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        return amount

    @staticmethod
    def _validate_date(date_iso):
        try:
            datetime.strptime(date_iso, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be YYYY-MM-DD.")

    @staticmethod
    def _validate_id(expense_id_text):
        try:
            value = int(expense_id_text)
        except ValueError:
            raise ValueError("Expense ID must be a whole number.")
        if value <= 0:
            raise ValueError("Expense ID must be positive.")
        return value


# ---------------------------
# 4) GUI LAYER (TKINTER)
# Only calls service methods
# ---------------------------
class ExpenseTrackerGUI:
    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.root.title("Expense Tracker")
        self.root.geometry("850x500")

        self._build_form()
        self._build_table()
        self._build_buttons()
        self.refresh_table()

    def _build_form(self):
        form = ttk.Frame(self.root, padding=10)
        form.pack(fill="x")

        self.date_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.id_var = tk.StringVar()

        ttk.Label(form, text="ID").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form, textvariable=self.id_var, width=10).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(form, textvariable=self.date_var, width=15).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Category").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form, textvariable=self.category_var, width=20).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Description").grid(row=1, column=2, padx=5, pady=5)
        ttk.Entry(form, textvariable=self.desc_var, width=30).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form, text="Amount").grid(row=1, column=4, padx=5, pady=5)
        ttk.Entry(form, textvariable=self.amount_var, width=12).grid(row=1, column=5, padx=5, pady=5)

    def _build_table(self):
        table_frame = ttk.Frame(self.root, padding=10)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "date", "category", "description", "amount"),
            show="headings",
            height=12,
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.heading("amount", text="Amount")

        self.tree.column("id", width=60)
        self.tree.column("date", width=120)
        self.tree.column("category", width=130)
        self.tree.column("description", width=300)
        self.tree.column("amount", width=120)

        self.tree.pack(fill="both", expand=True)

    def _build_buttons(self):
        btns = ttk.Frame(self.root, padding=10)
        btns.pack(fill="x")

        ttk.Button(btns, text="Create", command=self.create_record).pack(side="left", padx=6)
        ttk.Button(btns, text="Read/Refresh", command=self.refresh_table).pack(side="left", padx=6)
        ttk.Button(btns, text="Update", command=self.update_record).pack(side="left", padx=6)
        ttk.Button(btns, text="Delete", command=self.delete_record).pack(side="left", padx=6)

    def create_record(self):
        try:
            self.service.create_expense(
                self.date_var.get(),
                self.category_var.get(),
                self.desc_var.get(),
                self.amount_var.get(),
            )
            self.refresh_table()
            messagebox.showinfo("Success", "Expense created.")
        except (ValueError, RuntimeError) as err:
            messagebox.showerror("Error", str(err))

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            for exp in self.service.read_expenses():
                self.tree.insert(
                    "",
                    "end",
                    values=(exp.expense_id, exp.date_iso, exp.category, exp.description, f"{exp.amount:.2f}")
                )
        except RuntimeError as err:
            messagebox.showerror("Error", str(err))

    def update_record(self):
        try:
            self.service.update_expense(
                self.id_var.get(),
                date_iso=self.date_var.get(),
                category=self.category_var.get(),
                description=self.desc_var.get(),
                amount_text=self.amount_var.get(),
            )
            self.refresh_table()
            messagebox.showinfo("Success", "Expense updated.")
        except (ValueError, RuntimeError) as err:
            messagebox.showerror("Error", str(err))

    def delete_record(self):
        try:
            self.service.delete_expense(self.id_var.get())
            self.refresh_table()
            messagebox.showinfo("Success", "Expense deleted.")
        except (ValueError, RuntimeError) as err:
            messagebox.showerror("Error", str(err))


# ---------------------------
# 5) APP ENTRY POINT
# ---------------------------
def main():
    repo = ExpenseRepository("expenses.dat")
    service = ExpenseService(repo)

    root = tk.Tk()
    ExpenseTrackerGUI(root, service)
    root.mainloop()


if __name__ == "__main__":
    main()