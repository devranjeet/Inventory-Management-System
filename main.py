"""
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
