"""
Login View for the Inventory Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController


class LoginView:
    """Login window for user authentication"""
    
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.auth_controller = AuthController()
        
        # Configure root window
        self.root.title("Inventory Management System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Create UI
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create login form widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Inventory Management System",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 30))
        
        # Login form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=10)
        
        # Username
        ttk.Label(form_frame, text="Username:", font=('Arial', 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.username_entry = ttk.Entry(form_frame, width=25, font=('Arial', 10))
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(form_frame, text="Password:", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.password_entry = ttk.Entry(form_frame, width=25, show="*", font=('Arial', 10))
        self.password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Login button
        login_btn = ttk.Button(
            main_frame,
            text="Login",
            command=self.handle_login,
            width=20
        )
        login_btn.pack(pady=20)
        
        # Info label
        info_label = ttk.Label(
            main_frame,
            text="Default login: admin / admin123",
            font=('Arial', 9),
            foreground='gray'
        )
        info_label.pack(pady=5)
        
        # Bind Enter key to login
        self.username_entry.bind('<Return>', lambda e: self.handle_login())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Focus on username
        self.username_entry.focus()
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        success, result = self.auth_controller.login(username, password)
        
        if success:
            # Close login window and open main window
            self.root.destroy()
            self.on_login_success(self.auth_controller)
        else:
            messagebox.showerror("Login Failed", result)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
