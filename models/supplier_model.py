"""
Supplier Model for supplier management
"""

from models.base_model import BaseModel
from typing import Optional, Dict, Any


class SupplierModel(BaseModel):
    """Model for supplier-related database operations"""
    
    def get_all_suppliers(self) -> list:
        """Get all suppliers"""
        query = "SELECT * FROM suppliers ORDER BY supplier_name"
        results = self.db.execute_query(query)
        return self.to_dict_list(results)
    
    def get_supplier_by_id(self, supplier_id: int) -> Optional[Dict[str, Any]]:
        """Get supplier by ID"""
        query = "SELECT * FROM suppliers WHERE supplier_id = ?"
        results = self.db.execute_query(query, (supplier_id,))
        
        if results and len(results) > 0:
            return self.to_dict(results[0])
        return None
    
    def create_supplier(self, supplier_name: str, contact_person: str = "",
                       email: str = "", phone: str = "", address: str = "") -> tuple:
        """Create a new supplier"""
        query = """
            INSERT INTO suppliers (supplier_name, contact_person, email, phone, address)
            VALUES (?, ?, ?, ?, ?)
        """
        success, supplier_id = self.db.execute_update(
            query,
            (supplier_name, contact_person, email, phone, address)
        )
        return success, supplier_id
    
    def update_supplier(self, supplier_id: int, supplier_name: str, contact_person: str,
                       email: str, phone: str, address: str) -> bool:
        """Update supplier information"""
        query = """
            UPDATE suppliers 
            SET supplier_name = ?, contact_person = ?, email = ?, phone = ?, address = ?
            WHERE supplier_id = ?
        """
        success, _ = self.db.execute_update(
            query,
            (supplier_name, contact_person, email, phone, address, supplier_id)
        )
        return success
    
    def delete_supplier(self, supplier_id: int) -> bool:
        """Delete a supplier"""
        query = "DELETE FROM suppliers WHERE supplier_id = ?"
        success, _ = self.db.execute_update(query, (supplier_id,))
        return success
    
    def get_products_count(self, supplier_id: int) -> int:
        """Get count of products from a supplier"""
        query = "SELECT COUNT(*) as count FROM products WHERE supplier_id = ?"
        results = self.db.execute_query(query, (supplier_id,))
        
        if results and len(results) > 0:
            return results[0]['count']
        return 0
