"""
Test Suite for Inventory Management System
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.database import DatabaseManager
from models.user import UserManager
from models.category import CategoryManager
from models.supplier import SupplierManager
from models.product import ProductManager
from models.customer import CustomerManager


class TestInventorySystem(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up test database"""
        cls.db = DatabaseManager(':memory:')
    
    @classmethod
    def tearDownClass(cls):
        """Clean up"""
        cls.db.close()
    
    def test_01_database_creation(self):
        """Test database tables are created"""
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.db.cursor.fetchall()]
        
        self.assertIn('users', tables)
        self.assertIn('products', tables)
        self.assertIn('categories', tables)
        self.assertIn('suppliers', tables)
        self.assertIn('sales', tables)
        self.assertIn('purchases', tables)
    
    def test_02_user_authentication(self):
        """Test user authentication"""
        user_manager = UserManager(self.db)
        
        # Test default admin user
        user = user_manager.authenticate_user('admin', 'admin123')
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'admin')
        self.assertEqual(user['role'], 'Admin')
        
        # Test wrong password
        user = user_manager.authenticate_user('admin', 'wrongpassword')
        self.assertIsNone(user)
    
    def test_03_add_category(self):
        """Test adding a category"""
        category_manager = CategoryManager(self.db)
        
        cat_id = category_manager.add_category('Electronics', 'Electronic items')
        self.assertIsNotNone(cat_id)
        
        # Verify category
        category = category_manager.get_category_by_id(cat_id)
        self.assertEqual(category['category_name'], 'Electronics')
    
    def test_04_add_supplier(self):
        """Test adding a supplier"""
        supplier_manager = SupplierManager(self.db)
        
        sup_id = supplier_manager.add_supplier('ABC Suppliers', 'John Doe', '1234567890')
        self.assertIsNotNone(sup_id)
        
        # Verify supplier
        supplier = supplier_manager.get_supplier_by_id(sup_id)
        self.assertEqual(supplier['supplier_name'], 'ABC Suppliers')
    
    def test_05_add_product(self):
        """Test adding a product"""
        product_manager = ProductManager(self.db)
        
        # First ensure we have category and supplier
        category_manager = CategoryManager(self.db)
        supplier_manager = SupplierManager(self.db)
        
        cat_id = category_manager.add_category('Test Category', 'Test')
        sup_id = supplier_manager.add_supplier('Test Supplier', 'Test', '123')
        
        # Add product
        prod_id = product_manager.add_product(
            'Test Product', cat_id, sup_id, 100.0, 150.0, 50, 10
        )
        self.assertIsNotNone(prod_id)
        
        # Verify product
        product = product_manager.get_product_by_id(prod_id)
        self.assertEqual(product['product_name'], 'Test Product')
        self.assertEqual(product['stock_quantity'], 50)
    
    def test_06_product_search(self):
        """Test product search"""
        product_manager = ProductManager(self.db)
        
        # Search for product
        products = product_manager.search_products('Test Product')
        self.assertGreater(len(products), 0)
    
    def test_07_add_customer(self):
        """Test adding a customer"""
        customer_manager = CustomerManager(self.db)
        
        cust_id = customer_manager.add_customer('John Customer', '9876543210', 'john@example.com')
        self.assertIsNotNone(cust_id)
        
        # Verify customer
        customer = customer_manager.get_customer_by_id(cust_id)
        self.assertEqual(customer['customer_name'], 'John Customer')
    
    def test_08_stock_update(self):
        """Test stock updates"""
        product_manager = ProductManager(self.db)
        
        # Get a product
        products = product_manager.get_all_products()
        if products:
            product = products[0]
            original_stock = product['stock_quantity']
            
            # Update stock
            success = product_manager.update_stock(
                product['product_id'], 10, 'Adjustment', None, 'Test adjustment', 1
            )
            self.assertTrue(success)
            
            # Verify new stock
            updated_product = product_manager.get_product_by_id(product['product_id'])
            self.assertEqual(updated_product['stock_quantity'], original_stock + 10)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
