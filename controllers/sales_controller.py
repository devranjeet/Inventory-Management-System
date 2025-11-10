"""
Sales Controller
Handles sales-related business logic
"""

from models.sale_model import SaleModel
from models.product_model import ProductModel


class SalesController:
    """Controller for sales operations"""
    
    def __init__(self):
        self.sale_model = SaleModel()
        self.product_model = ProductModel()
    
    def get_all_sales(self, limit: int = 100) -> list:
        """Get all sales"""
        return self.sale_model.get_all_sales(limit)
    
    def get_sale(self, sale_id: int):
        """Get sale by ID"""
        return self.sale_model.get_sale_by_id(sale_id)
    
    def create_sale(self, product_id: int, quantity: int, unit_price: float,
                   user_id: int, customer_name: str = "", notes: str = "") -> tuple:
        """Create a new sale with validation"""
        # Validate inputs
        if quantity <= 0:
            return False, "Quantity must be greater than 0"
        
        if unit_price < 0:
            return False, "Unit price cannot be negative"
        
        # Check if product exists and has enough stock
        product = self.product_model.get_product_by_id(product_id)
        if not product:
            return False, "Product not found"
        
        if product['quantity_in_stock'] < quantity:
            return False, f"Insufficient stock. Available: {product['quantity_in_stock']}"
        
        return self.sale_model.create_sale(
            product_id, quantity, unit_price, user_id, customer_name, notes
        )
    
    def get_sales_report(self, start_date: str, end_date: str) -> list:
        """Get sales report for date range"""
        return self.sale_model.get_sales_by_date_range(start_date, end_date)
    
    def get_total_sales(self, days: int = 30) -> float:
        """Get total sales amount"""
        return self.sale_model.get_total_sales(days)
    
    def get_sales_count(self, days: int = 30) -> int:
        """Get count of sales"""
        return self.sale_model.get_sales_count(days)
    
    def get_top_selling_products(self, limit: int = 5) -> list:
        """Get top selling products"""
        return self.sale_model.get_top_selling_products(limit)
    
    def delete_sale(self, sale_id: int) -> tuple:
        """Delete a sale (admin only)"""
        success = self.sale_model.delete_sale(sale_id)
        
        if success:
            return True, "Sale deleted successfully"
        else:
            return False, "Failed to delete sale"
