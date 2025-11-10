"""Purchases View"""
import tkinter as tk
from tkinter import ttk, messagebox

class PurchasesView:
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        ttk.Label(parent, text="Purchases Management", font=('Helvetica', 18, 'bold')).pack(pady=20)
        ttk.Label(parent, text="This view provides purchases management functionality", font=('Helvetica', 12)).pack(pady=20)
