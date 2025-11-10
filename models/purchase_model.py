"""
Purchase Model for purchase management
"""

from models.base_model import BaseModel
from typing import Optional, Dict, Any


class PurchaseModel(BaseModel):
    """Model for purchase-related database operations"""
    
    def get_all_purchases(self, limit: int = 100) -> list:
        """Get all purchases with product and supplier names"""
        query = """
            SELECT pu.*, p.product_name, s.supplier_name, u.username
            FROM purchases pu
            LEFT JOIN products p ON pu.product_id = p.product_id
            LEFT JOIN suppliers s ON pu.supplier_id = s.supplier_id
            LEFT JOIN users u ON pu.user_id = u.user_id
            ORDER BY pu.purchase_date DESC
            LIMIT ?
        """
        results = self.db.execute_query(query, (limit,))
        return self.to_dict_list(results)
    
    def get_purchase_by_id(self, purchase_id: int) -> Optional[Dict[str, Any]]:
        """Get purchase by ID"""
        query = """
            SELECT pu.*, p.product_name, s.supplier_name, u.username
            FROM purchases pu
            LEFT JOIN products p ON pu.product_id = p.product_id
            LEFT JOIN suppliers s ON pu.supplier_id = s.supplier_id
            LEFT JOIN users u ON pu.user_id = u.user_id
            WHERE pu.purchase_id = ?
        """
        results = self.db.execute_query(query, (purchase_id,))
        
        if results and len(results) > 0:
            return self.to_dict(results[0])
        return None
    
    def create_purchase(self, product_id: int, supplier_id: int, quantity: int,
                       unit_cost: float, user_id: int, notes: str = "") -> tuple:
        """
        Create a new purchase and update product stock
        
        Returns:
            Tuple of (success, purchase_id or error message)
        """
        total_cost = quantity * unit_cost
        
        # Insert purchase
        query = """
            INSERT INTO purchases (product_id, supplier_id, quantity, unit_cost, 
                                 total_cost, user_id, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        success, purchase_id = self.db.execute_update(
            query,
            (product_id, supplier_id, quantity, unit_cost, total_cost, user_id, notes)
        )
        
        if success:
            # Update product stock
            from models.product_model import ProductModel
            product_model = ProductModel()
            product_model.update_stock(product_id, quantity)
        
        return success, purchase_id
    
    def get_purchases_by_date_range(self, start_date: str, end_date: str) -> list:
        """Get purchases within a date range"""
        query = """
            SELECT pu.*, p.product_name, s.supplier_name, u.username
            FROM purchases pu
            LEFT JOIN products p ON pu.product_id = p.product_id
            LEFT JOIN suppliers s ON pu.supplier_id = s.supplier_id
            LEFT JOIN users u ON pu.user_id = u.user_id
            WHERE DATE(pu.purchase_date) BETWEEN ? AND ?
            ORDER BY pu.purchase_date DESC
        """
        results = self.db.execute_query(query, (start_date, end_date))
        return self.to_dict_list(results)
    
    def get_total_purchases(self, days: int = 30) -> float:
        """Get total purchases amount for the last N days"""
        query = """
            SELECT SUM(total_cost) as total
            FROM purchases
            WHERE purchase_date >= datetime('now', '-' || ? || ' days')
        """
        results = self.db.execute_query(query, (days,))
        
        if results and len(results) > 0 and results[0]['total'] is not None:
            return float(results[0]['total'])
        return 0.0
    
    def get_purchases_count(self, days: int = 30) -> int:
        """Get count of purchases for the last N days"""
        query = """
            SELECT COUNT(*) as count
            FROM purchases
            WHERE purchase_date >= datetime('now', '-' || ? || ' days')
        """
        results = self.db.execute_query(query, (days,))
        
        if results and len(results) > 0:
            return results[0]['count']
        return 0
    
    def delete_purchase(self, purchase_id: int) -> bool:
        """Delete a purchase (admin only)"""
        query = "DELETE FROM purchases WHERE purchase_id = ?"
        success, _ = self.db.execute_update(query, (purchase_id,))
        return success
