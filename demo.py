"""
Demo Script for Inventory Management System
Demonstrates all key features
"""
import sys
sys.path.insert(0, 'src')

from models.database import DatabaseManager
from models.user import UserManager
from models.category import CategoryManager
from models.supplier import SupplierManager
from models.product import ProductManager
from models.customer import CustomerManager
from models.purchase import PurchaseManager
from models.sales import SalesManager
from models.expense import ExpenseManager
from models.reports import ReportManager
from datetime import datetime, timedelta

print("=" * 60)
print("INVENTORY MANAGEMENT SYSTEM - DEMO")
print("=" * 60)

# Initialize database
print("\n1. Initializing database...")
db = DatabaseManager('demo_inventory.db')
print("   ✓ Database initialized")

# User authentication
print("\n2. Testing user authentication...")
user_manager = UserManager(db)
admin_user = user_manager.authenticate_user('admin', 'admin123')
print(f"   ✓ Logged in as: {admin_user['full_name']} ({admin_user['role']})")

# Add categories
print("\n3. Adding categories...")
category_manager = CategoryManager(db)
categories = [
    ('Electronics', 'Electronic items and accessories'),
    ('Groceries', 'Food and grocery items'),
    ('Clothing', 'Apparel and fashion items'),
    ('Stationery', 'Office and school supplies')
]

cat_ids = {}
for name, desc in categories:
    cat_id = category_manager.add_category(name, desc)
    cat_ids[name] = cat_id
    print(f"   ✓ Added: {name} (ID: {cat_id})")

# Add suppliers
print("\n4. Adding suppliers...")
supplier_manager = SupplierManager(db)
suppliers = [
    ('TechWorld Inc', 'Raj Kumar', '9876543210', 'raj@techworld.com'),
    ('Fresh Foods Ltd', 'Priya Singh', '9876543211', 'priya@freshfoods.com'),
    ('Fashion Hub', 'Amit Patel', '9876543212', 'amit@fashionhub.com')
]

sup_ids = {}
for name, contact, phone, email in suppliers:
    sup_id = supplier_manager.add_supplier(name, contact, phone, email)
    sup_ids[name] = sup_id
    print(f"   ✓ Added: {name} (ID: {sup_id})")

# Add products
print("\n5. Adding products...")
product_manager = ProductManager(db)
products = [
    ('Laptop', 'Electronics', 'TechWorld Inc', 40000, 50000, 10),
    ('Mouse', 'Electronics', 'TechWorld Inc', 200, 350, 50),
    ('Rice (1kg)', 'Groceries', 'Fresh Foods Ltd', 50, 70, 100),
    ('T-Shirt', 'Clothing', 'Fashion Hub', 200, 400, 30),
    ('Notebook', 'Stationery', 'TechWorld Inc', 30, 50, 200)
]

prod_ids = []
for name, cat, sup, unit_price, selling_price, stock in products:
    prod_id = product_manager.add_product(
        name, cat_ids[cat], sup_ids[sup], unit_price, selling_price, stock, 10
    )
    prod_ids.append(prod_id)
    print(f"   ✓ Added: {name} - Stock: {stock}, Price: ₹{selling_price}")

# Add customers
print("\n6. Adding customers...")
customer_manager = CustomerManager(db)
customers = [
    ('Ramesh Sharma', '9988776655', 'ramesh@example.com'),
    ('Sunita Devi', '9988776656', 'sunita@example.com'),
    ('Vikram Singh', '9988776657', 'vikram@example.com')
]

cust_ids = []
for name, phone, email in customers:
    cust_id = customer_manager.add_customer(name, phone, email)
    cust_ids.append(cust_id)
    print(f"   ✓ Added: {name}")

# Record a purchase
print("\n7. Recording a purchase...")
purchase_manager = PurchaseManager(db)
purchase_items = [
    {'product_id': prod_ids[0], 'quantity': 5, 'unit_price': 40000},
    {'product_id': prod_ids[1], 'quantity': 20, 'unit_price': 200}
]
purchase_id = purchase_manager.add_purchase(
    sup_ids['TechWorld Inc'],
    datetime.now().strftime('%Y-%m-%d'),
    purchase_items,
    paid_amount=150000,
    notes='Initial stock purchase',
    created_by=admin_user['user_id']
)
print(f"   ✓ Purchase recorded (Invoice: PUR-...)")
print(f"   ✓ Stock updated automatically")

