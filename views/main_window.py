"""
Main Application Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.dashboard_view import DashboardView
from views.products_view import ProductsView
from views.categories_view import CategoriesView
from views.suppliers_view import SuppliersView
from views.sales_view import SalesView
from views.purchases_view import PurchasesView
from views.reports_view import ReportsView


class MainWindow:
    """Main application window with navigation"""
    
    def __init__(self, root, auth_controller):
        self.root = root
        self.auth_controller = auth_controller
        self.current_view = None
        
        # Configure root window
        self.root.title("Inventory Management System")
        self.root.geometry("1200x700")
        
        # Create UI
        self.create_menu()
        self.create_widgets()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Dashboard", command=self.show_dashboard)
        view_menu.add_command(label="Products", command=self.show_products)
        view_menu.add_command(label="Categories", command=self.show_categories)
        view_menu.add_command(label="Suppliers", command=self.show_suppliers)
        view_menu.add_command(label="Sales", command=self.show_sales)
        view_menu.add_command(label="Purchases", command=self.show_purchases)
        view_menu.add_command(label="Reports", command=self.show_reports)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create main window widgets"""
        # Header
        header_frame = ttk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="Inventory Management System",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # User info
        user = self.auth_controller.get_current_user()
        user_info = ttk.Label(
            header_frame,
            text=f"Logged in as: {user['full_name']} ({user['role']})",
            font=('Arial', 10)
        )
        user_info.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Main container with sidebar and content
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = ttk.Frame(main_container, relief=tk.RIDGE, borderwidth=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0), pady=5)
        
        ttk.Label(sidebar, text="Navigation", font=('Arial', 12, 'bold')).pack(pady=10, padx=10)
        
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Products", self.show_products),
            ("Categories", self.show_categories),
            ("Suppliers", self.show_suppliers),
            ("Sales", self.show_sales),
            ("Purchases", self.show_purchases),
            ("Reports", self.show_reports),
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(sidebar, text=text, command=command, width=18)
            btn.pack(padx=10, pady=2)
        
        ttk.Separator(sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Button(sidebar, text="Logout", command=self.logout, width=18).pack(padx=10, pady=2)
        
        # Content area
        self.content_frame = ttk.Frame(main_container)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_view = None
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.clear_content()
        self.current_view = DashboardView(self.content_frame, self.auth_controller)
    
    def show_products(self):
        """Show products view"""
        self.clear_content()
        self.current_view = ProductsView(self.content_frame, self.auth_controller)
    
    def show_categories(self):
        """Show categories view"""
        self.clear_content()
        self.current_view = CategoriesView(self.content_frame, self.auth_controller)
    
    def show_suppliers(self):
        """Show suppliers view"""
        self.clear_content()
        self.current_view = SuppliersView(self.content_frame, self.auth_controller)
    
    def show_sales(self):
        """Show sales view"""
        self.clear_content()
        self.current_view = SalesView(self.content_frame, self.auth_controller)
    
    def show_purchases(self):
        """Show purchases view"""
        self.clear_content()
        self.current_view = PurchasesView(self.content_frame, self.auth_controller)
    
    def show_reports(self):
        """Show reports view"""
        self.clear_content()
        self.current_view = ReportsView(self.content_frame, self.auth_controller)
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.auth_controller.logout()
            self.root.destroy()
            
            # Restart application with login screen
            from main import start_application
            start_application()
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Inventory Management System
Version 1.0

A complete inventory management solution built with Python and SQLite3.

Features:
• User authentication and management
• Product, category, and supplier management
• Sales and purchase tracking
• Stock monitoring and alerts
• Comprehensive reporting

© 2024 All rights reserved."""
        
        messagebox.showinfo("About", about_text)
