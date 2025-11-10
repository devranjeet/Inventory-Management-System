# API Documentation - Inventory Management System

## Overview

This document describes the internal API structure of the Inventory Management System. The system uses a modular architecture with separate managers for different business entities.

## Architecture

```
┌─────────────────┐
│   GUI Views     │  (Tkinter Interface)
└────────┬────────┘
         │
┌────────▼────────┐
│   Controllers   │  (Business Logic)
└────────┬────────┘
         │
┌────────▼────────┐
│     Models      │  (Data Access Layer)
└────────┬────────┘
         │
┌────────▼────────┐
│  SQLite DB      │  (Data Storage)
└─────────────────┘
```

## Core Modules

### DatabaseManager

**Location:** `src/models/database.py`

Manages database connections and schema.

#### Methods:

```python
connect()
# Establishes database connection

create_tables()
# Creates all database tables

backup_database(backup_path=None) -> str
# Creates database backup
# Returns: Path to backup file

restore_database(backup_path) -> bool
# Restores database from backup
# Returns: Success status
```

### UserManager

**Location:** `src/models/user.py`

Handles user authentication and management.

#### Methods:

```python
authenticate_user(username, password) -> dict|None
# Authenticates user credentials
# Returns: User dict with id, username, full_name, role

add_user(username, password, full_name, role, email=None, phone=None) -> bool
# Creates new user account
# role: 'Admin' or 'Staff'

update_user(user_id, full_name=None, email=None, phone=None, role=None) -> bool
# Updates user information

change_password(user_id, new_password) -> bool
# Changes user password

deactivate_user(user_id) -> bool
# Deactivates user account

get_all_users() -> list
# Returns all users
```

### ProductManager

**Location:** `src/models/product.py`

Manages product inventory.

#### Methods:

```python
generate_sku() -> str
# Generates unique SKU code
# Format: SKU-XXXXXXXX

add_product(product_name, category_id, supplier_id, unit_price, 
           selling_price, stock_quantity=0, min_stock_level=10, 
           barcode=None, description=None) -> int|None
# Adds new product
# Returns: Product ID

update_product(product_id, **kwargs) -> bool
# Updates product fields
# Allowed fields: product_name, category_id, supplier_id, unit_price, 
#                 selling_price, stock_quantity, min_stock_level, barcode, description

delete_product(product_id) -> bool
# Deletes product

get_product_by_id(product_id) -> dict|None
# Returns product with category and supplier names

search_products(search_term) -> list
# Searches products by name, SKU, or barcode

get_all_products() -> list
# Returns all products

get_low_stock_products() -> list
# Returns products with stock <= min_stock_level

get_out_of_stock_products() -> list
# Returns products with stock = 0

update_stock(product_id, quantity_change, transaction_type, 
            reference_id=None, notes=None, created_by=None) -> bool
# Updates product stock and records history
# transaction_type: 'Purchase', 'Sale', 'Adjustment'

get_stock_history(product_id) -> list
# Returns stock change history
```

### CategoryManager

**Location:** `src/models/category.py`

Manages product categories.

#### Methods:

```python
add_category(category_name, description=None) -> int|None
# Adds new category
# Returns: Category ID

update_category(category_id, category_name=None, description=None) -> bool
# Updates category

delete_category(category_id) -> bool
# Deletes category (fails if category has products)

get_all_categories() -> list
# Returns all categories with product count

get_category_by_id(category_id) -> dict|None
# Returns category details

get_products_by_category(category_id) -> list
# Returns all products in category
```

### SupplierManager

**Location:** `src/models/supplier.py`

Manages supplier information.

#### Methods:

```python
add_supplier(supplier_name, contact_person=None, phone=None, 
            email=None, address=None) -> int|None
# Adds new supplier
# Returns: Supplier ID

update_supplier(supplier_id, **kwargs) -> bool
# Updates supplier fields
# Allowed fields: supplier_name, contact_person, phone, email, 
#                 address, outstanding_payment

delete_supplier(supplier_id) -> bool
# Deletes supplier (fails if supplier has products)

get_all_suppliers() -> list
# Returns all suppliers with product count

get_supplier_by_id(supplier_id) -> dict|None
# Returns supplier details

get_supplier_purchases(supplier_id) -> list
# Returns purchase history

update_outstanding_payment(supplier_id, amount_change) -> bool
# Updates outstanding payment balance
```

