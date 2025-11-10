"""
Sales View - Manage sales transactions
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.sales_controller import SalesController
from controllers.product_controller import ProductController
from utils.helpers import format_currency, validate_positive_number, validate_positive_integer


class SalesView:
    """View for managing sales"""
    
    def __init__(self, parent, auth_controller):
        self.parent = parent
        self.auth_controller = auth_controller
        self.controller = SalesController()
        self.product_controller = ProductController()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_sales()
    
    def create_widgets(self):
        """Create sales view widgets"""
        # Title
        title_label = ttk.Label(self.frame, text="Sales", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Toolbar
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="New Sale", command=self.add_sale).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Refresh", command=self.load_sales).pack(side=tk.LEFT)
        
        # Sales treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Date', 'Product', 'Quantity', 'Unit Price', 'Total', 'Customer')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Product', text='Product')
        self.tree.heading('Quantity', text='Qty')
        self.tree.heading('Unit Price', text='Unit Price')
        self.tree.heading('Total', text='Total')
        self.tree.heading('Customer', text='Customer')
        
        self.tree.column('ID', width=60, anchor=tk.CENTER)
        self.tree.column('Date', width=150)
        self.tree.column('Product', width=200)
        self.tree.column('Quantity', width=80, anchor=tk.CENTER)
        self.tree.column('Unit Price', width=100, anchor=tk.E)
        self.tree.column('Total', width=100, anchor=tk.E)
        self.tree.column('Customer', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_sales(self):
        """Load all sales"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        sales = self.controller.get_all_sales()
        for sale in sales:
            sale_date = sale.get('sale_date', '')
            if sale_date:
                try:
                    date_obj = datetime.strptime(sale_date, "%Y-%m-%d %H:%M:%S")
                    sale_date = date_obj.strftime("%Y-%m-%d %I:%M %p")
                except:
                    pass
            
            self.tree.insert('', tk.END, values=(
                sale.get('sale_id', ''),
                sale_date,
                sale.get('product_name', 'N/A'),
                sale.get('quantity', 0),
                format_currency(sale.get('unit_price', 0)),
                format_currency(sale.get('total_price', 0)),
                sale.get('customer_name', 'N/A')
            ))
    
    def add_sale(self):
        """Open dialog to add new sale"""
        SaleDialog(self.frame, self.controller, self.product_controller, 
                  self.auth_controller, callback=self.load_sales)
    
    def refresh(self):
        """Refresh sales list"""
        self.load_sales()


class SaleDialog:
    """Dialog for adding sales"""
    
    def __init__(self, parent, controller, product_controller, auth_controller, callback=None):
        self.controller = controller
        self.product_controller = product_controller
        self.auth_controller = auth_controller
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Sale")
        self.dialog.geometry("500x400")
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
        product_values = [f"{p['product_id']} - {p['product_name']} (Stock: {p['quantity_in_stock']})" 
                         for p in products]
        self.product_combo = ttk.Combobox(main_frame, textvariable=self.product_var,
                                          values=product_values, width=45, state='readonly')
        self.product_combo.grid(row=0, column=1, pady=5)
        if product_values:
            self.product_combo.current(0)
        self.product_combo.bind('<<ComboboxSelected>>', self.on_product_selected)
        
        # Quantity
        ttk.Label(main_frame, text="Quantity:*").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="1")
        ttk.Entry(main_frame, textvariable=self.quantity_var, width=47).grid(row=1, column=1, pady=5)
        
        # Unit price
        ttk.Label(main_frame, text="Unit Price:*").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.price_var = tk.StringVar(value="0.00")
        ttk.Entry(main_frame, textvariable=self.price_var, width=47).grid(row=2, column=1, pady=5)
        
        # Total (calculated)
        ttk.Label(main_frame, text="Total:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.total_label = ttk.Label(main_frame, text="$0.00", font=('Arial', 12, 'bold'))
        self.total_label.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Customer name
        ttk.Label(main_frame, text="Customer Name:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.customer_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.customer_var, width=47).grid(row=4, column=1, pady=5)
        
        # Notes
        ttk.Label(main_frame, text="Notes:").grid(row=5, column=0, sticky=tk.NW, pady=5)
        self.notes_text = tk.Text(main_frame, width=35, height=4)
        self.notes_text.grid(row=5, column=1, pady=5)
        
        # Bind changes to calculate total
        self.quantity_var.trace('w', self.calculate_total)
        self.price_var.trace('w', self.calculate_total)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Complete Sale", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Load initial product price
        self.on_product_selected()
    
    def on_product_selected(self, event=None):
        """Update price when product is selected"""
        product_str = self.product_var.get()
        if not product_str:
            return
        
        product_id = int(product_str.split(' - ')[0])
        product = self.product_controller.get_product(product_id)
        
        if product:
            self.price_var.set(str(product['unit_price']))
    
    def calculate_total(self, *args):
        """Calculate and display total"""
        try:
            quantity = float(self.quantity_var.get())
            price = float(self.price_var.get())
            total = quantity * price
            self.total_label.config(text=format_currency(total))
        except:
            self.total_label.config(text="$0.00")
    
    def save(self):
        """Save sale"""
        product_str = self.product_var.get()
        
        if not product_str:
            messagebox.showerror("Error", "Please select a product")
            return
        
        product_id = int(product_str.split(' - ')[0])
        
        # Validate quantity
        valid, quantity = validate_positive_integer(self.quantity_var.get(), "Quantity")
        if not valid or quantity == 0:
            messagebox.showerror("Error", "Quantity must be greater than 0")
            return
        
        # Validate price
        valid, price = validate_positive_number(self.price_var.get(), "Unit price")
        if not valid:
            messagebox.showerror("Error", price)
            return
        
        customer_name = self.customer_var.get().strip()
        notes = self.notes_text.get('1.0', tk.END).strip()
        user_id = self.auth_controller.get_current_user()['user_id']
        
        # Create sale
        success, result = self.controller.create_sale(
            product_id, quantity, price, user_id, customer_name, notes
        )
        
        if success:
            messagebox.showinfo("Success", "Sale completed successfully")
            self.dialog.destroy()
            if self.callback:
                self.callback()
        else:
            messagebox.showerror("Error", result)
