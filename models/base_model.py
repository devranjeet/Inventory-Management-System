"""
Base Model class for all models in the Inventory Management System
"""

from database.database_manager import get_db_manager
from typing import Optional, List, Dict, Any


class BaseModel:
    """Base class for all models"""
    
    def __init__(self):
        self.db = get_db_manager()
    
    def to_dict(self, row) -> Dict[str, Any]:
        """Convert a database row to a dictionary"""
        if row is None:
            return None
        return dict(row)
    
    def to_dict_list(self, rows) -> List[Dict[str, Any]]:
        """Convert a list of database rows to a list of dictionaries"""
        if rows is None:
            return []
        return [dict(row) for row in rows]
