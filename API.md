# API Documentation

This document describes the internal API (models and controllers) of the Inventory Management System.

## Models API

All models extend `BaseModel` and interact with the SQLite database.

### UserModel

**Location:** `models/user_model.py`

#### Methods

##### `authenticate(username: str, password: str) -> Optional[Dict]`
Authenticate a user with username and password.

**Parameters:**
- `username`: User's username
- `password`: User's password

**Returns:** User data dictionary if authenticated, None otherwise

**Example:**
```python
from models.user_model import UserModel

user_model = UserModel()
user = user_model.authenticate('admin', 'admin123')
if user:
    print(f"Welcome {user['full_name']}")
```

##### `get_all_users() -> list`
Get all active users.

##### `create_user(username, password, full_name, role='user') -> tuple`
Create a new user.

**Returns:** `(success: bool, user_id: int)`

##### `update_user(user_id, username, full_name, role) -> bool`
Update user information.

##### `change_password(user_id, new_password) -> bool`
Change user password.

##### `deactivate_user(user_id) -> bool`
Deactivate a user account.

---

### ProductModel

**Location:** `models/product_model.py`

#### Methods

##### `get_all_products() -> list`
Get all products with category and supplier names.

**Returns:** List of product dictionaries

**Example:**
```python
from models.product_model import ProductModel

product_model = ProductModel()
products = product_model.get_all_products()
for product in products:
    print(f"{product['product_name']}: ${product['unit_price']}")
```

##### `get_product_by_id(product_id: int) -> Optional[Dict]`
Get product by ID with full details.

##### `search_products(search_term: str) -> list`
Search products by name or description.

##### `create_product(product_name, category_id, supplier_id, description, unit_price, quantity_in_stock, reorder_level) -> tuple`
Create a new product.

**Returns:** `(success: bool, product_id: int)`

##### `update_product(product_id, product_name, category_id, supplier_id, description, unit_price, quantity_in_stock, reorder_level) -> bool`
Update product information.

##### `delete_product(product_id: int) -> bool`
Delete a product.

##### `update_stock(product_id: int, quantity_change: int) -> bool`
Update product stock quantity.

**Parameters:**
- `quantity_change`: Amount to add (positive) or subtract (negative)

##### `get_low_stock_products() -> list`
Get products with stock below reorder level.

##### `get_stock_value() -> float`
Get total value of all stock.

---

### CategoryModel

**Location:** `models/category_model.py`

#### Methods

##### `get_all_categories() -> list`
Get all categories.

##### `get_category_by_id(category_id: int) -> Optional[Dict]`
Get category by ID.

##### `create_category(category_name: str, description: str = "") -> tuple`
Create a new category.

**Returns:** `(success: bool, category_id: int)`

##### `update_category(category_id, category_name, description) -> bool`
Update category information.

##### `delete_category(category_id: int) -> bool`
Delete a category.

##### `get_products_count(category_id: int) -> int`
Get count of products in a category.

---

### SupplierModel

**Location:** `models/supplier_model.py`

#### Methods

##### `get_all_suppliers() -> list`
Get all suppliers.

##### `get_supplier_by_id(supplier_id: int) -> Optional[Dict]`
Get supplier by ID.

##### `create_supplier(supplier_name, contact_person="", email="", phone="", address="") -> tuple`
Create a new supplier.

**Returns:** `(success: bool, supplier_id: int)`

##### `update_supplier(supplier_id, supplier_name, contact_person, email, phone, address) -> bool`
Update supplier information.

##### `delete_supplier(supplier_id: int) -> bool`
Delete a supplier.

##### `get_products_count(supplier_id: int) -> int`
Get count of products from a supplier.

---

### SaleModel

**Location:** `models/sale_model.py`

#### Methods

##### `get_all_sales(limit: int = 100) -> list`
Get all sales with product names.

##### `get_sale_by_id(sale_id: int) -> Optional[Dict]`
Get sale by ID.

##### `create_sale(product_id, quantity, unit_price, user_id, customer_name="", notes="") -> tuple`
Create a new sale and update product stock.

**Returns:** `(success: bool, sale_id: int or error_message: str)`

**Example:**
```python
from models.sale_model import SaleModel

sale_model = SaleModel()
success, sale_id = sale_model.create_sale(
    product_id=1,
    quantity=2,
    unit_price=99.99,
    user_id=1,
    customer_name="John Doe"
)
if success:
    print(f"Sale created with ID: {sale_id}")
```

##### `get_sales_by_date_range(start_date: str, end_date: str) -> list`
Get sales within a date range.

**Parameters:**
- `start_date`: Date in format "YYYY-MM-DD"
- `end_date`: Date in format "YYYY-MM-DD"

##### `get_total_sales(days: int = 30) -> float`
Get total sales amount for the last N days.

