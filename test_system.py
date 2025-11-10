#!/usr/bin/env python3
"""
Test script for Inventory Management System
Run this to verify all components are working correctly
"""

import os
import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from database.database_manager import get_db_manager
        from models.user_model import UserModel
        from models.product_model import ProductModel
        from models.category_model import CategoryModel
        from models.supplier_model import SupplierModel
        from models.sale_model import SaleModel
        from models.purchase_model import PurchaseModel
        from controllers.auth_controller import AuthController
        from controllers.product_controller import ProductController
        from controllers.sales_controller import SalesController
        from controllers.purchase_controller import PurchaseController
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\nTesting database...")
    try:
        from database.database_manager import get_db_manager
        db = get_db_manager()
        
        # Test connection
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['users', 'categories', 'suppliers', 'products', 'sales', 'purchases']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"✗ Missing tables: {missing_tables}")
            return False
        
        conn.close()
        print("✓ Database initialized with all required tables")
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_authentication():
    """Test user authentication"""
    print("\nTesting authentication...")
    try:
        from controllers.auth_controller import AuthController
        
        auth = AuthController()
        
        # Test valid login
        success, user = auth.login('admin', 'admin123')
        if not success:
            print("✗ Admin login failed")
            return False
        
        if not auth.is_authenticated():
            print("✗ Authentication check failed")
            return False
        
        if not auth.is_admin():
            print("✗ Admin role check failed")
            return False
        
        # Test invalid login
        success, result = auth.login('invalid', 'wrong')
        if success:
            print("✗ Invalid login should fail")
            return False
        
        auth.logout()
        if auth.is_authenticated():
            print("✗ Logout failed")
            return False
        
        print("✓ Authentication working correctly")
        return True
    except Exception as e:
        print(f"✗ Authentication test failed: {e}")
        return False

def test_crud_operations():
    """Test CRUD operations"""
    print("\nTesting CRUD operations...")
    try:
        from controllers.product_controller import ProductController
        from models.category_model import CategoryModel
        from models.supplier_model import SupplierModel
        
        # Get categories and suppliers
        category_model = CategoryModel()
        supplier_model = SupplierModel()
        
        categories = category_model.get_all_categories()
        suppliers = supplier_model.get_all_suppliers()
        
        if not categories or not suppliers:
            print("✗ No default categories or suppliers found")
            return False
        
        product_ctrl = ProductController()
        
        # Create
        success, product_id = product_ctrl.create_product(
            "Test Product", categories[0]['category_id'], 
            suppliers[0]['supplier_id'], "Test Description",
            99.99, 10, 5
        )
        if not success:
            print("✗ Product creation failed")
            return False
        
        # Read
        product = product_ctrl.get_product(product_id)
        if not product or product['product_name'] != "Test Product":
            print("✗ Product read failed")
            return False
        
        # Update
        success, msg = product_ctrl.update_product(
            product_id, "Updated Product", categories[0]['category_id'],
            suppliers[0]['supplier_id'], "Updated Description",
            89.99, 15, 5
        )
        if not success:
            print("✗ Product update failed")
            return False
        
        # Verify update
        product = product_ctrl.get_product(product_id)
        if product['product_name'] != "Updated Product":
            print("✗ Product update verification failed")
            return False
        
        # Delete
        success, msg = product_ctrl.delete_product(product_id)
        if not success:
            print("✗ Product deletion failed")
            return False
        
        # Verify deletion
        product = product_ctrl.get_product(product_id)
        if product:
            print("✗ Product should be deleted")
            return False
        
        print("✓ CRUD operations working correctly")
        return True
    except Exception as e:
        print(f"✗ CRUD test failed: {e}")
        return False