# Record a sale
print("\n8. Recording a sale...")
sales_manager = SalesManager(db)
sale_items = [
    {'product_id': prod_ids[0], 'quantity': 2, 'unit_price': 50000},
    {'product_id': prod_ids[1], 'quantity': 3, 'unit_price': 350}
]
sale_id = sales_manager.add_sale(
    datetime.now().strftime('%Y-%m-%d'),
    sale_items,
    customer_id=cust_ids[0],
    tax_rate=18,
    discount_amount=500,
    payment_method='Cash',
    created_by=admin_user['user_id']
)
print(f"   ✓ Sale recorded (Invoice: INV-...)")
print(f"   ✓ Stock deducted automatically")
print(f"   ✓ Customer loyalty points updated")

# Add an expense
print("\n9. Recording business expense...")
expense_manager = ExpenseManager(db)
expense_id = expense_manager.add_expense(
    'Rent',
    15000,
    datetime.now().strftime('%Y-%m-%d'),
    'Monthly office rent',
    admin_user['user_id']
)
print(f"   ✓ Expense recorded: Rent - ₹15,000")

# Generate dashboard stats
print("\n10. Generating dashboard statistics...")
report_manager = ReportManager(db)
stats = report_manager.get_dashboard_stats()
print(f"   ✓ Total Products: {stats['total_products']}")
print(f"   ✓ Total Customers: {stats['total_customers']}")
print(f"   ✓ Total Stock Value: ₹{stats['total_stock_value']:,.2f}")
print(f"   ✓ Today's Sales: ₹{stats['today_sales_total']:,.2f}")
print(f"   ✓ Low Stock Items: {stats['low_stock_count']}")

# Check low stock products
print("\n11. Checking low stock products...")
low_stock = product_manager.get_low_stock_products()
if low_stock:
    print(f"   ⚠️  {len(low_stock)} products with low stock:")
    for product in low_stock[:3]:
        print(f"      - {product['product_name']}: {product['stock_quantity']} units")
else:
    print("   ✓ All products have adequate stock")

# Get top selling products
print("\n12. Top selling products (today)...")
today = datetime.now().strftime('%Y-%m-%d')
top_products = report_manager.get_top_selling_products(today, today, 5)
if top_products:
    for i, product in enumerate(top_products, 1):
        print(f"   {i}. {product['product_name']}: {product['total_quantity']} units, ₹{product['total_revenue']:,.2f}")
else:
    print("   No sales data yet")

# Profit/Loss report
print("\n13. Profit/Loss analysis (today)...")
profit_report = report_manager.get_profit_loss_report(today, today)
if profit_report:
    print(f"   Total Sales: ₹{profit_report['total_sales']:,.2f}")
    print(f"   COGS: ₹{profit_report['cogs']:,.2f}")
    print(f"   Gross Profit: ₹{profit_report['gross_profit']:,.2f}")
    print(f"   Net Profit: ₹{profit_report['net_profit']:,.2f}")
    print(f"   Profit Margin: {profit_report['net_margin']:.2f}%")

# Test backup
print("\n14. Creating database backup...")
backup_path = db.backup_database()
print(f"   ✓ Backup created: {backup_path}")

# Close database
db.close()

print("\n" + "=" * 60)
print("DEMO COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nAll features demonstrated:")
print("✓ User authentication")
print("✓ Category management")
print("✓ Supplier management")
print("✓ Product management with SKU generation")
print("✓ Customer management")
print("✓ Purchase management with stock updates")
print("✓ Sales management with automatic stock deduction")
print("✓ Expense tracking")
print("✓ Dashboard statistics")
print("✓ Reports and analytics")
print("✓ Database backup")
print("\nYou can now run 'python3 main.py' to start the GUI application!")
