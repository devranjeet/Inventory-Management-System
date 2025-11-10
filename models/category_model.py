"""
Category Model for category management
"""

from models.base_model import BaseModel
from typing import Optional, Dict, Any


class CategoryModel(BaseModel):
    """Model for category-related database operations"""
    
    def get_all_categories(self) -> list:
        """Get all categories"""
        query = "SELECT * FROM categories ORDER BY category_name"
        results = self.db.execute_query(query)
        return self.to_dict_list(results)
    
    def get_category_by_id(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Get category by ID"""
        query = "SELECT * FROM categories WHERE category_id = ?"
        results = self.db.execute_query(query, (category_id,))
        
        if results and len(results) > 0:
            return self.to_dict(results[0])
        return None
    
    def create_category(self, category_name: str, description: str = "") -> tuple:
        """Create a new category"""
        query = "INSERT INTO categories (category_name, description) VALUES (?, ?)"
        success, category_id = self.db.execute_update(query, (category_name, description))
        return success, category_id
    
    def update_category(self, category_id: int, category_name: str, description: str) -> bool:
        """Update category information"""
        query = "UPDATE categories SET category_name = ?, description = ? WHERE category_id = ?"
        success, _ = self.db.execute_update(query, (category_name, description, category_id))
        return success
    
    def delete_category(self, category_id: int) -> bool:
        """Delete a category"""
        query = "DELETE FROM categories WHERE category_id = ?"
        success, _ = self.db.execute_update(query, (category_id,))
        return success
    
    def get_products_count(self, category_id: int) -> int:
        """Get count of products in a category"""
        query = "SELECT COUNT(*) as count FROM products WHERE category_id = ?"
        results = self.db.execute_query(query, (category_id,))
        
        if results and len(results) > 0:
            return results[0]['count']
        return 0
