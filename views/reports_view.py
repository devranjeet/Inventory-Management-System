"""
Reports View - Generate various reports
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from models.sale_model import SaleModel
from models.purchase_model import PurchaseModel
from models.product_model import ProductModel
from utils.helpers import format_currency


class ReportsView:
    """View for generating reports"""
    
    def __init__(self, parent, auth_controller):
        self.parent = parent
        self.auth_controller = auth_controller
        self.sale_model = SaleModel()
        self.purchase_model = PurchaseModel()
        self.product_model = ProductModel()
        
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create reports view widgets"""
        # Title
        title_label = ttk.Label(self.frame, text="Reports", font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Report types
        reports_frame = ttk.LabelFrame(self.frame, text="Available Reports", padding="15")
        reports_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Sales Report
        sales_frame = ttk.LabelFrame(reports_frame, text="Sales Report", padding="10")
        sales_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        
        ttk.Label(sales_frame, text="Generate sales report for:").pack(pady=5)
        
        sales_btn_frame = ttk.Frame(sales_frame)
        sales_btn_frame.pack(pady=5)
        
        ttk.Button(sales_btn_frame, text="Last 7 Days", 
                  command=lambda: self.show_sales_report(7)).pack(side=tk.LEFT, padx=2)
        ttk.Button(sales_btn_frame, text="Last 30 Days",
                  command=lambda: self.show_sales_report(30)).pack(side=tk.LEFT, padx=2)
        ttk.Button(sales_btn_frame, text="Last 90 Days",
                  command=lambda: self.show_sales_report(90)).pack(side=tk.LEFT, padx=2)
        
        # Purchases Report
        purchases_frame = ttk.LabelFrame(reports_frame, text="Purchases Report", padding="10")
        purchases_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
        
        ttk.Label(purchases_frame, text="Generate purchases report for:").pack(pady=5)
        
        purchases_btn_frame = ttk.Frame(purchases_frame)
        purchases_btn_frame.pack(pady=5)
        
        ttk.Button(purchases_btn_frame, text="Last 7 Days",
                  command=lambda: self.show_purchases_report(7)).pack(side=tk.LEFT, padx=2)
        ttk.Button(purchases_btn_frame, text="Last 30 Days",
                  command=lambda: self.show_purchases_report(30)).pack(side=tk.LEFT, padx=2)
        ttk.Button(purchases_btn_frame, text="Last 90 Days",
                  command=lambda: self.show_purchases_report(90)).pack(side=tk.LEFT, padx=2)
        
        # Stock Report
        stock_frame = ttk.LabelFrame(reports_frame, text="Stock Report", padding="10")
        stock_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        
        ttk.Label(stock_frame, text="Generate stock reports:").pack(pady=5)
        
        stock_btn_frame = ttk.Frame(stock_frame)
        stock_btn_frame.pack(pady=5)
        
        ttk.Button(stock_btn_frame, text="Low Stock Items",
                  command=self.show_low_stock_report).pack(side=tk.LEFT, padx=2)
        ttk.Button(stock_btn_frame, text="Stock Value",
                  command=self.show_stock_value_report).pack(side=tk.LEFT, padx=2)
        
        # Top Products Report
        top_products_frame = ttk.LabelFrame(reports_frame, text="Product Performance", padding="10")
        top_products_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)
        
        ttk.Label(top_products_frame, text="View product performance:").pack(pady=5)
        
        ttk.Button(top_products_frame, text="Top Selling Products",
                  command=self.show_top_products).pack(pady=5)
        
        # Configure grid weights
        reports_frame.columnconfigure(0, weight=1)
        reports_frame.columnconfigure(1, weight=1)
        reports_frame.rowconfigure(0, weight=1)
        reports_frame.rowconfigure(1, weight=1)
    
    def show_sales_report(self, days):
        """Show sales report for last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        sales = self.sale_model.get_sales_by_date_range(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        total = sum(s.get('total_price', 0) for s in sales)
        
        # Create report window
        ReportWindow(self.frame, f"Sales Report - Last {days} Days", 
                    f"Total Sales: {format_currency(total)}\nTransactions: {len(sales)}",
                    sales, ['Date', 'Product', 'Quantity', 'Unit Price', 'Total', 'Customer'],
                    lambda s: [
                        s.get('sale_date', '')[:16] if s.get('sale_date') else '',
                        s.get('product_name', ''),
                        s.get('quantity', 0),
                        format_currency(s.get('unit_price', 0)),
                        format_currency(s.get('total_price', 0)),
                        s.get('customer_name', 'N/A')
                    ])
    
    def show_purchases_report(self, days):
        """Show purchases report for last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        purchases = self.purchase_model.get_purchases_by_date_range(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        total = sum(p.get('total_cost', 0) for p in purchases)
        
        # Create report window
        ReportWindow(self.frame, f"Purchases Report - Last {days} Days",
                    f"Total Purchases: {format_currency(total)}\nTransactions: {len(purchases)}",
                    purchases, ['Date', 'Product', 'Supplier', 'Quantity', 'Unit Cost', 'Total'],
                    lambda p: [
                        p.get('purchase_date', '')[:16] if p.get('purchase_date') else '',
                        p.get('product_name', ''),
                        p.get('supplier_name', ''),
                        p.get('quantity', 0),
                        format_currency(p.get('unit_cost', 0)),
                        format_currency(p.get('total_cost', 0))
                    ])
    
    def show_low_stock_report(self):
        """Show low stock items report"""
        products = self.product_model.get_low_stock_products()
        
        # Create report window
        ReportWindow(self.frame, "Low Stock Items Report",
                    f"Products below reorder level: {len(products)}",
                    products, ['Product', 'Category', 'In Stock', 'Reorder Level', 'Unit Price'],
                    lambda p: [
                        p.get('product_name', ''),
                        p.get('category_name', 'N/A'),
                        p.get('quantity_in_stock', 0),
                        p.get('reorder_level', 0),
                        format_currency(p.get('unit_price', 0))
                    ])
    
    def show_stock_value_report(self):
        """Show stock value report"""
        products = self.product_model.get_all_products()
        total_value = self.product_model.get_stock_value()
        
        # Calculate value for each product
        for p in products:
            p['stock_value'] = p.get('quantity_in_stock', 0) * p.get('unit_price', 0)
        
        # Create report window
        ReportWindow(self.frame, "Stock Value Report",
                    f"Total Stock Value: {format_currency(total_value)}\nTotal Products: {len(products)}",
                    products, ['Product', 'Category', 'Quantity', 'Unit Price', 'Stock Value'],
                    lambda p: [
                        p.get('product_name', ''),
                        p.get('category_name', 'N/A'),
                        p.get('quantity_in_stock', 0),
                        format_currency(p.get('unit_price', 0)),
                        format_currency(p.get('stock_value', 0))
                    ])
    
    def show_top_products(self):
        """Show top selling products"""
        products = self.sale_model.get_top_selling_products(10)
        
        # Create report window
        ReportWindow(self.frame, "Top Selling Products",
                    f"Top 10 products by sales volume",
                    products, ['Product', 'Total Quantity Sold', 'Total Revenue'],
                    lambda p: [
                        p.get('product_name', ''),
                        p.get('total_quantity', 0),
                        format_currency(p.get('total_revenue', 0))
                    ])
    
    def refresh(self):
        """Refresh reports view"""
        pass


class ReportWindow:
    """Window for displaying report data"""
    
    def __init__(self, parent, title, summary, data, columns, row_formatter):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("900x600")
        self.window.transient(parent)
        
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=title, font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Summary
        summary_label = ttk.Label(main_frame, text=summary, font=('Arial', 11))
        summary_label.pack(pady=(0, 10))
        
        # Data treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        tree.grid(row=0, column=0, sticky=tk.NSEW)
        vsb.grid(row=0, column=1, sticky=tk.NS)
        hsb.grid(row=1, column=0, sticky=tk.EW)
        
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        # Populate data
        for item in data:
            tree.insert('', tk.END, values=row_formatter(item))
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.window.destroy).pack(pady=5)
