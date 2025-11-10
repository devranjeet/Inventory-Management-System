"""
Dashboard View - Main window of the Inventory Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.product_model import ProductModel
from models.sale_model import SaleModel
from models.purchase_model import PurchaseModel
from utils.helpers import format_currency


class DashboardView:
    """Dashboard showing overview and statistics"""
    
    def __init__(self, parent, auth_controller):
        self.parent = parent
        self.auth_controller = auth_controller
        self.product_model = ProductModel()
        self.sale_model = SaleModel()
        self.purchase_model = PurchaseModel()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create dashboard widgets"""
        # Title
        title_label = ttk.Label(
            self.frame,
            text="Dashboard",
            font=('Arial', 18, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(self.frame, text="Statistics (Last 30 Days)", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create statistics cards
        cards_frame = ttk.Frame(stats_frame)
        cards_frame.pack(fill=tk.X)
        
        # Sales card
        self.sales_card = self.create_stat_card(cards_frame, "Total Sales", "$0.00", "0 transactions")
        self.sales_card.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        
        # Purchases card
        self.purchases_card = self.create_stat_card(cards_frame, "Total Purchases", "$0.00", "0 transactions")
        self.purchases_card.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
        
        # Stock value card
        self.stock_card = self.create_stat_card(cards_frame, "Stock Value", "$0.00", "All products")
        self.stock_card.grid(row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
        
        # Configure grid weights
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)
        
        # Low stock alerts
        alerts_frame = ttk.LabelFrame(self.frame, text="Low Stock Alerts", padding="10")
        alerts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for low stock products
        columns = ('Product', 'Category', 'In Stock', 'Reorder Level')
        self.low_stock_tree = ttk.Treeview(alerts_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.low_stock_tree.heading('Product', text='Product Name')
        self.low_stock_tree.heading('Category', text='Category')
        self.low_stock_tree.heading('In Stock', text='In Stock')
        self.low_stock_tree.heading('Reorder Level', text='Reorder Level')
        
        self.low_stock_tree.column('Product', width=200)
        self.low_stock_tree.column('Category', width=150)
        self.low_stock_tree.column('In Stock', width=100, anchor=tk.CENTER)
        self.low_stock_tree.column('Reorder Level', width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(alerts_frame, orient=tk.VERTICAL, command=self.low_stock_tree.yview)
        self.low_stock_tree.configure(yscrollcommand=scrollbar.set)
        
        self.low_stock_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh button
        refresh_btn = ttk.Button(self.frame, text="Refresh Data", command=self.load_data)
        refresh_btn.pack(pady=5)
    
    def create_stat_card(self, parent, title, value, subtitle):
        """Create a statistics card widget"""
        card = ttk.Frame(parent, relief=tk.RIDGE, borderwidth=2)
        card_inner = ttk.Frame(card, padding="15")
        card_inner.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(card_inner, text=title, font=('Arial', 10))
        title_label.pack()
        
        value_label = ttk.Label(card_inner, text=value, font=('Arial', 16, 'bold'))
        value_label.pack(pady=5)
        
        subtitle_label = ttk.Label(card_inner, text=subtitle, font=('Arial', 9), foreground='gray')
        subtitle_label.pack()
        
        # Store references to update later
        card.value_label = value_label
        card.subtitle_label = subtitle_label
        
        return card
    
    def load_data(self):
        """Load dashboard data"""
        try:
            # Load sales statistics
            total_sales = self.sale_model.get_total_sales(30)
            sales_count = self.sale_model.get_sales_count(30)
            self.sales_card.value_label.config(text=format_currency(total_sales))
            self.sales_card.subtitle_label.config(text=f"{sales_count} transactions")
            
            # Load purchases statistics
            total_purchases = self.purchase_model.get_total_purchases(30)
            purchases_count = self.purchase_model.get_purchases_count(30)
            self.purchases_card.value_label.config(text=format_currency(total_purchases))
            self.purchases_card.subtitle_label.config(text=f"{purchases_count} transactions")
            
            # Load stock value
            stock_value = self.product_model.get_stock_value()
            self.stock_card.value_label.config(text=format_currency(stock_value))
            
            # Load low stock products
            self.load_low_stock_products()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dashboard data: {str(e)}")
    
    def load_low_stock_products(self):
        """Load products with low stock"""
        # Clear existing items
        for item in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(item)
        
        # Get low stock products
        products = self.product_model.get_low_stock_products()
        
        if not products:
            # Show message if no low stock products
            self.low_stock_tree.insert('', tk.END, values=('No low stock alerts', '', '', ''))
        else:
            for product in products:
                self.low_stock_tree.insert('', tk.END, values=(
                    product.get('product_name', 'N/A'),
                    product.get('category_name', 'N/A'),
                    product.get('quantity_in_stock', 0),
                    product.get('reorder_level', 0)
                ))
    
    def refresh(self):
        """Refresh dashboard data"""
        self.load_data()
