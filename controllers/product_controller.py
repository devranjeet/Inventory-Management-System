"""
Product Controller
Handles product-related business logic
"""

from models.product_model import ProductModel
from models.category_model import CategoryModel
from models.supplier_model import SupplierModel


class ProductController:
    """Controller for product operations"""
    
    def __init__(self):
        self.product_model = ProductModel()
        self.category_model = CategoryModel()
        self.supplier_model = SupplierModel()
    
    def get_all_products(self) -> list:
        """Get all products"""
        return self.product_model.get_all_products()
    
    def get_product(self, product_id: int):
        """Get product by ID"""
        return self.product_model.get_product_by_id(product_id)
    
    def search_products(self, search_term: str) -> list:
        """Search products"""
        return self.product_model.search_products(search_term)
    
    def create_product(self, product_name: str, category_id: int, supplier_id: int,
                      description: str, unit_price: float, quantity_in_stock: int,
                      reorder_level: int) -> tuple:
        """Create a new product with validation"""
        # Validate inputs
        if not product_name or not product_name.strip():
            return False, "Product name is required"
        
        if unit_price < 0:
            return False, "Unit price cannot be negative"
        
        if quantity_in_stock < 0:
            return False, "Quantity cannot be negative"
        
        if reorder_level < 0:
            return False, "Reorder level cannot be negative"
        
        # Validate category exists
        if category_id:
            category = self.category_model.get_category_by_id(category_id)
            if not category:
                return False, "Invalid category selected"
        
        # Validate supplier exists
        if supplier_id:
            supplier = self.supplier_model.get_supplier_by_id(supplier_id)
            if not supplier:
                return False, "Invalid supplier selected"
        
        return self.product_model.create_product(
            product_name, category_id, supplier_id, description,
            unit_price, quantity_in_stock, reorder_level
        )
    
    def update_product(self, product_id: int, product_name: str, category_id: int,
                      supplier_id: int, description: str, unit_price: float,
                      quantity_in_stock: int, reorder_level: int) -> tuple:
        """Update product with validation"""
        # Validate inputs
        if not product_name or not product_name.strip():
            return False, "Product name is required"
        
        if unit_price < 0:
            return False, "Unit price cannot be negative"
        
        if quantity_in_stock < 0:
            return False, "Quantity cannot be negative"
        
        if reorder_level < 0:
            return False, "Reorder level cannot be negative"
        
        success = self.product_model.update_product(
            product_id, product_name, category_id, supplier_id, description,
            unit_price, quantity_in_stock, reorder_level
        )
        
        if success:
            return True, "Product updated successfully"
        else:
            return False, "Failed to update product"
    
    def delete_product(self, product_id: int) -> tuple:
        """Delete product"""
        success = self.product_model.delete_product(product_id)
        
        if success:
            return True, "Product deleted successfully"
        else:
            return False, "Failed to delete product"
    
    def get_low_stock_products(self) -> list:
        """Get products with low stock"""
        return self.product_model.get_low_stock_products()
    
    def get_categories(self) -> list:
        """Get all categories"""
        return self.category_model.get_all_categories()
    
    def get_suppliers(self) -> list:
        """Get all suppliers"""
        return self.supplier_model.get_all_suppliers()
