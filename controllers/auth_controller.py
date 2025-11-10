"""
Authentication Controller
Handles user authentication and session management
"""

from models.user_model import UserModel
from typing import Optional, Dict, Any


class AuthController:
    """Controller for authentication operations"""
    
    def __init__(self):
        self.user_model = UserModel()
        self.current_user = None
    
    def login(self, username: str, password: str) -> tuple:
        """
        Authenticate user and create session
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Tuple of (success, user_data or error_message)
        """
        if not username or not password:
            return False, "Username and password are required"
        
        user = self.user_model.authenticate(username, password)
        
        if user:
            self.current_user = user
            return True, user
        else:
            return False, "Invalid username or password"
    
    def logout(self):
        """Clear current session"""
        self.current_user = None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged-in user"""
        return self.current_user
    
    def is_admin(self) -> bool:
        """Check if current user is admin"""
        return self.current_user and self.current_user.get('role') == 'admin'
