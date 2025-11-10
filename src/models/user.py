"""
User Management Module
Handles user authentication and user-related operations
"""
import bcrypt
from datetime import datetime


class UserManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def authenticate_user(self, username, password):
        """Authenticate user with username and password"""
        try:
            self.db.cursor.execute('''
                SELECT user_id, username, password, full_name, role, is_active
                FROM users
                WHERE username = ?
            ''', (username,))
            
            user = self.db.cursor.fetchone()
            
            if user and user['is_active']:
                stored_password = user['password']
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    return {
                        'user_id': user['user_id'],
                        'username': user['username'],
                        'full_name': user['full_name'],
                        'role': user['role']
                    }
            return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def add_user(self, username, password, full_name, role, email=None, phone=None):
        """Add a new user"""
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.db.cursor.execute('''
                INSERT INTO users (username, password, full_name, role, email, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password.decode('utf-8'), full_name, role, email, phone))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def update_user(self, user_id, full_name=None, email=None, phone=None, role=None):
        """Update user information"""
        try:
            updates = []
            params = []
            
            if full_name:
                updates.append("full_name = ?")
                params.append(full_name)
            if email:
                updates.append("email = ?")
                params.append(email)
            if phone:
                updates.append("phone = ?")
                params.append(phone)
            if role:
                updates.append("role = ?")
                params.append(role)
            
            if not updates:
                return False
            
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
            
            self.db.cursor.execute(query, params)
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def change_password(self, user_id, new_password):
        """Change user password"""
        try:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self.db.cursor.execute('''
                UPDATE users SET password = ? WHERE user_id = ?
            ''', (hashed_password.decode('utf-8'), user_id))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
    
    def deactivate_user(self, user_id):
        """Deactivate a user account"""
        try:
            self.db.cursor.execute('''
                UPDATE users SET is_active = 0 WHERE user_id = ?
            ''', (user_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error deactivating user: {e}")
            return False
    
    def activate_user(self, user_id):
        """Activate a user account"""
        try:
            self.db.cursor.execute('''
                UPDATE users SET is_active = 1 WHERE user_id = ?
            ''', (user_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error activating user: {e}")
            return False
    
    def get_all_users(self):
        """Get all users"""
        try:
            self.db.cursor.execute('''
                SELECT user_id, username, full_name, role, email, phone, is_active, created_at
                FROM users
                ORDER BY created_at DESC
            ''')
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            self.db.cursor.execute('''
                SELECT user_id, username, full_name, role, email, phone, is_active, created_at
                FROM users
                WHERE user_id = ?
            ''', (user_id,))
            return self.db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