##### `get_sales_count(days: int = 30) -> int`
Get count of sales for the last N days.

##### `get_top_selling_products(limit: int = 5) -> list`
Get top selling products.

##### `delete_sale(sale_id: int) -> bool`
Delete a sale (admin only).

---

### PurchaseModel

**Location:** `models/purchase_model.py`

#### Methods

##### `get_all_purchases(limit: int = 100) -> list`
Get all purchases with product and supplier names.

##### `get_purchase_by_id(purchase_id: int) -> Optional[Dict]`
Get purchase by ID.

##### `create_purchase(product_id, supplier_id, quantity, unit_cost, user_id, notes="") -> tuple`
Create a new purchase and update product stock.

**Returns:** `(success: bool, purchase_id: int or error_message: str)`

**Example:**
```python
from models.purchase_model import PurchaseModel

purchase_model = PurchaseModel()
success, purchase_id = purchase_model.create_purchase(
    product_id=1,
    supplier_id=1,
    quantity=10,
    unit_cost=75.00,
    user_id=1,
    notes="Restocking"
)
```

##### `get_purchases_by_date_range(start_date: str, end_date: str) -> list`
Get purchases within a date range.

##### `get_total_purchases(days: int = 30) -> float`
Get total purchases amount for the last N days.

##### `get_purchases_count(days: int = 30) -> int`
Get count of purchases for the last N days.

##### `delete_purchase(purchase_id: int) -> bool`
Delete a purchase (admin only).

---

## Controllers API

Controllers handle business logic and validation.

### AuthController

**Location:** `controllers/auth_controller.py`

#### Methods

##### `login(username: str, password: str) -> tuple`
Authenticate user and create session.

**Returns:** `(success: bool, user_data or error_message)`

**Example:**
```python
from controllers.auth_controller import AuthController

auth = AuthController()
success, result = auth.login('admin', 'admin123')
if success:
    print(f"Logged in as: {result['full_name']}")
else:
    print(f"Login failed: {result}")
```

##### `logout()`
Clear current session.

##### `is_authenticated() -> bool`
Check if user is authenticated.

##### `get_current_user() -> Optional[Dict]`
Get current logged-in user.

##### `is_admin() -> bool`
Check if current user is admin.

---

### ProductController

**Location:** `controllers/product_controller.py`

#### Methods

##### `get_all_products() -> list`
Get all products.

##### `get_product(product_id: int) -> Optional[Dict]`
Get product by ID.

##### `search_products(search_term: str) -> list`
Search products.

##### `create_product(product_name, category_id, supplier_id, description, unit_price, quantity_in_stock, reorder_level) -> tuple`
Create a new product with validation.

**Returns:** `(success: bool, product_id or error_message: str)`

##### `update_product(product_id, product_name, category_id, supplier_id, description, unit_price, quantity_in_stock, reorder_level) -> tuple`
Update product with validation.

**Returns:** `(success: bool, success_message or error_message: str)`

##### `delete_product(product_id: int) -> tuple`
Delete product.

**Returns:** `(success: bool, message: str)`

##### `get_low_stock_products() -> list`
Get products with low stock.

##### `get_categories() -> list`
Get all categories.

##### `get_suppliers() -> list`
Get all suppliers.

---

### SalesController

**Location:** `controllers/sales_controller.py`

#### Methods

##### `get_all_sales(limit: int = 100) -> list`
Get all sales.

##### `create_sale(product_id, quantity, unit_price, user_id, customer_name="", notes="") -> tuple`
Create a new sale with validation.

**Returns:** `(success: bool, sale_id or error_message: str)`

**Validation:**
- Checks quantity > 0
- Checks unit_price >= 0
- Verifies product exists
- Verifies sufficient stock

##### `get_sales_report(start_date: str, end_date: str) -> list`
Get sales report for date range.

##### `get_total_sales(days: int = 30) -> float`
Get total sales amount.

##### `get_sales_count(days: int = 30) -> int`
Get count of sales.

##### `get_top_selling_products(limit: int = 5) -> list`
Get top selling products.

---

### PurchaseController

**Location:** `controllers/purchase_controller.py`

#### Methods

##### `get_all_purchases(limit: int = 100) -> list`
Get all purchases.

##### `create_purchase(product_id, supplier_id, quantity, unit_cost, user_id, notes="") -> tuple`
Create a new purchase with validation.

**Returns:** `(success: bool, purchase_id or error_message: str)`

**Validation:**
- Checks quantity > 0
- Checks unit_cost >= 0
- Verifies product exists
- Verifies supplier exists

##### `get_purchases_report(start_date: str, end_date: str) -> list`
Get purchases report for date range.

##### `get_total_purchases(days: int = 30) -> float`
Get total purchases amount.

