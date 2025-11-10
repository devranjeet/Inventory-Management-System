"""
Product Model for product management
"""

from models.base_model import BaseModel
from typing import Optional, Dict, Any


class ProductModel(BaseModel):
    """Model for product-related database operations"""
    
    def get_all_products(self) -> list:
        """Get all products with category and supplier names"""
        query = """
            SELECT p.*, c.category_name, s.supplier_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.product_name
        """
        results = self.db.execute_query(query)
        return self.to_dict_list(results)
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get product by ID"""
        query = """
            SELECT p.*, c.category_name, s.supplier_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            WHERE p.product_id = ?
        """
        results = self.db.execute_query(query, (product_id,))
        
        if results and len(results) > 0:
            return self.to_dict(results[0])
        return None
    
    def search_products(self, search_term: str) -> list:
        """Search products by name or description"""
        query = """
            SELECT p.*, c.category_name, s.supplier_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            WHERE p.product_name LIKE ? OR p.description LIKE ?
            ORDER BY p.product_name
        """
        search_pattern = f"%{search_term}%"
        results = self.db.execute_query(query, (search_pattern, search_pattern))
        return self.to_dict_list(results)
    
    def create_product(self, product_name: str, category_id: int, supplier_id: int,
                      description: str, unit_price: float, quantity_in_stock: int = 0,
                      reorder_level: int = 10) -> tuple:
        """Create a new product"""
        query = """
            INSERT INTO products (product_name, category_id, supplier_id, description, 
                                unit_price, quantity_in_stock, reorder_level)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        success, product_id = self.db.execute_update(
            query,
            (product_name, category_id, supplier_id, description, 
             unit_price, quantity_in_stock, reorder_level)
        )
        return success, product_id
    
    def update_product(self, product_id: int, product_name: str, category_id: int,
                      supplier_id: int, description: str, unit_price: float,
                      quantity_in_stock: int, reorder_level: int) -> bool:
        """Update product information"""
        query = """
            UPDATE products 
            SET product_name = ?, category_id = ?, supplier_id = ?, 
                description = ?, unit_price = ?, quantity_in_stock = ?, 
                reorder_level = ?, updated_at = CURRENT_TIMESTAMP
            WHERE product_id = ?
        """
        success, _ = self.db.execute_update(
            query,
            (product_name, category_id, supplier_id, description,
             unit_price, quantity_in_stock, reorder_level, product_id)
        )
        return success
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        query = "DELETE FROM products WHERE product_id = ?"
        success, _ = self.db.execute_update(query, (product_id,))
        return success
    
    def update_stock(self, product_id: int, quantity_change: int) -> bool:
        """
        Update product stock quantity
        
        Args:
            product_id: ID of the product
            quantity_change: Amount to add (positive) or subtract (negative)
        """
        query = """
            UPDATE products 
            SET quantity_in_stock = quantity_in_stock + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE product_id = ?
        """
        success, _ = self.db.execute_update(query, (quantity_change, product_id))
        return success
    
    def get_low_stock_products(self) -> list:
        """Get products with stock below reorder level"""
        query = """
            SELECT p.*, c.category_name, s.supplier_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
            WHERE p.quantity_in_stock <= p.reorder_level
            ORDER BY p.quantity_in_stock ASC
        """
        results = self.db.execute_query(query)
        return self.to_dict_list(results)
    
    def get_stock_value(self) -> float:
        """Get total value of all stock"""
        query = "SELECT SUM(quantity_in_stock * unit_price) as total_value FROM products"
        results = self.db.execute_query(query)
        
        if results and len(results) > 0 and results[0]['total_value'] is not None:
            return float(results[0]['total_value'])
        return 0.0
