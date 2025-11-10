"""
Products View - Manage products with CRUD operations
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.product_controller import ProductController
from utils.helpers import format_currency, validate_positive_number, validate_positive_integer


class ProductsView:
    """View for managing products"""
    
    def __init__(self, parent, auth_controller):
        self.parent = parent
        self.auth_controller = auth_controller
        self.controller = ProductController()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        """Create products view widgets"""
        # Title and search frame
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(top_frame, text="Products", font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Search
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind('<KeyRelease>', lambda e: self.search_products())
        
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side=tk.LEFT)
        
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Add Product", command=self.add_product).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Edit Product", command=self.edit_product).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Delete Product", command=self.delete_product).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Refresh", command=self.load_products).pack(side=tk.LEFT)
        
        # Products treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Category', 'Supplier', 'Price', 'Stock', 'Reorder Level')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        # Configure columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Product Name')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Supplier', text='Supplier')
        self.tree.heading('Price', text='Unit Price')
        self.tree.heading('Stock', text='In Stock')
        self.tree.heading('Reorder Level', text='Reorder Level')
        
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Name', width=200)
        self.tree.column('Category', width=120)
        self.tree.column('Supplier', width=120)
        self.tree.column('Price', width=100, anchor=tk.E)
        self.tree.column('Stock', width=80, anchor=tk.CENTER)
        self.tree.column('Reorder Level', width=100, anchor=tk.CENTER)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        vsb.grid(row=0, column=1, sticky=tk.NS)
        hsb.grid(row=1, column=0, sticky=tk.EW)
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Double click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_product())
    
    def load_products(self):
        """Load all products"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        products = self.controller.get_all_products()
        
        for product in products:
            self.tree.insert('', tk.END, values=(
                product.get('product_id', ''),
                product.get('product_name', ''),
                product.get('category_name', 'N/A'),
                product.get('supplier_name', 'N/A'),
                format_currency(product.get('unit_price', 0)),
                product.get('quantity_in_stock', 0),
                product.get('reorder_level', 0)
            ), tags=(product.get('product_id'),))
    
    def search_products(self):
        """Search products by name"""
        search_term = self.search_var.get().strip()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not search_term:
            self.load_products()
            return
        
        products = self.controller.search_products(search_term)
        
        for product in products:
            self.tree.insert('', tk.END, values=(
                product.get('product_id', ''),
                product.get('product_name', ''),
                product.get('category_name', 'N/A'),
                product.get('supplier_name', 'N/A'),
                format_currency(product.get('unit_price', 0)),
                product.get('quantity_in_stock', 0),
                product.get('reorder_level', 0)
            ), tags=(product.get('product_id'),))
    
    def clear_search(self):
        """Clear search and reload all products"""
        self.search_var.set("")
        self.load_products()
    
    def add_product(self):
        """Open dialog to add new product"""
        ProductDialog(self.frame, self.controller, callback=self.load_products)
    
    def edit_product(self):
        """Open dialog to edit selected product"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product to edit")
            return
        
        item = self.tree.item(selection[0])
        product_id = item['values'][0]
        
        product = self.controller.get_product(product_id)
        if product:
            ProductDialog(self.frame, self.controller, product=product, callback=self.load_products)
    
    def delete_product(self):
        """Delete selected product"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        item = self.tree.item(selection[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            success, message = self.controller.delete_product(product_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_products()
            else:
                messagebox.showerror("Error", message)
    
    def refresh(self):
        """Refresh products list"""
        self.load_products()


