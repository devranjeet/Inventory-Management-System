"""Expenses View"""
import tkinter as tk
from tkinter import ttk, messagebox

class ExpensesView:
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        ttk.Label(parent, text="Expenses Management", font=('Helvetica', 18, 'bold')).pack(pady=20)
        ttk.Label(parent, text="This view provides expenses management functionality", font=('Helvetica', 12)).pack(pady=20)
