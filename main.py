"""
Main Application Entry Point
Inventory Management System with Tkinter GUI
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.login_view import LoginView
from views.main_view import MainView
from models.database import DatabaseManager
import sys


class InventoryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Inventory Management System")
        self.root.geometry("1200x700")
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Current user
        self.current_user = None
        
        # Show login screen
        self.show_login()
        
    def show_login(self):
        """Show login screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show login view
        login_view = LoginView(self.root, self.db, self.on_login_success)
    
    def on_login_success(self, user):
        """Handle successful login"""
        self.current_user = user
        self.show_main_view()
    
    def show_main_view(self):
        """Show main application view"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show main view
        main_view = MainView(self.root, self.db, self.current_user, self.logout)
    
    def logout(self):
        """Handle logout"""
        self.current_user = None
        self.show_login()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
    
    def __del__(self):
        """Clean up on exit"""
        if hasattr(self, 'db'):
            self.db.close()


if __name__ == "__main__":
    try:
        app = InventoryApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Application error: {str(e)}")
        sys.exit(1)
Main Entry Point for Inventory Management System
"""

import tkinter as tk
from views.login_view import LoginView
from views.main_window import MainWindow


def start_application():
    """Start the application with login screen"""
    root = tk.Tk()
    
    def on_login_success(auth_controller):
        """Callback when login is successful"""
        # Create new root for main window
        main_root = tk.Tk()
        MainWindow(main_root, auth_controller)
        main_root.mainloop()
    
    # Show login window
    LoginView(root, on_login_success)
    root.mainloop()


if __name__ == "__main__":
    start_application()