##### `get_purchases_count(days: int = 30) -> int`
Get count of purchases.

---

## Utility Functions

**Location:** `utils/helpers.py`

### `validate_email(email: str) -> bool`
Validate email format.

### `validate_phone(phone: str) -> bool`
Validate phone format.

### `format_currency(amount: float) -> str`
Format amount as currency.

**Example:** `format_currency(1234.56)` returns `"$1,234.56"`

### `format_date(date_str: str) -> str`
Format date string to readable format.

### `get_date_range(days: int) -> tuple`
Get start and end date for last N days.

**Returns:** `(start_date: str, end_date: str)` in "YYYY-MM-DD" format

### `validate_positive_number(value, field_name: str) -> tuple`
Validate that a value is a positive number.

**Returns:** `(valid: bool, number or error_message)`

### `validate_positive_integer(value, field_name: str) -> tuple`
Validate that a value is a positive integer.

**Returns:** `(valid: bool, integer or error_message)`

---

## Database Schema

### Tables

#### users
- `user_id` (INTEGER, PRIMARY KEY)
- `username` (TEXT, UNIQUE, NOT NULL)
- `password` (TEXT, NOT NULL)
- `full_name` (TEXT, NOT NULL)
- `role` (TEXT, DEFAULT 'user')
- `created_at` (TIMESTAMP)
- `is_active` (INTEGER, DEFAULT 1)

#### categories
- `category_id` (INTEGER, PRIMARY KEY)
- `category_name` (TEXT, UNIQUE, NOT NULL)
- `description` (TEXT)
- `created_at` (TIMESTAMP)

#### suppliers
- `supplier_id` (INTEGER, PRIMARY KEY)
- `supplier_name` (TEXT, NOT NULL)
- `contact_person` (TEXT)
- `email` (TEXT)
- `phone` (TEXT)
- `address` (TEXT)
- `created_at` (TIMESTAMP)

#### products
- `product_id` (INTEGER, PRIMARY KEY)
- `product_name` (TEXT, NOT NULL)
- `category_id` (INTEGER, FOREIGN KEY)
- `supplier_id` (INTEGER, FOREIGN KEY)
- `description` (TEXT)
- `unit_price` (REAL, NOT NULL)
- `quantity_in_stock` (INTEGER, DEFAULT 0)
- `reorder_level` (INTEGER, DEFAULT 10)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

#### sales
- `sale_id` (INTEGER, PRIMARY KEY)
- `product_id` (INTEGER, FOREIGN KEY, NOT NULL)
- `quantity` (INTEGER, NOT NULL)
- `unit_price` (REAL, NOT NULL)
- `total_price` (REAL, NOT NULL)
- `sale_date` (TIMESTAMP)
- `user_id` (INTEGER, FOREIGN KEY)
- `customer_name` (TEXT)
- `notes` (TEXT)

#### purchases
- `purchase_id` (INTEGER, PRIMARY KEY)
- `product_id` (INTEGER, FOREIGN KEY, NOT NULL)
- `supplier_id` (INTEGER, FOREIGN KEY, NOT NULL)
- `quantity` (INTEGER, NOT NULL)
- `unit_cost` (REAL, NOT NULL)
- `total_cost` (REAL, NOT NULL)
- `purchase_date` (TIMESTAMP)
- `user_id` (INTEGER, FOREIGN KEY)
- `notes` (TEXT)

---

## Usage Examples

### Complete Workflow Example

```python
# 1. Authenticate
from controllers.auth_controller import AuthController
auth = AuthController()
success, user = auth.login('admin', 'admin123')

# 2. Add a product
from controllers.product_controller import ProductController
product_ctrl = ProductController()
success, product_id = product_ctrl.create_product(
    product_name="Laptop",
    category_id=1,
    supplier_id=1,
    description="Gaming laptop",
    unit_price=1299.99,
    quantity_in_stock=0,
    reorder_level=5
)

# 3. Purchase stock
from controllers.purchase_controller import PurchaseController
purchase_ctrl = PurchaseController()
success, purchase_id = purchase_ctrl.create_purchase(
    product_id=product_id,
    supplier_id=1,
    quantity=10,
    unit_cost=1000.00,
    user_id=user['user_id'],
    notes="Initial stock"
)

# 4. Make a sale
from controllers.sales_controller import SalesController
sales_ctrl = SalesController()
success, sale_id = sales_ctrl.create_sale(
    product_id=product_id,
    quantity=1,
    unit_price=1299.99,
    user_id=user['user_id'],
    customer_name="John Doe"
)

# 5. Check stock
products = product_ctrl.get_all_products()
for p in products:
    print(f"{p['product_name']}: {p['quantity_in_stock']} in stock")
```

---

For more information, see the [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md) files.
