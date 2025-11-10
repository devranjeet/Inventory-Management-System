"""
Login View
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.user import UserManager


class LoginView:
    def __init__(self, parent, db, on_success_callback):
        self.parent = parent
        self.db = db
        self.on_success = on_success_callback
        self.user_manager = UserManager(db)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create login form widgets"""
        # Main frame
        main_frame = ttk.Frame(self.parent, padding="50")
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_label = ttk.Label(main_frame, text="Inventory Management System", 
                               font=('Helvetica', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="Please login to continue", 
                                   font=('Helvetica', 12))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Username
        ttk.Label(main_frame, text="Username:", font=('Helvetica', 11)).grid(row=2, column=0, 
                                                                             sticky='e', pady=10, padx=5)
        self.username_entry = ttk.Entry(main_frame, width=30, font=('Helvetica', 11))
        self.username_entry.grid(row=2, column=1, pady=10, padx=5)
        self.username_entry.focus()
        
        # Password
        ttk.Label(main_frame, text="Password:", font=('Helvetica', 11)).grid(row=3, column=0, 
                                                                             sticky='e', pady=10, padx=5)
        self.password_entry = ttk.Entry(main_frame, width=30, show="*", font=('Helvetica', 11))
        self.password_entry.grid(row=3, column=1, pady=10, padx=5)
        
        # Login button
        login_btn = ttk.Button(main_frame, text="Login", command=self.login, width=20)
        login_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Default credentials info
        info_label = ttk.Label(main_frame, 
                              text="Default credentials: admin / admin123", 
                              font=('Helvetica', 9), foreground='gray')
        info_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Bind Enter key to login
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        # Authenticate user
        user = self.user_manager.authenticate_user(username, password)
        
        if user:
            messagebox.showinfo("Success", f"Welcome, {user['full_name']}!")
            self.on_success(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
