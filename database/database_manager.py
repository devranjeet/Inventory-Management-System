"""
Database Manager for Inventory Management System
Handles all database connections and initialization
"""

import sqlite3
import os
from typing import Optional, Tuple


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, db_path: str = "database/inventory.db"):
        """
        Initialize the database manager
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._ensure_database_directory()
        self.initialize_database()
    
    def _ensure_database_directory(self):
        """Ensure the database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection
        
        Returns:
            SQLite connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_database(self):
        """Initialize database with schema"""
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        
        if not os.path.exists(schema_path):
            print(f"Warning: Schema file not found at {schema_path}")
            return
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.executescript(schema_sql)
            conn.commit()
            print("Database initialized successfully")
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[list]:
        """
        Execute a SELECT query and return results
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of rows or None on error
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    
    def execute_update(self, query: str, params: tuple = ()) -> Tuple[bool, Optional[int]]:
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Tuple of (success, last_row_id or rows_affected)
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            
            if query.strip().upper().startswith('INSERT'):
                return True, cursor.lastrowid
            else:
                return True, cursor.rowcount
        except sqlite3.Error as e:
            print(f"Error executing update: {e}")
            conn.rollback()
            return False, None
        finally:
            conn.close()
    
    def execute_many(self, query: str, params_list: list) -> bool:
        """
        Execute multiple queries with different parameters
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
            
        Returns:
            True if successful, False otherwise
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error executing batch update: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()


# Singleton instance
_db_manager = None


def get_db_manager() -> DatabaseManager:
    """Get or create the database manager singleton"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
