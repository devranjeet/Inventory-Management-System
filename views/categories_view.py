"""
Categories View - Manage product categories
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.category_model import CategoryModel


class CategoriesView:
    """View for managing categories"""
    
    def __init__(self, parent, auth_controller):
        self.parent = parent
        self.auth_controller = auth_controller
        self.model = CategoryModel()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_categories()
    
    def create_widgets(self):
        """Create categories view widgets"""
        # Title
        title_label = ttk.Label(self.frame, text="Categories", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Add Category", command=self.add_category).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Edit Category", command=self.edit_category).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Delete Category", command=self.delete_category).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Refresh", command=self.load_categories).pack(side=tk.LEFT)
        
        # Categories treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Description')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Category Name')
        self.tree.heading('Description', text='Description')
        
        self.tree.column('ID', width=80, anchor=tk.CENTER)
        self.tree.column('Name', width=200)
        self.tree.column('Description', width=400)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_category())
    
    def load_categories(self):
        """Load all categories"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        categories = self.model.get_all_categories()
        for category in categories:
            self.tree.insert('', tk.END, values=(
                category.get('category_id', ''),
                category.get('category_name', ''),
                category.get('description', '')
            ))
    
    def add_category(self):
        """Open dialog to add new category"""
        CategoryDialog(self.frame, self.model, callback=self.load_categories)
    
    def edit_category(self):
        """Open dialog to edit selected category"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a category to edit")
            return
        
        item = self.tree.item(selection[0])
        category_id = item['values'][0]
        category = self.model.get_category_by_id(category_id)
        
        if category:
            CategoryDialog(self.frame, self.model, category=category, callback=self.load_categories)
    
    def delete_category(self):
        """Delete selected category"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a category to delete")
            return
        
        item = self.tree.item(selection[0])
        category_id = item['values'][0]
        category_name = item['values'][1]
        
        # Check if category has products
        count = self.model.get_products_count(category_id)
        if count > 0:
            messagebox.showerror("Error", f"Cannot delete category. It has {count} products.")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{category_name}'?"):
            success = self.model.delete_category(category_id)
            if success:
                messagebox.showinfo("Success", "Category deleted successfully")
                self.load_categories()
            else:
                messagebox.showerror("Error", "Failed to delete category")
    
    def refresh(self):
        """Refresh categories list"""
        self.load_categories()


class CategoryDialog:
    """Dialog for adding/editing categories"""
    
    def __init__(self, parent, model, category=None, callback=None):
        self.model = model
        self.category = category
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Category" if category else "Add Category")
        self.dialog.geometry("450x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        if category:
            self.populate_fields()
    
    def create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Category name
        ttk.Label(main_frame, text="Category Name:*").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, pady=5)
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.description_text = tk.Text(main_frame, width=30, height=5)
        self.description_text.grid(row=1, column=1, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def populate_fields(self):
        """Populate fields with category data"""
        self.name_var.set(self.category.get('category_name', ''))
        self.description_text.insert('1.0', self.category.get('description', ''))
    
    def save(self):
        """Save category"""
        name = self.name_var.get().strip()
        description = self.description_text.get('1.0', tk.END).strip()
        
        if not name:
            messagebox.showerror("Error", "Category name is required")
            return
        
        if self.category:
            success = self.model.update_category(self.category['category_id'], name, description)
        else:
            success, _ = self.model.create_category(name, description)
        
        if success:
            messagebox.showinfo("Success", "Category saved successfully")
            self.dialog.destroy()
            if self.callback:
                self.callback()
        else:
            messagebox.showerror("Error", "Failed to save category")
