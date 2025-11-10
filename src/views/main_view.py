"""
Main Application View
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.dashboard_view import DashboardView
from views.products_view import ProductsView
from views.categories_view import CategoriesView
from views.suppliers_view import SuppliersView
from views.purchases_view import PurchasesView
from views.sales_view import SalesView
from views.customers_view import CustomersView
from views.reports_view import ReportsView
from views.expenses_view import ExpensesView
from views.settings_view import SettingsView
from views.users_view import UsersView


class MainView:
    def __init__(self, parent, db, current_user, logout_callback):
        self.parent = parent
        self.db = db
        self.current_user = current_user
        self.logout_callback = logout_callback
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create main application widgets"""
        # Top bar
        self.create_top_bar()
        
        # Main container
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill='both', expand=True)
        
        # Left sidebar
        self.create_sidebar(main_container)
        
        # Content area
        self.content_frame = ttk.Frame(main_container)
        self.content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_top_bar(self):
        """Create top bar with user info and logout"""
        top_bar = ttk.Frame(self.parent, relief='raised', height=50)
        top_bar.pack(side='top', fill='x')
        
        # Title
        title_label = ttk.Label(top_bar, text="Inventory Management System", 
                               font=('Helvetica', 16, 'bold'))
        title_label.pack(side='left', padx=20, pady=10)
        
        # User info
        user_label = ttk.Label(top_bar, 
                              text=f"User: {self.current_user['full_name']} ({self.current_user['role']})", 
                              font=('Helvetica', 10))
        user_label.pack(side='right', padx=10, pady=10)
        
        # Logout button
        logout_btn = ttk.Button(top_bar, text="Logout", command=self.logout)
        logout_btn.pack(side='right', padx=10, pady=10)
    
    def create_sidebar(self, parent):
        """Create sidebar navigation"""
        sidebar = ttk.Frame(parent, relief='raised', width=200)
        sidebar.pack(side='left', fill='y', padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Navigation buttons
        buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📦 Products", self.show_products),
            ("🗂️ Categories", self.show_categories),
            ("🏷️ Suppliers", self.show_suppliers),
            ("📥 Purchases", self.show_purchases),
            ("📤 Sales", self.show_sales),
            ("👥 Customers", self.show_customers),
            ("📊 Reports", self.show_reports),
            ("💰 Expenses", self.show_expenses),
            ("⚙️ Settings", self.show_settings),
        ]
        
        # Add Users button only for Admin
        if self.current_user['role'] == 'Admin':
            buttons.append(("👤 Users", self.show_users))
        
        for text, command in buttons:
            btn = ttk.Button(sidebar, text=text, command=command, width=25)
            btn.pack(pady=5, padx=10, fill='x')
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_content()
        DashboardView(self.content_frame, self.db, self.current_user)
    
    def show_products(self):
        """Show products view"""
        self.clear_content()
        ProductsView(self.content_frame, self.db, self.current_user)
    
    def show_categories(self):
        """Show categories view"""
        self.clear_content()
        CategoriesView(self.content_frame, self.db, self.current_user)
    
    def show_suppliers(self):
        """Show suppliers view"""
        self.clear_content()
        SuppliersView(self.content_frame, self.db, self.current_user)
    
    def show_purchases(self):
        """Show purchases view"""
        self.clear_content()
        PurchasesView(self.content_frame, self.db, self.current_user)
    
    def show_sales(self):
        """Show sales view"""
        self.clear_content()
        SalesView(self.content_frame, self.db, self.current_user)
    
    def show_customers(self):
        """Show customers view"""
        self.clear_content()
        CustomersView(self.content_frame, self.db, self.current_user)
    
    def show_reports(self):
        """Show reports view"""
        self.clear_content()
        ReportsView(self.content_frame, self.db, self.current_user)
    
    def show_expenses(self):
        """Show expenses view"""
        self.clear_content()
        ExpensesView(self.content_frame, self.db, self.current_user)
    
    def show_settings(self):
        """Show settings view"""
        self.clear_content()
        SettingsView(self.content_frame, self.db, self.current_user)
    
    def show_users(self):
        """Show users view"""
        if self.current_user['role'] != 'Admin':
            messagebox.showerror("Access Denied", "Only administrators can access user management")
            return
        self.clear_content()
        UsersView(self.content_frame, self.db, self.current_user)
    
    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.logout_callback()
