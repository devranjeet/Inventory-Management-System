"""
Purchases View - Manage purchase transactions
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.purchase_controller import PurchaseController
from controllers.product_controller import ProductController
from utils.helpers import format_currency, validate_positive_number, validate_positive_integer


class PurchasesView:
    """View for managing purchases"""
    
    def __init__(self, parent, auth_controller):
        self.parent = parent
        self.auth_controller = auth_controller
        self.controller = PurchaseController()
        self.product_controller = ProductController()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_purchases()
    
    def create_widgets(self):
        """Create purchases view widgets"""
        # Title
        title_label = ttk.Label(self.frame, text="Purchases", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="New Purchase", command=self.add_purchase).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Refresh", command=self.load_purchases).pack(side=tk.LEFT)
        
        # Purchases treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Date', 'Product', 'Supplier', 'Quantity', 'Unit Cost', 'Total')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Product', text='Product')
        self.tree.heading('Supplier', text='Supplier')
        self.tree.heading('Quantity', text='Qty')
        self.tree.heading('Unit Cost', text='Unit Cost')
        self.tree.heading('Total', text='Total')
        
        self.tree.column('ID', width=60, anchor=tk.CENTER)
        self.tree.column('Date', width=150)
        self.tree.column('Product', width=200)
        self.tree.column('Supplier', width=150)
        self.tree.column('Quantity', width=80, anchor=tk.CENTER)
        self.tree.column('Unit Cost', width=100, anchor=tk.E)
        self.tree.column('Total', width=100, anchor=tk.E)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_purchases(self):
        """Load all purchases"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        purchases = self.controller.get_all_purchases()
        for purchase in purchases:
            purchase_date = purchase.get('purchase_date', '')
            if purchase_date:
                try:
                    date_obj = datetime.strptime(purchase_date, "%Y-%m-%d %H:%M:%S")
                    purchase_date = date_obj.strftime("%Y-%m-%d %I:%M %p")
                except:
                    pass
            
            self.tree.insert('', tk.END, values=(
                purchase.get('purchase_id', ''),
                purchase_date,
                purchase.get('product_name', 'N/A'),
                purchase.get('supplier_name', 'N/A'),
                purchase.get('quantity', 0),
                format_currency(purchase.get('unit_cost', 0)),
                format_currency(purchase.get('total_cost', 0))
            ))
    
    def add_purchase(self):
        """Open dialog to add new purchase"""
        PurchaseDialog(self.frame, self.controller, self.product_controller,
                      self.auth_controller, callback=self.load_purchases)
    
    def refresh(self):
        """Refresh purchases list"""
        self.load_purchases()


class PurchaseDialog:
    """Dialog for adding purchases"""
    
    def __init__(self, parent, controller, product_controller, auth_controller, callback=None):
        self.controller = controller
        self.product_controller = product_controller
        self.auth_controller = auth_controller
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Purchase")
        self.dialog.geometry("500x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Product
        ttk.Label(main_frame, text="Product:*").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.product_var = tk.StringVar()
        products = self.product_controller.get_all_products()
        product_values = [f"{p['product_id']} - {p['product_name']}" for p in products]
        self.product_combo = ttk.Combobox(main_frame, textvariable=self.product_var,
                                          values=product_values, width=45, state='readonly')
        self.product_combo.grid(row=0, column=1, pady=5)
        if product_values:
            self.product_combo.current(0)
        self.product_combo.bind('<<ComboboxSelected>>', self.on_product_selected)
        
        # Supplier
        ttk.Label(main_frame, text="Supplier:*").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.supplier_var = tk.StringVar()
        suppliers = self.product_controller.get_suppliers()
        supplier_values = [f"{s['supplier_id']} - {s['supplier_name']}" for s in suppliers]
        self.supplier_combo = ttk.Combobox(main_frame, textvariable=self.supplier_var,
                                           values=supplier_values, width=45, state='readonly')
        self.supplier_combo.grid(row=1, column=1, pady=5)
        if supplier_values:
            self.supplier_combo.current(0)
        
        # Quantity
        ttk.Label(main_frame, text="Quantity:*").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        ttk.Entry(main_frame, textvariable=self.quantity_var, width=47).grid(row=2, column=1, pady=5)
        
        # Unit cost
        ttk.Label(main_frame, text="Unit Cost:*").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cost_var = tk.StringVar(value="0.00")
        ttk.Entry(main_frame, textvariable=self.cost_var, width=47).grid(row=3, column=1, pady=5)
        
        # Total (calculated)
        ttk.Label(main_frame, text="Total Cost:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.total_label = ttk.Label(main_frame, text="$0.00", font=('Arial', 12, 'bold'))
        self.total_label.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Notes
        ttk.Label(main_frame, text="Notes:").grid(row=5, column=0, sticky=tk.NW, pady=5)
        self.notes_text = tk.Text(main_frame, width=35, height=4)
        self.notes_text.grid(row=5, column=1, pady=5)
        
        # Bind changes to calculate total
        self.quantity_var.trace('w', self.calculate_total)
        self.cost_var.trace('w', self.calculate_total)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Complete Purchase", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Load initial product supplier
        self.on_product_selected()
    
    def on_product_selected(self, event=None):
        """Update supplier when product is selected"""
        product_str = self.product_var.get()
        if not product_str:
            return
        
        product_id = int(product_str.split(' - ')[0])
        product = self.product_controller.get_product(product_id)
        
        if product and product.get('supplier_id'):
            # Try to select the product's default supplier
            supplier_id = product['supplier_id']
            for i, val in enumerate(self.supplier_combo['values']):
                if val.startswith(f"{supplier_id} -"):
                    self.supplier_combo.current(i)
                    break
    
    def calculate_total(self, *args):
        """Calculate and display total"""
        try:
            quantity = float(self.quantity_var.get())
            cost = float(self.cost_var.get())
            total = quantity * cost
            self.total_label.config(text=format_currency(total))
        except:
            self.total_label.config(text="$0.00")
    
    def save(self):
        """Save purchase"""
        product_str = self.product_var.get()
        supplier_str = self.supplier_var.get()
        
        if not product_str:
            messagebox.showerror("Error", "Please select a product")
            return
        
        if not supplier_str:
            messagebox.showerror("Error", "Please select a supplier")
            return
        
        product_id = int(product_str.split(' - ')[0])
        supplier_id = int(supplier_str.split(' - ')[0])
        
        # Validate quantity
        valid, quantity = validate_positive_integer(self.quantity_var.get(), "Quantity")
        if not valid or quantity == 0:
            messagebox.showerror("Error", "Quantity must be greater than 0")
            return
        
        # Validate cost
        valid, cost = validate_positive_number(self.cost_var.get(), "Unit cost")
        if not valid:
            messagebox.showerror("Error", cost)
            return
        
        notes = self.notes_text.get('1.0', tk.END).strip()
        user_id = self.auth_controller.get_current_user()['user_id']
        
        # Create purchase
        success, result = self.controller.create_purchase(
            product_id, supplier_id, quantity, cost, user_id, notes
        )
        
        if success:
            messagebox.showinfo("Success", "Purchase completed successfully")
            self.dialog.destroy()
            if self.callback:
                self.callback()
        else:
            messagebox.showerror("Error", result)