def test_sales_purchases():
    """Test sales and purchases with stock management"""
    print("\nTesting sales and purchases...")
    try:
        from controllers.product_controller import ProductController
        from controllers.sales_controller import SalesController
        from controllers.purchase_controller import PurchaseController
        from models.category_model import CategoryModel
        from models.supplier_model import SupplierModel
        
        # Create test product
        category_model = CategoryModel()
        supplier_model = SupplierModel()
        categories = category_model.get_all_categories()
        suppliers = supplier_model.get_all_suppliers()
        
        product_ctrl = ProductController()
        success, product_id = product_ctrl.create_product(
            "Stock Test Product", categories[0]['category_id'],
            suppliers[0]['supplier_id'], "For testing",
            50.00, 0, 5
        )
        if not success:
            print("✗ Test product creation failed")
            return False
        
        # Test purchase (add stock)
        purchase_ctrl = PurchaseController()
        success, purchase_id = purchase_ctrl.create_purchase(
            product_id, suppliers[0]['supplier_id'], 10, 40.00, 1, "Test purchase"
        )
        if not success:
            print(f"✗ Purchase creation failed: {purchase_id}")
            return False
        
        # Verify stock increased
        product = product_ctrl.get_product(product_id)
        if product['quantity_in_stock'] != 10:
            print(f"✗ Stock should be 10, got {product['quantity_in_stock']}")
            return False
        
        # Test sale (reduce stock)
        sales_ctrl = SalesController()
        success, sale_id = sales_ctrl.create_sale(
            product_id, 3, 50.00, 1, "Test Customer", "Test sale"
        )
        if not success:
            print(f"✗ Sale creation failed: {sale_id}")
            return False
        
        # Verify stock decreased
        product = product_ctrl.get_product(product_id)
        if product['quantity_in_stock'] != 7:
            print(f"✗ Stock should be 7, got {product['quantity_in_stock']}")
            return False
        
        # Test insufficient stock
        success, result = sales_ctrl.create_sale(
            product_id, 10, 50.00, 1, "Test Customer", "Should fail"
        )
        if success:
            print("✗ Sale with insufficient stock should fail")
            return False
        
        # Clean up
        product_ctrl.delete_product(product_id)
        
        print("✓ Sales and purchases working correctly")
        return True
    except Exception as e:
        print(f"✗ Sales/purchases test failed: {e}")
        return False

def test_reports():
    """Test reporting functionality"""
    print("\nTesting reports...")
    try:
        from models.sale_model import SaleModel
        from models.purchase_model import PurchaseModel
        from models.product_model import ProductModel
        
        sale_model = SaleModel()
        purchase_model = PurchaseModel()
        product_model = ProductModel()
        
        # Test statistics
        total_sales = sale_model.get_total_sales(30)
        sales_count = sale_model.get_sales_count(30)
        total_purchases = purchase_model.get_total_purchases(30)
        purchases_count = purchase_model.get_purchases_count(30)
        stock_value = product_model.get_stock_value()
        
        print(f"  - Total sales (30 days): ${total_sales:.2f} ({sales_count} transactions)")
        print(f"  - Total purchases (30 days): ${total_purchases:.2f} ({purchases_count} transactions)")
        print(f"  - Stock value: ${stock_value:.2f}")
        
        # Test low stock
        low_stock = product_model.get_low_stock_products()
        print(f"  - Low stock products: {len(low_stock)}")
        
        # Test top products
        top_products = sale_model.get_top_selling_products(5)
        print(f"  - Top selling products: {len(top_products)}")
        
        print("✓ Reports working correctly")
        return True
    except Exception as e:
        print(f"✗ Reports test failed: {e}")
        return False

def test_validation():
    """Test input validation"""
    print("\nTesting validation...")
    try:
        from utils.helpers import (
            validate_email, validate_phone, validate_positive_number,
            validate_positive_integer, format_currency
        )
        
        # Test email validation
        if not validate_email("test@example.com"):
            print("✗ Valid email failed validation")
            return False
        
        if validate_email("invalid-email"):
            print("✗ Invalid email passed validation")
            return False
        
        # Test phone validation
        if not validate_phone("123-456-7890"):
            print("✗ Valid phone failed validation")
            return False
        
        # Test number validation
        valid, num = validate_positive_number("123.45", "Test")
        if not valid or num != 123.45:
            print("✗ Positive number validation failed")
            return False
        
        valid, _ = validate_positive_number("-10", "Test")
        if valid:
            print("✗ Negative number should fail validation")
            return False
        
        # Test integer validation
        valid, num = validate_positive_integer("10", "Test")
        if not valid or num != 10:
            print("✗ Positive integer validation failed")
            return False
        
        # Test currency formatting
        formatted = format_currency(1234.56)
        if formatted != "$1,234.56":
            print(f"✗ Currency formatting failed: {formatted}")
            return False
        
        print("✓ Validation working correctly")
        return True
    except Exception as e:
        print(f"✗ Validation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Inventory Management System - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_database,
        test_authentication,
        test_crud_operations,
        test_sales_purchases,
        test_reports,
        test_validation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("\n🎉 All tests passed! System is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