class ProductDialog:
    """Dialog for adding/editing products"""
    
    def __init__(self, parent, controller, product=None, callback=None):
        self.controller = controller
        self.product = product
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Product" if product else "Add Product")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        if product:
            self.populate_fields()
    
    def create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Product name
        ttk.Label(main_frame, text="Product Name:*").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, pady=5)
        
        # Category
        ttk.Label(main_frame, text="Category:*").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        categories = self.controller.get_categories()
        category_values = [f"{c['category_id']} - {c['category_name']}" for c in categories]
        category_combo = ttk.Combobox(main_frame, textvariable=self.category_var, 
                                      values=category_values, width=37, state='readonly')
        category_combo.grid(row=1, column=1, pady=5)
        if category_values:
            category_combo.current(0)
        
        # Supplier
        ttk.Label(main_frame, text="Supplier:*").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.supplier_var = tk.StringVar()
        suppliers = self.controller.get_suppliers()
        supplier_values = [f"{s['supplier_id']} - {s['supplier_name']}" for s in suppliers]
        supplier_combo = ttk.Combobox(main_frame, textvariable=self.supplier_var,
                                      values=supplier_values, width=37, state='readonly')
        supplier_combo.grid(row=2, column=1, pady=5)
        if supplier_values:
            supplier_combo.current(0)
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=3, column=0, sticky=tk.NW, pady=5)
        self.description_text = tk.Text(main_frame, width=30, height=4)
        self.description_text.grid(row=3, column=1, pady=5)
        
        # Unit price
        ttk.Label(main_frame, text="Unit Price:*").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.price_var = tk.StringVar(value="0.00")
        ttk.Entry(main_frame, textvariable=self.price_var, width=40).grid(row=4, column=1, pady=5)
        
        # Quantity in stock
        ttk.Label(main_frame, text="Quantity in Stock:*").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="0")
        ttk.Entry(main_frame, textvariable=self.quantity_var, width=40).grid(row=5, column=1, pady=5)
        
        # Reorder level
        ttk.Label(main_frame, text="Reorder Level:*").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.reorder_var = tk.StringVar(value="10")
        ttk.Entry(main_frame, textvariable=self.reorder_var, width=40).grid(row=6, column=1, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Required fields note
        ttk.Label(main_frame, text="* Required fields", foreground='gray').grid(
            row=8, column=0, columnspan=2, pady=5
        )
    
    def populate_fields(self):
        """Populate fields with product data"""
        self.name_var.set(self.product.get('product_name', ''))
        
        # Set category
        category_id = self.product.get('category_id')
        if category_id:
            categories = self.controller.get_categories()
            for i, cat in enumerate(categories):
                if cat['category_id'] == category_id:
                    self.category_var.set(f"{cat['category_id']} - {cat['category_name']}")
                    break
        
        # Set supplier
        supplier_id = self.product.get('supplier_id')
        if supplier_id:
            suppliers = self.controller.get_suppliers()
            for i, sup in enumerate(suppliers):
                if sup['supplier_id'] == supplier_id:
                    self.supplier_var.set(f"{sup['supplier_id']} - {sup['supplier_name']}")
                    break
        
        self.description_text.insert('1.0', self.product.get('description', ''))
        self.price_var.set(str(self.product.get('unit_price', 0)))
        self.quantity_var.set(str(self.product.get('quantity_in_stock', 0)))
        self.reorder_var.set(str(self.product.get('reorder_level', 10)))
    
    def save(self):
        """Save product"""
        # Get values
        name = self.name_var.get().strip()
        category_str = self.category_var.get()
        supplier_str = self.supplier_var.get()
        description = self.description_text.get('1.0', tk.END).strip()
        
        # Validate required fields
        if not name:
            messagebox.showerror("Error", "Product name is required")
            return
        
        if not category_str:
            messagebox.showerror("Error", "Please select a category")
            return
        
        if not supplier_str:
            messagebox.showerror("Error", "Please select a supplier")
            return
        
        # Extract IDs from combo box values
        category_id = int(category_str.split(' - ')[0])
        supplier_id = int(supplier_str.split(' - ')[0])
        
        # Validate numbers
        valid, price = validate_positive_number(self.price_var.get(), "Unit price")
        if not valid:
            messagebox.showerror("Error", price)
            return
        
        valid, quantity = validate_positive_integer(self.quantity_var.get(), "Quantity")
        if not valid:
            messagebox.showerror("Error", quantity)
            return
        
        valid, reorder = validate_positive_integer(self.reorder_var.get(), "Reorder level")
        if not valid:
            messagebox.showerror("Error", reorder)
            return
        
        # Save product
        if self.product:
            # Update existing product
            success, message = self.controller.update_product(
                self.product['product_id'], name, category_id, supplier_id,
                description, price, quantity, reorder
            )
        else:
            # Create new product
            success, message = self.controller.create_product(
                name, category_id, supplier_id, description, price, quantity, reorder
            )
        
        if success:
            messagebox.showinfo("Success", "Product saved successfully")
            self.dialog.destroy()
            if self.callback:
                self.callback()
        else:
            messagebox.showerror("Error", message)
