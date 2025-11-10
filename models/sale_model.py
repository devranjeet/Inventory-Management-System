"""
Sale Model for sales management
"""

from models.base_model import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class SaleModel(BaseModel):
    """Model for sales-related database operations"""
    
    def get_all_sales(self, limit: int = 100) -> list:
        """Get all sales with product names"""
        query = """
            SELECT s.*, p.product_name, u.username
            FROM sales s
            LEFT JOIN products p ON s.product_id = p.product_id
            LEFT JOIN users u ON s.user_id = u.user_id
            ORDER BY s.sale_date DESC
            LIMIT ?
        """
        results = self.db.execute_query(query, (limit,))
        return self.to_dict_list(results)
    
    def get_sale_by_id(self, sale_id: int) -> Optional[Dict[str, Any]]:
        """Get sale by ID"""
        query = """
            SELECT s.*, p.product_name, u.username
            FROM sales s
            LEFT JOIN products p ON s.product_id = p.product_id
            LEFT JOIN users u ON s.user_id = u.user_id
            WHERE s.sale_id = ?
        """
        results = self.db.execute_query(query, (sale_id,))
        
        if results and len(results) > 0:
            return self.to_dict(results[0])
        return None
    
    def create_sale(self, product_id: int, quantity: int, unit_price: float,
                   user_id: int, customer_name: str = "", notes: str = "") -> tuple:
        """
        Create a new sale and update product stock
        
        Returns:
            Tuple of (success, sale_id or error message)
        """
        total_price = quantity * unit_price
        
        # Insert sale
        query = """
            INSERT INTO sales (product_id, quantity, unit_price, total_price, 
                             user_id, customer_name, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        success, sale_id = self.db.execute_update(
            query,
            (product_id, quantity, unit_price, total_price, user_id, customer_name, notes)
        )
        
        if success:
            # Update product stock
            from models.product_model import ProductModel
            product_model = ProductModel()
            product_model.update_stock(product_id, -quantity)
        
        return success, sale_id
    
    def get_sales_by_date_range(self, start_date: str, end_date: str) -> list:
        """Get sales within a date range"""
        query = """
            SELECT s.*, p.product_name, u.username
            FROM sales s
            LEFT JOIN products p ON s.product_id = p.product_id
            LEFT JOIN users u ON s.user_id = u.user_id
            WHERE DATE(s.sale_date) BETWEEN ? AND ?
            ORDER BY s.sale_date DESC
        """
        results = self.db.execute_query(query, (start_date, end_date))
        return self.to_dict_list(results)
    
    def get_total_sales(self, days: int = 30) -> float:
        """Get total sales amount for the last N days"""
        query = """
            SELECT SUM(total_price) as total
            FROM sales
            WHERE sale_date >= datetime('now', '-' || ? || ' days')
        """
        results = self.db.execute_query(query, (days,))
        
        if results and len(results) > 0 and results[0]['total'] is not None:
            return float(results[0]['total'])
        return 0.0
    
    def get_sales_count(self, days: int = 30) -> int:
        """Get count of sales for the last N days"""
        query = """
            SELECT COUNT(*) as count
            FROM sales
            WHERE sale_date >= datetime('now', '-' || ? || ' days')
        """
        results = self.db.execute_query(query, (days,))
        
        if results and len(results) > 0:
            return results[0]['count']
        return 0
    
    def get_top_selling_products(self, limit: int = 5) -> list:
        """Get top selling products"""
        query = """
            SELECT p.product_name, SUM(s.quantity) as total_quantity, 
                   SUM(s.total_price) as total_revenue
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY s.product_id, p.product_name
            ORDER BY total_quantity DESC
            LIMIT ?
        """
        results = self.db.execute_query(query, (limit,))
        return self.to_dict_list(results)
    
    def delete_sale(self, sale_id: int) -> bool:
        """Delete a sale (admin only)"""
        query = "DELETE FROM sales WHERE sale_id = ?"
        success, _ = self.db.execute_update(query, (sale_id,))
        return success
