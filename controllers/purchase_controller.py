"""
Purchase Controller
Handles purchase-related business logic
"""

from models.purchase_model import PurchaseModel
from models.product_model import ProductModel
from models.supplier_model import SupplierModel


class PurchaseController:
    """Controller for purchase operations"""
    
    def __init__(self):
        self.purchase_model = PurchaseModel()
        self.product_model = ProductModel()
        self.supplier_model = SupplierModel()
    
    def get_all_purchases(self, limit: int = 100) -> list:
        """Get all purchases"""
        return self.purchase_model.get_all_purchases(limit)
    
    def get_purchase(self, purchase_id: int):
        """Get purchase by ID"""
        return self.purchase_model.get_purchase_by_id(purchase_id)
    
    def create_purchase(self, product_id: int, supplier_id: int, quantity: int,
                       unit_cost: float, user_id: int, notes: str = "") -> tuple:
        """Create a new purchase with validation"""
        # Validate inputs
        if quantity <= 0:
            return False, "Quantity must be greater than 0"
        
        if unit_cost < 0:
            return False, "Unit cost cannot be negative"
        
        # Validate product exists
        product = self.product_model.get_product_by_id(product_id)
        if not product:
            return False, "Product not found"
        
        # Validate supplier exists
        supplier = self.supplier_model.get_supplier_by_id(supplier_id)
        if not supplier:
            return False, "Supplier not found"
        
        return self.purchase_model.create_purchase(
            product_id, supplier_id, quantity, unit_cost, user_id, notes
        )
    
    def get_purchases_report(self, start_date: str, end_date: str) -> list:
        """Get purchases report for date range"""
        return self.purchase_model.get_purchases_by_date_range(start_date, end_date)
    
    def get_total_purchases(self, days: int = 30) -> float:
        """Get total purchases amount"""
        return self.purchase_model.get_total_purchases(days)
    
    def get_purchases_count(self, days: int = 30) -> int:
        """Get count of purchases"""
        return self.purchase_model.get_purchases_count(days)
    
    def delete_purchase(self, purchase_id: int) -> tuple:
        """Delete a purchase (admin only)"""
        success = self.purchase_model.delete_purchase(purchase_id)
        
        if success:
            return True, "Purchase deleted successfully"
        else:
            return False, "Failed to delete purchase"
