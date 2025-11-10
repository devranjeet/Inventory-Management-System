"""Suppliers View"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.supplier import SupplierManager

class SuppliersView:
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.supplier_manager = SupplierManager(db)
        ttk.Label(parent, text="Supplier Management", font=('Helvetica', 18, 'bold')).pack(pady=20)
        self.tree = ttk.Treeview(parent, columns=('Name', 'Contact', 'Phone', 'Outstanding'), show='headings', height=15)
        self.tree.heading('Name', text='Supplier Name')
        self.tree.heading('Contact', text='Contact Person')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Outstanding', text='Outstanding Payment')
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)
        ttk.Button(parent, text="Refresh", command=self.load_suppliers).pack(pady=10)
        self.load_suppliers()
    
    def load_suppliers(self):
        self.tree.delete(*self.tree.get_children())
        suppliers = self.supplier_manager.get_all_suppliers()
        for sup in suppliers:
            self.tree.insert('', 'end', values=(sup['supplier_name'], sup['contact_person'] or 'N/A', 
                                               sup['phone'] or 'N/A', f"₹{sup['outstanding_payment']:.2f}"))