### PurchaseManager

**Location:** `src/models/purchase.py`

Manages purchase transactions.

#### Methods:

```python
generate_invoice_number() -> str
# Generates unique invoice number
# Format: PUR-YYYYMMDDHHmmss

add_purchase(supplier_id, purchase_date, items, paid_amount=0, 
            notes=None, created_by=None) -> int|None
# Records new purchase
# items: [{'product_id': int, 'quantity': int, 'unit_price': float}]
# Automatically updates stock and outstanding payments
# Returns: Purchase ID

get_purchase_by_id(purchase_id) -> dict|None
# Returns purchase details

get_purchase_items(purchase_id) -> list
# Returns items in purchase

get_all_purchases() -> list
# Returns all purchases

update_payment(purchase_id, additional_payment) -> bool
# Records additional payment for purchase
# Updates outstanding payment
```

### SalesManager

**Location:** `src/models/sales.py`

Manages sales transactions.

#### Methods:

```python
generate_invoice_number() -> str
# Generates unique invoice number
# Format: INV-YYYYMMDDHHmmss

add_sale(sale_date, items, customer_id=None, tax_rate=0, 
        discount_amount=0, payment_method=None, created_by=None) -> int|None
# Records new sale
# items: [{'product_id': int, 'quantity': int, 'unit_price': float}]
# Automatically deducts stock and awards loyalty points
# Returns: Sale ID

get_sale_by_id(sale_id) -> dict|None
# Returns sale details

get_sale_items(sale_id) -> list
# Returns items in sale

get_all_sales() -> list
# Returns all sales

get_sales_by_date_range(start_date, end_date) -> list
# Returns sales within date range
```

### CustomerManager

**Location:** `src/models/customer.py`

Manages customer information.

#### Methods:

```python
add_customer(customer_name, phone=None, email=None, address=None) -> int|None
# Adds new customer
# Returns: Customer ID

update_customer(customer_id, **kwargs) -> bool
# Updates customer fields
# Allowed fields: customer_name, phone, email, address, loyalty_points

delete_customer(customer_id) -> bool
# Deletes customer

get_all_customers() -> list
# Returns all customers with purchase count

get_customer_by_id(customer_id) -> dict|None
# Returns customer details

get_customer_purchases(customer_id) -> list
# Returns purchase history

search_customers(search_term) -> list
# Searches customers by name, phone, or email
```

### ExpenseManager

**Location:** `src/models/expense.py`

Manages business expenses.

#### Methods:

```python
add_expense(expense_type, amount, expense_date, description=None, 
           created_by=None) -> int|None
# Records new expense
# Returns: Expense ID

update_expense(expense_id, **kwargs) -> bool
# Updates expense fields

delete_expense(expense_id) -> bool
# Deletes expense

get_all_expenses() -> list
# Returns all expenses

get_expenses_by_date_range(start_date, end_date) -> list
# Returns expenses within date range

get_expenses_by_type(expense_type) -> list
# Returns expenses of specific type

get_expense_summary(start_date, end_date) -> list
# Returns expense summary by type
```

### ReportManager

**Location:** `src/models/reports.py`

Generates reports and analytics.

#### Methods:

```python
get_sales_report(start_date, end_date) -> list
# Returns daily sales summary

get_purchase_report(start_date, end_date) -> list
# Returns daily purchase summary

get_profit_loss_report(start_date, end_date) -> dict
# Returns profit/loss analysis
# Keys: total_sales, cogs, gross_profit, expenses, net_profit, 
#       gross_margin, net_margin

get_top_selling_products(start_date, end_date, limit=10) -> list
# Returns top selling products

get_category_sales_report(start_date, end_date) -> list
# Returns sales by category

get_supplier_purchase_report(start_date, end_date) -> list
# Returns purchases by supplier

get_dashboard_stats() -> dict
# Returns key metrics for dashboard
# Keys: total_products, low_stock_count, out_of_stock_count,
#       today_sales_count, today_sales_total, month_sales_count,
#       month_sales_total, total_customers, total_suppliers,
#       outstanding_payments, total_stock_value
```

