"""
User Model for authentication and user management
"""

from models.base_model import BaseModel
from typing import Optional, Dict, Any


class UserModel(BaseModel):
    """Model for user-related database operations"""
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with username and password
        
        Args:
            username: User's username
            password: User's password (plain text - in production, use hashed passwords)
            
        Returns:
            User data dictionary if authenticated, None otherwise
        """
        query = """
            SELECT user_id, username, full_name, role, is_active 
            FROM users 
            WHERE username = ? AND password = ? AND is_active = 1
        """
        results = self.db.execute_query(query, (username, password))
        
        if results and len(results) > 0:
            return self.to_dict(results[0])
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE user_id = ?"
        results = self.db.execute_query(query, (user_id,))
        
        if results and len(results) > 0:
            return self.to_dict(results[0])
        return None
    
    def get_all_users(self) -> list:
        """Get all active users"""
        query = "SELECT user_id, username, full_name, role, created_at, is_active FROM users ORDER BY username"
        results = self.db.execute_query(query)
        return self.to_dict_list(results)
    
    def create_user(self, username: str, password: str, full_name: str, role: str = 'user') -> tuple:
        """
        Create a new user
        
        Args:
            username: Unique username
            password: User's password
            full_name: User's full name
            role: User role (admin/user)
            
        Returns:
            Tuple of (success, user_id or error message)
        """
        query = """
            INSERT INTO users (username, password, full_name, role) 
            VALUES (?, ?, ?, ?)
        """
        success, user_id = self.db.execute_update(query, (username, password, full_name, role))
        return success, user_id
    
    def update_user(self, user_id: int, username: str, full_name: str, role: str) -> bool:
        """Update user information"""
        query = """
            UPDATE users 
            SET username = ?, full_name = ?, role = ? 
            WHERE user_id = ?
        """
        success, _ = self.db.execute_update(query, (username, full_name, role, user_id))
        return success
    
    def change_password(self, user_id: int, new_password: str) -> bool:
        """Change user password"""
        query = "UPDATE users SET password = ? WHERE user_id = ?"
        success, _ = self.db.execute_update(query, (new_password, user_id))
        return success
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user"""
        query = "UPDATE users SET is_active = 0 WHERE user_id = ?"
        success, _ = self.db.execute_update(query, (user_id,))
        return success
