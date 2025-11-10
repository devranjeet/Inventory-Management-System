"""
Categories View - Simplified
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.category import CategoryManager


class CategoriesView:
    def __init__(self, parent, db, current_user):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        self.category_manager = CategoryManager(db)
        
        ttk.Label(parent, text="Category Management", 
                 font=('Helvetica', 18, 'bold')).pack(pady=20)
        
        # Categories list
        self.tree = ttk.Treeview(parent, columns=('Name', 'Description', 'Products'), 
                                show='headings', height=15)
        self.tree.heading('Name', text='Category Name')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Products', text='Product Count')
        self.tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add Category", 
                  command=self.add_category).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", 
                  command=self.load_categories).pack(side='left', padx=5)
        
        self.load_categories()
    
    def load_categories(self):
        self.tree.delete(*self.tree.get_children())
        categories = self.category_manager.get_all_categories()
        for cat in categories:
            self.tree.insert('', 'end', values=(
                cat['category_name'],
                cat['description'] or 'N/A',
                cat['product_count']
            ))
    
    def add_category(self):
        messagebox.showinfo("Info", "Add category dialog")