### SettingsManager

**Location:** `src/models/settings.py`

Manages system settings.

#### Methods:

```python
get_setting(key) -> str|None
# Gets setting value

set_setting(key, value) -> bool
# Sets setting value

get_all_settings() -> list
# Returns all settings

get_currency() -> str
# Returns currency symbol

get_tax_rate() -> float
# Returns tax rate percentage

get_theme() -> str
# Returns theme name

get_low_stock_threshold() -> int
# Returns low stock threshold
```

## Utility Modules

### BarcodeGenerator

**Location:** `src/utils/barcode_gen.py`

```python
generate_barcode(data, barcode_type='code128', output_path='reports/barcodes') -> str|None
# Generates barcode image
# Returns: Path to image file

generate_product_barcode(product_sku) -> str|None
# Generates barcode for product SKU
```

### DataExporter

**Location:** `src/utils/data_utils.py`

```python
export_to_csv(data, columns, filename, output_path='reports') -> str|None
# Exports data to CSV
# Returns: Path to file

export_to_excel(data, columns, filename, output_path='reports') -> str|None
# Exports data to Excel
# Returns: Path to file
```

### DataImporter

**Location:** `src/utils/data_utils.py`

```python
import_from_csv(filepath) -> list|None
# Imports data from CSV
# Returns: List of dicts

import_from_excel(filepath) -> list|None
# Imports data from Excel
# Returns: List of dicts

validate_product_import(data) -> tuple
# Validates product import data
# Returns: (valid_rows, errors)
```

## Database Schema

### Key Tables:

- **users:** User accounts and roles
- **categories:** Product categories
- **suppliers:** Supplier information
- **products:** Product inventory
- **customers:** Customer information
- **purchases:** Purchase transactions
- **purchase_items:** Items in purchases
- **sales:** Sales transactions
- **sale_items:** Items in sales
- **expenses:** Business expenses
- **settings:** System configuration
- **stock_history:** Stock movement tracking

## Data Types

### User Object
```python
{
    'user_id': int,
    'username': str,
    'full_name': str,
    'role': str,  # 'Admin' or 'Staff'
    'email': str,
    'phone': str,
    'is_active': int,
    'created_at': str
}
```

### Product Object
```python
{
    'product_id': int,
    'sku': str,
    'product_name': str,
    'category_id': int,
    'category_name': str,
    'supplier_id': int,
    'supplier_name': str,
    'unit_price': float,
    'selling_price': float,
    'stock_quantity': int,
    'min_stock_level': int,
    'barcode': str,
    'description': str,
    'created_at': str,
    'updated_at': str
}
```

## Error Handling

All manager methods include try-except blocks and return appropriate values:
- **Success:** Return ID (for create), True (for update/delete), or data (for queries)
- **Failure:** Return None (for create), False (for update/delete), or empty list (for queries)

Errors are printed to console for debugging.

## Usage Examples

### Adding a Product
```python
from models.database import DatabaseManager
from models.product import ProductManager

db = DatabaseManager()
product_manager = ProductManager(db)

product_id = product_manager.add_product(
    product_name="Laptop",
    category_id=1,
    supplier_id=1,
    unit_price=40000,
    selling_price=50000,
    stock_quantity=10,
    min_stock_level=5
)
```

### Recording a Sale
```python
from models.sales import SalesManager

sales_manager = SalesManager(db)

items = [
    {'product_id': 1, 'quantity': 2, 'unit_price': 50000},
    {'product_id': 2, 'quantity': 1, 'unit_price': 350}
]

sale_id = sales_manager.add_sale(
    sale_date='2024-11-10',
    items=items,
    customer_id=1,
    tax_rate=18,
    discount_amount=500,
    payment_method='Cash',
    created_by=1
)
```

### Generating Reports
```python
from models.reports import ReportManager

report_manager = ReportManager(db)

stats = report_manager.get_dashboard_stats()
profit_report = report_manager.get_profit_loss_report('2024-11-01', '2024-11-10')
top_products = report_manager.get_top_selling_products('2024-11-01', '2024-11-10', 10)
```

---

**Version:** 1.0.0
**Last Updated:** November 2024
